"""
03_Asyncio.py

Industry-standard demonstration of `asyncio` for I/O-bound concurrency:
polling a lab information management system (LIMS) for the status of
several in-flight analysis jobs, with bounded concurrency, timeouts,
and cancellation.

Why asyncio here
-----------------
Checking N job statuses is dominated by waiting on network I/O. A
single-threaded event loop can juggle many such waits concurrently
without the memory/context-switch overhead of one OS thread per job.
This is cooperative concurrency: coroutines voluntarily yield control
at each `await` point rather than being preemptively interrupted.

All simulated network latency uses `await asyncio.sleep(...)`, never
`time.sleep()` -- a blocking sleep would freeze the entire event loop
and defeat the purpose of the coroutine model. Where genuinely
blocking/legacy work must be integrated, it is offloaded to a thread
via `asyncio.to_thread()` so it cannot stall the loop.
"""

from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass
from random import Random

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

MAX_CONCURRENT_STATUS_CHECKS = 5
PER_JOB_TIMEOUT_SECONDS = 1.0
OVERALL_TIMEOUT_SECONDS = 6.0

_RNG = Random(7)


class JobStatusError(RuntimeError):
    """Raised when a job status lookup fails."""


@dataclass(frozen=True, slots=True)
class JobStatus:
    job_id: str
    state: str
    progress_percent: int


async def _fetch_job_status(job_id: str, semaphore: asyncio.Semaphore) -> JobStatus:
    """
    Simulated async network call to the LIMS API.

    `asyncio.sleep` here stands in for an awaited HTTP/database call
    (e.g. `await session.get(...)`). It suspends only this coroutine,
    letting the event loop run other ready coroutines meanwhile.
    """
    async with semaphore:  # bounded concurrency: cap simultaneous LIMS requests
        latency = _RNG.uniform(0.1, 0.4)
        await asyncio.sleep(latency)
        if _RNG.random() < 0.1:
            raise JobStatusError(f"LIMS API returned an error for job {job_id}")
        state = _RNG.choice(["running", "queued", "completed"])
        progress = 100 if state == "completed" else _RNG.randint(0, 99)
        return JobStatus(job_id, state, progress)


async def _fetch_job_status_with_timeout(job_id: str, semaphore: asyncio.Semaphore) -> JobStatus:
    """Bound each individual lookup so one slow job cannot stall the batch."""
    try:
        async with asyncio.timeout(PER_JOB_TIMEOUT_SECONDS):
            return await _fetch_job_status(job_id, semaphore)
    except TimeoutError:
        logger.warning("job=%s status check timed out after %.1fs", job_id, PER_JOB_TIMEOUT_SECONDS)
        raise
    except asyncio.CancelledError:
        # Cancellation must not be swallowed: log for observability, then
        # re-raise so the surrounding scope (gather/task group) sees it.
        logger.info("job=%s status check cancelled", job_id)
        raise


def _blocking_legacy_metadata_lookup(job_id: str) -> str:
    """
    Stand-in for a genuinely blocking legacy client (e.g. an old
    synchronous SDK) that cannot be awaited directly. Must be offloaded
    off the event loop thread via asyncio.to_thread, never called
    directly from a coroutine.
    """
    time.sleep(0.05)  # real blocking I/O in the legacy client -- safe here because it runs in a worker thread
    return f"legacy-metadata-for-{job_id}"


async def _fetch_legacy_metadata(job_id: str) -> str:
    return await asyncio.to_thread(_blocking_legacy_metadata_lookup, job_id)


async def poll_all_jobs(job_ids: list[str]) -> tuple[list[JobStatus], list[BaseException]]:
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_STATUS_CHECKS)
    statuses: list[JobStatus] = []
    errors: list[BaseException] = []

    try:
        async with asyncio.timeout(OVERALL_TIMEOUT_SECONDS):
            tasks = [
                asyncio.create_task(_fetch_job_status_with_timeout(job_id, semaphore), name=f"status-{job_id}")
                for job_id in job_ids
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)
    except TimeoutError:
        logger.error("overall polling round exceeded %.1fs; remaining tasks were cancelled", OVERALL_TIMEOUT_SECONDS)
        return statuses, errors

    for job_id, outcome in zip(job_ids, results):
        if isinstance(outcome, JobStatus):
            statuses.append(outcome)
        elif isinstance(outcome, BaseException):
            errors.append(outcome)
            logger.warning("job=%s failed: %s", job_id, outcome)

    return statuses, errors


async def demonstrate_explicit_cancellation(job_ids: list[str]) -> None:
    """
    Demonstrates cooperative cancellation: start a status check, then
    cancel it mid-flight and confirm the coroutine cleans up rather
    than being silently abandoned.
    """
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_STATUS_CHECKS)
    task = asyncio.create_task(_fetch_job_status_with_timeout(job_ids[0], semaphore), name="cancel-demo")
    await asyncio.sleep(0.01)  # let it start, then cancel before it completes
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        logger.info("confirmed task '%s' was cancelled cleanly", task.get_name())


async def async_main() -> None:
    job_ids = [f"JOB-{i:03d}" for i in range(1, 9)]

    statuses, errors = await poll_all_jobs(job_ids)
    for status in sorted(statuses, key=lambda s: s.job_id):
        logger.info("job=%s state=%s progress=%d%%", status.job_id, status.state, status.progress_percent)
    logger.info("polled %d jobs: %d succeeded, %d failed", len(job_ids), len(statuses), len(errors))

    metadata = await _fetch_legacy_metadata(job_ids[0])
    logger.info("offloaded legacy metadata lookup result: %s", metadata)

    await demonstrate_explicit_cancellation(job_ids)


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
