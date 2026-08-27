"""
05_Task_Scheduling.py

Industry-standard demonstration of `asyncio` task orchestration:
scheduling, naming, bounding, monitoring, and cleanly shutting down a
set of concurrent scientific-pipeline jobs plus a periodic status
reporter.

Focus of this file (distinct from 03_Asyncio.py)
--------------------------------------------------
03_Asyncio.py shows the core event-loop primitives. This file shows
*task ownership*: every asyncio.Task created here has a clear owner
that is responsible for awaiting, cancelling, and retrieving its
result or exception. No task is created and abandoned as unmanaged
background work.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from random import Random

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

MAX_CONCURRENT_PIPELINE_JOBS = 3
JOB_TIMEOUT_SECONDS = 1.5
STATUS_REPORT_INTERVAL_SECONDS = 0.5

_RNG = Random(99)


class PipelineJobError(RuntimeError):
    """Raised when a scientific pipeline job fails."""


@dataclass(frozen=True, slots=True)
class JobOutcome:
    job_id: str
    duration_seconds: float


async def run_pipeline_job(job_id: str, semaphore: asyncio.Semaphore) -> JobOutcome:
    """A single scientific analysis job (e.g. variant-calling stage) run under a concurrency cap."""
    async with semaphore:
        started = asyncio.get_running_loop().time()
        duration = _RNG.uniform(0.2, 2.0)  # simulated variable job runtime
        try:
            await asyncio.sleep(duration)
        except asyncio.CancelledError:
            logger.info("job=%s cancelled after %.2fs; releasing resources", job_id, asyncio.get_running_loop().time() - started)
            raise
        if _RNG.random() < 0.15:
            raise PipelineJobError(f"job {job_id} failed during analysis stage")
        elapsed = asyncio.get_running_loop().time() - started
        return JobOutcome(job_id, elapsed)


async def run_job_with_timeout(job_id: str, semaphore: asyncio.Semaphore) -> JobOutcome:
    async with asyncio.timeout(JOB_TIMEOUT_SECONDS):
        return await run_pipeline_job(job_id, semaphore)


async def periodic_status_reporter(active_tasks: dict[str, asyncio.Task[JobOutcome]], stop_event: asyncio.Event) -> None:
    """
    Runs until `stop_event` is set, reporting on outstanding jobs at a
    fixed interval. Uses a stop event rather than an unconditional
    `while True: await asyncio.sleep(...)` loop with no exit
    mechanism, so the caller can always stop it deterministically.
    """
    try:
        while not stop_event.is_set():
            pending = [name for name, task in active_tasks.items() if not task.done()]
            logger.info("status report: %d job(s) still running: %s", len(pending), pending or "none")
            try:
                await asyncio.wait_for(stop_event.wait(), timeout=STATUS_REPORT_INTERVAL_SECONDS)
            except TimeoutError:
                continue  # normal: no stop signal yet, loop and report again
    except asyncio.CancelledError:
        logger.info("status reporter cancelled")
        raise
    finally:
        logger.info("status reporter shutting down")


async def orchestrate_jobs(job_ids: list[str]) -> tuple[list[JobOutcome], dict[str, BaseException]]:
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_PIPELINE_JOBS)
    stop_event = asyncio.Event()

    # Task ownership: this dict is the single source of truth for every
    # task we create. Nothing is fired-and-forgotten.
    job_tasks: dict[str, asyncio.Task[JobOutcome]] = {
        job_id: asyncio.create_task(run_job_with_timeout(job_id, semaphore), name=f"job-{job_id}")
        for job_id in job_ids
    }
    reporter_task = asyncio.create_task(periodic_status_reporter(job_tasks, stop_event), name="status-reporter")

    successes: list[JobOutcome] = []
    failures: dict[str, BaseException] = {}

    results = await asyncio.gather(*job_tasks.values(), return_exceptions=True)
    for job_id, outcome in zip(job_tasks.keys(), results):
        if isinstance(outcome, JobOutcome):
            successes.append(outcome)
        else:
            failures[job_id] = outcome
            if isinstance(outcome, TimeoutError):
                logger.warning("job=%s exceeded %.1fs timeout", job_id, JOB_TIMEOUT_SECONDS)
            else:
                logger.warning("job=%s raised %s: %s", job_id, outcome.__class__.__name__, outcome)

    # Graceful shutdown of the periodic reporter: signal, then await
    # its own cooperative exit rather than cancelling blindly.
    stop_event.set()
    try:
        await asyncio.wait_for(reporter_task, timeout=STATUS_REPORT_INTERVAL_SECONDS + 1.0)
    except TimeoutError:
        logger.error("status reporter did not stop in time; cancelling")
        reporter_task.cancel()
        await asyncio.gather(reporter_task, return_exceptions=True)

    return successes, failures


async def async_main() -> None:
    job_ids = [f"PIPE-{i:03d}" for i in range(1, 7)]
    successes, failures = await orchestrate_jobs(job_ids)
    logger.info("orchestration complete: %d succeeded, %d failed", len(successes), len(failures))
    for outcome in sorted(successes, key=lambda o: o.job_id):
        logger.info("job=%s completed in %.2fs", outcome.job_id, outcome.duration_seconds)


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
