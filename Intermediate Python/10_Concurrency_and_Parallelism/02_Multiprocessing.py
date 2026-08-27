"""
02_Multiprocessing.py

Industry-standard demonstration of Python `multiprocessing` for a
CPU-bound genomics workload: computing k-mer Shannon-entropy
complexity scores for DNA sequences.

Why multiprocessing here
-------------------------
Entropy scoring requires iterating every k-mer window of every
sequence and updating frequency counts -- pure CPU work with no I/O.
Because of CPython's GIL, threads would NOT parallelize this: only one
thread can execute Python bytecode at a time regardless of how many
threads exist. Separate OS processes each get their own interpreter
and GIL, so they can execute Python bytecode truly in parallel across
CPU cores. This is the correct tool for this workload.

Process memory vs thread memory
--------------------------------
Each worker process has its own private address space -- module-level
globals, imported data, etc. are copied (or re-imported) into the
child, not shared with the parent. There is no accidental shared
mutable state the way there is with threads. Communication must be
explicit, here via a multiprocessing.Queue used as a one-way result
channel (IPC), which pickles data across the process boundary.
"""

from __future__ import annotations

import logging
import math
import multiprocessing as mp
import time
import traceback
from dataclasses import dataclass, field
from random import Random

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(processName)s] %(message)s")

KMER_LENGTH = 4
BASES = "ACGT"
_RNG = Random(42)


class SequenceScoringError(RuntimeError):
    """Raised when a worker process fails to score a sequence."""


@dataclass(frozen=True, slots=True)
class SequenceJob:
    sequence_id: str
    sequence: str


@dataclass(frozen=True, slots=True)
class ScoreResult:
    sequence_id: str
    entropy_bits: float
    length: int
    worker_pid: int


@dataclass(frozen=True, slots=True)
class ScoreFailure:
    sequence_id: str
    error_message: str


def _generate_synthetic_sequence(length: int, rng: Random) -> str:
    return "".join(rng.choice(BASES) for _ in range(length))


def _kmer_entropy(sequence: str, k: int = KMER_LENGTH) -> float:
    """
    CPU-bound: Shannon entropy (bits) of the k-mer frequency
    distribution across a sliding window. Genuinely scales with
    sequence length -- O(n) window extraction plus counting -- and is
    representative of real sequence-complexity scoring used to flag
    low-complexity / repetitive genomic regions.
    """
    if len(sequence) < k:
        raise SequenceScoringError(f"sequence shorter than k-mer length {k}")

    counts: dict[str, int] = {}
    total = 0
    for i in range(len(sequence) - k + 1):
        kmer = sequence[i : i + k]
        counts[kmer] = counts.get(kmer, 0) + 1
        total += 1

    entropy = 0.0
    for count in counts.values():
        p = count / total
        entropy -= p * math.log2(p)
    return entropy


def _score_worker(job: SequenceJob, result_queue: mp.Queue) -> None:
    """
    Entry point executed inside a fresh child process.

    Any exception raised here happens in the CHILD's stack; it will
    not surface in the parent unless we explicitly capture and send it
    back over IPC. We convert failures into a ScoreFailure record
    rather than letting the child crash silently.
    """
    try:
        entropy = _kmer_entropy(job.sequence)
        result_queue.put(ScoreResult(job.sequence_id, entropy, len(job.sequence), mp.current_process().pid))
    except Exception as exc:  # noqa: BLE001 - deliberately broad: report all worker failures
        logger.error("sequence=%s failed: %s", job.sequence_id, exc)
        result_queue.put(ScoreFailure(job.sequence_id, f"{exc.__class__.__name__}: {exc}"))
        # Preserve traceback context in child-side logs for debugging.
        logger.debug("traceback for %s:\n%s", job.sequence_id, traceback.format_exc())


def score_sequences_in_parallel(
    jobs: list[SequenceJob],
    join_timeout_seconds: float = 30.0,
) -> tuple[list[ScoreResult], list[ScoreFailure]]:
    """
    Launch one process per sequence-scoring job (bounded by job count,
    which is small and deterministic in this demonstration; see
    08_Process_Pools.py for a pool-based approach that scales to many
    more independent jobs without per-job process-creation overhead).
    """
    result_queue: mp.Queue = mp.Queue()
    processes: list[mp.Process] = []

    started_at = time.monotonic()
    for job in jobs:
        process = mp.Process(target=_score_worker, name=f"score-{job.sequence_id}", args=(job, result_queue))
        processes.append(process)
        process.start()

    results: list[ScoreResult] = []
    failures: list[ScoreFailure] = []

    # Drain the queue before joining: on some platforms a child can
    # block on a full pipe if the parent hasn't consumed queued items,
    # which would deadlock a naive join-then-get ordering.
    for _ in processes:
        item = result_queue.get()
        if isinstance(item, ScoreResult):
            results.append(item)
        else:
            failures.append(item)

    deadline = started_at + join_timeout_seconds
    for process in processes:
        remaining = max(0.0, deadline - time.monotonic())
        process.join(timeout=remaining)
        if process.is_alive():
            logger.error("process %s did not exit in time; terminating", process.name)
            process.terminate()
            process.join(timeout=2.0)

    elapsed = time.monotonic() - started_at
    logger.info(
        "scored %d sequences in %.3fs across %d processes (%d succeeded, %d failed)",
        len(jobs),
        elapsed,
        len(processes),
        len(results),
        len(failures),
    )
    return results, failures


def main() -> None:
    jobs = [
        SequenceJob(f"SEQ-{i:03d}", _generate_synthetic_sequence(length=20_000, rng=Random(1000 + i)))
        for i in range(6)
    ]
    results, failures = score_sequences_in_parallel(jobs)
    for result in sorted(results, key=lambda r: r.sequence_id):
        logger.info(
            "sequence=%s entropy=%.4f bits length=%d worker_pid=%d",
            result.sequence_id,
            result.entropy_bits,
            result.length,
            result.worker_pid,
        )
    for failure in failures:
        logger.warning("sequence=%s scoring failed: %s", failure.sequence_id, failure.error_message)


if __name__ == "__main__":
    mp.freeze_support()
    main()
