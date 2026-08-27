"""
08_Process_Pools.py

Industry-standard demonstration of a process-pool architecture for
scalable CPU-bound work: scoring a large batch of independent DNA
sequences (e.g. a sequencing run's worth of reads) across all
available CPU cores.

ProcessPoolExecutor vs multiprocessing.Pool
--------------------------------------------
Both spin up a fixed pool of worker processes and distribute
independent jobs across them. `concurrent.futures.ProcessPoolExecutor`
is preferred for modern application code: it shares the same Future-
based interface as ThreadPoolExecutor (see 06_Concurrent_Futures.py),
which makes it trivial to swap executor types when a workload's
I/O-bound/CPU-bound classification changes, and it integrates cleanly
with `as_completed()` / `map()`. `multiprocessing.Pool` remains useful
when you need pool features ProcessPoolExecutor doesn't expose (e.g.
`imap_unordered`, explicit `apply_async` callbacks) -- shown briefly
below for comparison only.

Why a pool instead of one Process per job (contrast with
02_Multiprocessing.py)
------------------------------------------------------------------
02_Multiprocessing.py spins up one Process per job, which is fine for
a handful of long-running jobs but wasteful for many short,
independent jobs: process creation has real OS overhead. A pool
amortizes that cost by reusing a fixed set of worker processes across
many submitted jobs, and `map`'s `chunksize` batches multiple jobs per
IPC round trip to further cut overhead for small, numerous tasks.
"""

from __future__ import annotations

import logging
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from random import Random

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(processName)s] %(message)s")

BASES = "ACGT"
_RNG = Random(31)


class SequenceProcessingError(RuntimeError):
    """Raised when a sequence fails processing in a worker process."""


@dataclass(frozen=True, slots=True)
class SequenceRecord:
    read_id: str
    sequence: str


@dataclass(frozen=True, slots=True)
class SequenceMetrics:
    read_id: str
    gc_content: float
    length: int


def _generate_reads(count: int, length: int) -> list[SequenceRecord]:
    return [
        SequenceRecord(f"READ-{i:05d}", "".join(_RNG.choice(BASES) for _ in range(length)))
        for i in range(count)
    ]


# Module-level worker function: required for pickle-compatibility.
# Lambdas and nested/local functions cannot be submitted to a process
# pool because they cannot be pickled to send to the child process.
def compute_sequence_metrics(record: SequenceRecord) -> SequenceMetrics:
    """
    CPU-bound per-read computation: GC content over the full read.
    Independent per read, which is exactly the shape of job that
    benefits from process-pool parallelism -- no shared state needed
    between reads, so there is no coordination cost beyond dispatch
    and result collection.
    """
    if not record.sequence:
        raise SequenceProcessingError(f"empty sequence for read {record.read_id}")
    gc = sum(1 for base in record.sequence if base in "GC")
    return SequenceMetrics(record.read_id, gc / len(record.sequence), len(record.sequence))


def process_batch_with_executor(
    records: list[SequenceRecord],
    max_workers: int | None = None,
) -> tuple[list[SequenceMetrics], dict[str, str]]:
    """
    Distributes many independent per-read jobs across a bounded pool
    of worker processes using ProcessPoolExecutor.map(), which
    preserves input order and batches submissions via `chunksize` to
    reduce per-task IPC overhead for large read counts.
    """
    worker_count = max_workers or min(os.cpu_count() or 1, 8)
    metrics: list[SequenceMetrics] = []
    failures: dict[str, str] = {}

    chunk_size = max(1, len(records) // (worker_count * 4) or 1)

    # Context manager guarantees pool shutdown (and worker process
    # cleanup) even if an exception escapes this block.
    with ProcessPoolExecutor(max_workers=worker_count) as executor:
        futures = {
            executor.submit(compute_sequence_metrics, record): record.read_id for record in records
        }
        for future in as_completed(futures, timeout=60.0):
            read_id = futures[future]
            try:
                metrics.append(future.result(timeout=10.0))
            except SequenceProcessingError as exc:
                failures[read_id] = str(exc)
                logger.warning("read=%s processing failed: %s", read_id, exc)
            except Exception as exc:  # noqa: BLE001 - report unexpected worker failures explicitly
                failures[read_id] = f"unexpected error: {exc}"
                logger.error("read=%s unexpected failure: %s", read_id, exc)

    logger.info(
        "processed %d reads with %d worker processes (chunk hint=%d): %d succeeded, %d failed",
        len(records),
        worker_count,
        chunk_size,
        len(metrics),
        len(failures),
    )
    return metrics, failures


def process_batch_with_map(records: list[SequenceRecord], max_workers: int | None = None) -> list[SequenceMetrics]:
    """
    Alternative entry point using `executor.map()` directly, useful
    when per-task exception granularity is less important than simple
    ordered batch throughput. `chunksize` groups multiple jobs into a
    single IPC transfer, which matters when each individual job is
    cheap relative to pickling/dispatch overhead.
    """
    worker_count = max_workers or min(os.cpu_count() or 1, 8)
    chunk_size = max(1, len(records) // (worker_count * 4) or 1)

    with ProcessPoolExecutor(max_workers=worker_count) as executor:
        results = list(executor.map(compute_sequence_metrics, records, chunksize=chunk_size))
    return results


def main() -> None:
    reads = _generate_reads(count=64, length=5_000)

    metrics, failures = process_batch_with_executor(reads)
    mean_gc = sum(m.gc_content for m in metrics) / len(metrics) if metrics else 0.0
    logger.info("batch mean GC content: %.4f across %d reads", mean_gc, len(metrics))
    if failures:
        logger.warning("failed reads: %s", list(failures.keys()))


if __name__ == "__main__":
    main()
