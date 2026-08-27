"""
01_Threading.py

Industry-standard demonstration of Python `threading` for I/O-bound
workloads in a laboratory-automation context.

Scenario
--------
A lab controller polls several networked instruments for the latest
sensor readings associated with a batch of biological samples. Each
poll is I/O-bound: the thread spends almost all of its time waiting on
a (simulated) network round trip to the instrument, not on CPU work.
This is exactly the situation where CPython threads are useful: while
one thread is blocked on I/O, the GIL is released and other threads
can run.

GIL note
--------
Threads here provide *concurrency*, not CPU *parallelism*. CPython's
GIL still allows only one thread to execute Python bytecode at a time.
What we gain is that I/O waits overlap, so total wall-clock time is
close to the slowest single call, not the sum of all calls. If this
workload were CPU-bound, threading would not help; multiprocessing
would be required instead (see 02_Multiprocessing.py).

The "network call" below is simulated with time.sleep(). This is
explicitly a stand-in for a blocking socket/HTTP call to instrument
hardware -- it is not the concurrency mechanism itself.
"""

from __future__ import annotations

import logging
import threading
import time
from dataclasses import dataclass, field
from random import Random

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(threadName)s] %(message)s")

# Bounded concurrency: never open more than this many simultaneous
# "connections" to lab instruments, to respect instrument/network limits.
MAX_CONCURRENT_INSTRUMENT_CONNECTIONS = 4

# Deterministic pseudo-random source for reproducible simulated latency.
_RNG = Random(1234)


class InstrumentCommunicationError(RuntimeError):
    """Raised when a simulated instrument read fails."""


@dataclass(frozen=True, slots=True)
class InstrumentReading:
    sample_id: str
    instrument_id: str
    measurement: float


@dataclass(slots=True)
class ReadingsStore:
    """
    Shared mutable state written to by multiple worker threads.

    A dict's single __setitem__ is atomic in CPython, but the
    read-modify-write we perform here (append to a per-sample list,
    increment a failure counter) is NOT atomic. Without a lock, two
    threads could interleave and lose an update. Keep the critical
    section small: only the mutation itself is guarded, not the
    (slow) I/O call that produced the value.
    """

    _readings: dict[str, list[InstrumentReading]] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock)
    _failure_count: int = 0

    def record(self, reading: InstrumentReading) -> None:
        with self._lock:
            self._readings.setdefault(reading.sample_id, []).append(reading)

    def record_failure(self) -> None:
        with self._lock:
            self._failure_count += 1

    def snapshot(self) -> tuple[dict[str, list[InstrumentReading]], int]:
        with self._lock:
            return {k: list(v) for k, v in self._readings.items()}, self._failure_count


def _simulated_instrument_round_trip(sample_id: str, instrument_id: str) -> float:
    """
    Stand-in for a blocking network/serial call to lab hardware.

    This sleep is a SIMULATION of I/O latency only -- it does not
    itself provide concurrency. Concurrency comes from running several
    of these blocking calls on separate threads so their waits overlap.
    """
    latency_seconds = _RNG.uniform(0.05, 0.15)
    time.sleep(latency_seconds)
    if _RNG.random() < 0.05:
        raise InstrumentCommunicationError(
            f"instrument {instrument_id} timed out reading sample {sample_id}"
        )
    return round(_RNG.uniform(0.0, 100.0), 3)


def poll_instrument(
    sample_id: str,
    instrument_id: str,
    store: ReadingsStore,
    connection_limiter: threading.Semaphore,
    stop_event: threading.Event,
    errors: list[BaseException],
    errors_lock: threading.Lock,
) -> None:
    """
    Worker executed on a dedicated thread per instrument poll.

    Exceptions raised inside a thread do NOT propagate to the main
    thread automatically. We must explicitly capture and hand them
    back via shared, synchronized state (`errors`).
    """
    if stop_event.is_set():
        return

    # Bound simultaneous "connections" so we don't overwhelm lab
    # hardware/network capacity.
    with connection_limiter:
        if stop_event.is_set():
            return
        try:
            measurement = _simulated_instrument_round_trip(sample_id, instrument_id)
            store.record(InstrumentReading(sample_id, instrument_id, measurement))
            logger.info("sample=%s instrument=%s reading=%.3f", sample_id, instrument_id, measurement)
        except InstrumentCommunicationError as exc:
            store.record_failure()
            with errors_lock:
                errors.append(exc)
            logger.warning("sample=%s instrument=%s failed: %s", sample_id, instrument_id, exc)


def run_polling_round(
    sample_ids: list[str],
    instrument_ids: list[str],
    timeout_seconds: float = 5.0,
) -> tuple[dict[str, list[InstrumentReading]], int, list[BaseException]]:
    store = ReadingsStore()
    connection_limiter = threading.Semaphore(MAX_CONCURRENT_INSTRUMENT_CONNECTIONS)
    stop_event = threading.Event()
    errors: list[BaseException] = []
    errors_lock = threading.Lock()

    threads: list[threading.Thread] = []
    for sample_id in sample_ids:
        for instrument_id in instrument_ids:
            thread = threading.Thread(
                target=poll_instrument,
                name=f"poll-{sample_id}-{instrument_id}",
                args=(sample_id, instrument_id, store, connection_limiter, stop_event, errors, errors_lock),
                daemon=True,
            )
            threads.append(thread)

    started_at = time.monotonic()
    for thread in threads:
        thread.start()

    # Graceful shutdown: join every thread with a bounded deadline so a
    # stuck instrument call cannot hang the whole program indefinitely.
    deadline = started_at + timeout_seconds
    for thread in threads:
        remaining = max(0.0, deadline - time.monotonic())
        thread.join(timeout=remaining)
        if thread.is_alive():
            logger.error("thread %s exceeded deadline; signalling stop", thread.name)
            stop_event.set()

    elapsed = time.monotonic() - started_at
    readings, failure_count = store.snapshot()
    logger.info(
        "polling round complete in %.3fs: %d samples with readings, %d failures, %d captured errors",
        elapsed,
        len(readings),
        failure_count,
        len(errors),
    )
    return readings, failure_count, errors


def main() -> None:
    sample_ids = [f"SAMPLE-{i:03d}" for i in range(1, 6)]
    instrument_ids = ["PCR-01", "SEQ-02"]
    run_polling_round(sample_ids, instrument_ids)


if __name__ == "__main__":
    main()
