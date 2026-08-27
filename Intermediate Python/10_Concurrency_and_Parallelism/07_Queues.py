"""
07_Queues.py

Industry-standard demonstration of `queue.Queue`-based producer/
consumer architecture: a bounded, multi-stage sample-processing
pipeline running on dedicated threads.

Pipeline
--------
    Producer -> Validation Worker -> Analysis Worker -> Result Consumer

Each arrow is a bounded `queue.Queue`. Bounding queue size provides
backpressure: if downstream workers fall behind, upstream producers
block on `put()` instead of buffering unbounded amounts of in-flight
work in memory. This is essential for a pipeline processing large
sample batches where an unbounded queue could exhaust memory.

Shutdown uses a sentinel value (`_SHUTDOWN`) propagated stage by
stage: each worker, upon receiving the sentinel, forwards it to its
own output queue (so downstream stages also stop) and then exits its
loop. `task_done()`/`join()` are used to let the producer confirm all
enqueued work has actually been processed, not merely enqueued.
"""

from __future__ import annotations

import logging
import queue
import threading
import time
from dataclasses import dataclass
from random import Random

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(threadName)s] %(message)s")

QUEUE_MAX_SIZE = 5  # bounded: caps in-flight items per stage, providing backpressure
QUEUE_OP_TIMEOUT_SECONDS = 2.0

_SHUTDOWN = object()  # sentinel signalling "no more work"

_RNG = Random(55)


class SampleValidationError(RuntimeError):
    """Raised when a sample fails validation."""


@dataclass(frozen=True, slots=True)
class RawSample:
    sample_id: str
    optical_density: float


@dataclass(frozen=True, slots=True)
class ValidatedSample:
    sample_id: str
    optical_density: float


@dataclass(frozen=True, slots=True)
class AnalyzedSample:
    sample_id: str
    concentration_ng_per_ul: float


def producer(raw_samples: list[RawSample], out_q: queue.Queue) -> None:
    """Produces raw samples into the pipeline, blocking (backpressure) when downstream is full."""
    for sample in raw_samples:
        while True:
            try:
                out_q.put(sample, timeout=QUEUE_OP_TIMEOUT_SECONDS)
                logger.info("produced sample=%s", sample.sample_id)
                break
            except queue.Full:
                logger.warning("validation queue full; producer backing off")
                continue
    out_q.put(_SHUTDOWN)
    logger.info("producer finished; sentinel sent")


def validation_worker(in_q: queue.Queue, out_q: queue.Queue) -> None:
    """Validates each sample, forwarding only valid ones downstream. Forwards the sentinel on exit."""
    while True:
        try:
            item = in_q.get(timeout=QUEUE_OP_TIMEOUT_SECONDS)
        except queue.Empty:
            logger.error("validation worker timed out waiting for input; treating as shutdown")
            break

        if item is _SHUTDOWN:
            in_q.task_done()
            out_q.put(_SHUTDOWN)
            logger.info("validation worker forwarding shutdown sentinel")
            break

        sample: RawSample = item
        try:
            if sample.optical_density <= 0:
                raise SampleValidationError(f"non-positive optical density for {sample.sample_id}")
            out_q.put(ValidatedSample(sample.sample_id, sample.optical_density), timeout=QUEUE_OP_TIMEOUT_SECONDS)
            logger.info("validated sample=%s", sample.sample_id)
        except SampleValidationError as exc:
            logger.warning("sample=%s rejected: %s", sample.sample_id, exc)
        finally:
            in_q.task_done()


def analysis_worker(in_q: queue.Queue, out_q: queue.Queue) -> None:
    """CPU-light transformation stage: converts optical density to an estimated concentration."""
    while True:
        try:
            item = in_q.get(timeout=QUEUE_OP_TIMEOUT_SECONDS)
        except queue.Empty:
            logger.error("analysis worker timed out waiting for input; treating as shutdown")
            break

        if item is _SHUTDOWN:
            in_q.task_done()
            out_q.put(_SHUTDOWN)
            logger.info("analysis worker forwarding shutdown sentinel")
            break

        sample: ValidatedSample = item
        # Representative deterministic transformation (Beer-Lambert-style scaling).
        concentration = round(sample.optical_density * 50.0, 3)
        out_q.put(AnalyzedSample(sample.sample_id, concentration), timeout=QUEUE_OP_TIMEOUT_SECONDS)
        logger.info("analyzed sample=%s concentration=%.3f ng/uL", sample.sample_id, concentration)
        in_q.task_done()


def result_consumer(in_q: queue.Queue, collected: list[AnalyzedSample], collected_lock: threading.Lock) -> None:
    """Terminal stage: collects final results. Stops on the sentinel; does not forward further."""
    while True:
        try:
            item = in_q.get(timeout=QUEUE_OP_TIMEOUT_SECONDS)
        except queue.Empty:
            logger.error("result consumer timed out waiting for input; treating as shutdown")
            break

        if item is _SHUTDOWN:
            in_q.task_done()
            logger.info("result consumer received shutdown sentinel")
            break

        with collected_lock:
            collected.append(item)
        in_q.task_done()


def run_sample_pipeline(raw_samples: list[RawSample]) -> list[AnalyzedSample]:
    validation_q: queue.Queue = queue.Queue(maxsize=QUEUE_MAX_SIZE)
    analysis_q: queue.Queue = queue.Queue(maxsize=QUEUE_MAX_SIZE)
    result_q: queue.Queue = queue.Queue(maxsize=QUEUE_MAX_SIZE)

    collected: list[AnalyzedSample] = []
    collected_lock = threading.Lock()

    threads = [
        threading.Thread(target=producer, name="producer", args=(raw_samples, validation_q)),
        threading.Thread(target=validation_worker, name="validator", args=(validation_q, analysis_q)),
        threading.Thread(target=analysis_worker, name="analyzer", args=(analysis_q, result_q)),
        threading.Thread(target=result_consumer, name="consumer", args=(result_q, collected, collected_lock)),
    ]

    started_at = time.monotonic()
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=30.0)
        if thread.is_alive():
            logger.error("thread %s failed to exit cleanly", thread.name)

    elapsed = time.monotonic() - started_at
    logger.info("pipeline complete in %.3fs: %d samples reached the consumer", elapsed, len(collected))
    return collected


def main() -> None:
    raw_samples = [
        RawSample(f"SAMPLE-{i:03d}", optical_density=_RNG.uniform(-0.3, 1.2)) for i in range(1, 13)
    ]
    results = run_sample_pipeline(raw_samples)
    for result in sorted(results, key=lambda r: r.sample_id):
        logger.info("final: sample=%s concentration=%.3f ng/uL", result.sample_id, result.concentration_ng_per_ul)


if __name__ == "__main__":
    main()
