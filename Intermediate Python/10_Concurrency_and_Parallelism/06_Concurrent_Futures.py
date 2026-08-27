"""
06_Concurrent_Futures.py

Industry-standard demonstration of `concurrent.futures`, contrasting
ThreadPoolExecutor (I/O-bound work) with ProcessPoolExecutor (CPU-bound
work) on two distinct scientific workloads.

Workload split
--------------
- I/O-bound: fetching sample metadata from a (simulated) external
  LIMS service. Dominated by wait time -> ThreadPoolExecutor, because
  threads release the GIL while blocked on I/O, letting many requests
  overlap cheaply.
- CPU-bound: computing GC-content and molecular-weight-style scores
  for DNA sequences. Dominated by interpreter bytecode execution ->
  ProcessPoolExecutor, because only separate processes can execute
  Python bytecode in true parallel across cores under CPython's GIL.

Using ThreadPoolExecutor for the CPU-bound job, or ProcessPoolExecutor
for the I/O-bound job, would be the wrong tool: the former would not
speed up CPU work (GIL-bound), and the latter would pay needless
process-startup/pickling overhead for work that is mostly waiting.
"""

from __future__ import annotations

import logging
import time
from concurrent.futures import (
    Future,
    ProcessPoolExecutor,
    ThreadPoolExecutor,
    TimeoutError as FuturesTimeoutError,
    as_completed,
)
from dataclasses import dataclass
from random import Random

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(threadName)s/%(processName)s] %(message)s")

IO_MAX_WORKERS = 6
CPU_MAX_WORKERS = 4
IO_FETCH_TIMEOUT_SECONDS = 2.0

_RNG = Random(2024)


class MetadataFetchError(RuntimeError):
    """Raised when simulated LIMS metadata retrieval fails."""


@dataclass(frozen=True, slots=True)
class SampleMetadata:
    sample_id: str
    collection_site: str


def fetch_sample_metadata(sample_id: str) -> SampleMetadata:
    """I/O-bound: simulated blocking call to an external LIMS HTTP API."""
    time.sleep(_RNG.uniform(0.05, 0.2))  # simulated network latency
    if _RNG.random() < 0.1:
        raise MetadataFetchError(f"LIMS lookup failed for {sample_id}")
    site = _RNG.choice(["Site-A", "Site-B", "Site-C"])
    return SampleMetadata(sample_id, site)


def gc_content_score(sequence: str) -> float:
    """CPU-bound: pure computation over the sequence, no I/O."""
    if not sequence:
        return 0.0
    gc = sum(1 for base in sequence if base in "GC")
    return gc / len(sequence)


def demonstrate_thread_pool(sample_ids: list[str]) -> tuple[list[SampleMetadata], dict[str, BaseException]]:
    """I/O-bound fan-out using a bounded ThreadPoolExecutor."""
    results: list[SampleMetadata] = []
    failures: dict[str, BaseException] = {}

    with ThreadPoolExecutor(max_workers=IO_MAX_WORKERS, thread_name_prefix="metadata") as executor:
        future_to_sample: dict[Future[SampleMetadata], str] = {
            executor.submit(fetch_sample_metadata, sample_id): sample_id for sample_id in sample_ids
        }
        # as_completed() lets us process results as they arrive rather
        # than waiting for the slowest submission, which matters when
        # requests have highly variable latency.
        for future in as_completed(future_to_sample, timeout=IO_FETCH_TIMEOUT_SECONDS * 3):
            sample_id = future_to_sample[future]
            try:
                metadata = future.result(timeout=IO_FETCH_TIMEOUT_SECONDS)
                results.append(metadata)
                logger.info("sample=%s metadata site=%s", metadata.sample_id, metadata.collection_site)
            except MetadataFetchError as exc:
                failures[sample_id] = exc
                logger.warning("sample=%s metadata fetch failed: %s", sample_id, exc)
            except FuturesTimeoutError as exc:
                failures[sample_id] = exc
                logger.warning("sample=%s metadata fetch timed out", sample_id)

    return results, failures


def demonstrate_process_pool(sequences: dict[str, str]) -> tuple[dict[str, float], dict[str, BaseException]]:
    """CPU-bound fan-out using a bounded ProcessPoolExecutor."""
    scores: dict[str, float] = {}
    failures: dict[str, BaseException] = {}

    with ProcessPoolExecutor(max_workers=CPU_MAX_WORKERS) as executor:
        # map() preserves input order and is convenient when every job
        # runs the same function; exceptions are raised lazily as each
        # result is consumed, so we still need to guard iteration.
        sequence_ids = list(sequences.keys())
        futures = [executor.submit(gc_content_score, sequences[sid]) for sid in sequence_ids]
        for sequence_id, future in zip(sequence_ids, futures):
            try:
                scores[sequence_id] = future.result(timeout=10.0)
            except Exception as exc:  # noqa: BLE001 - report all worker failures explicitly
                failures[sequence_id] = exc
                logger.warning("sequence=%s scoring failed: %s", sequence_id, exc)

    return scores, failures


def main() -> None:
    sample_ids = [f"SAMPLE-{i:03d}" for i in range(1, 10)]
    metadata_results, metadata_failures = demonstrate_thread_pool(sample_ids)
    logger.info("metadata fetch: %d succeeded, %d failed", len(metadata_results), len(metadata_failures))

    sequences = {
        f"SEQ-{i:03d}": "".join(_RNG.choice("ACGT") for _ in range(50_000))
        for i in range(6)
    }
    scores, scoring_failures = demonstrate_process_pool(sequences)
    for sequence_id, score in sorted(scores.items()):
        logger.info("sequence=%s gc_content=%.4f", sequence_id, score)
    logger.info("gc-content scoring: %d succeeded, %d failed", len(scores), len(scoring_failures))


if __name__ == "__main__":
    main()
