from __future__ import annotations

import asyncio
from dataclasses import dataclass


class UniversityAsyncSyntax:
    """Simple coroutine and await example simulating a single laboratory
    data retrieval over the network (I/O-bound, non-blocking)."""

    @staticmethod
    async def fetch_sample_reading(sample_id: str) -> float:
        """Simulate an I/O-bound network call with asyncio.sleep, which
        yields control back to the event loop instead of blocking it
        the way time.sleep() would.

        Time: O(1) plus the simulated I/O delay
        """
        await asyncio.sleep(0.01)
        return 6.8 if sample_id == "S001" else 7.2

    @staticmethod
    async def _main() -> None:
        reading = await UniversityAsyncSyntax.fetch_sample_reading("S001")
        print("University: fetched reading ->", reading)

    @staticmethod
    def run() -> None:
        asyncio.run(UniversityAsyncSyntax._main())


class InstrumentTimeoutError(Exception):
    """Raised when an instrument does not respond within the expected time."""


class InterviewAsyncSyntax:
    """Coordinate multiple concurrent async operations using
    asyncio.gather to collect several experiment statuses concurrently
    rather than sequentially."""

    @staticmethod
    async def fetch_experiment_status(experiment_id: str) -> dict[str, str]:
        """Simulate a per-experiment status check.

        Time: O(1) plus simulated I/O delay
        """
        await asyncio.sleep(0.01)
        if experiment_id == "EXP-BAD":
            raise InstrumentTimeoutError(f"{experiment_id} did not respond")
        return {"experiment_id": experiment_id, "status": "running"}

    @staticmethod
    async def fetch_all_statuses(experiment_ids: list[str]) -> list[dict[str, str] | str]:
        """Run all status checks concurrently and handle individual
        failures without aborting the whole batch.

        Time: O(max single-call latency) instead of O(sum of latencies)
        for sequential awaiting.
        """
        results = await asyncio.gather(
            *(InterviewAsyncSyntax.fetch_experiment_status(eid) for eid in experiment_ids),
            return_exceptions=True,
        )
        normalized: list[dict[str, str] | str] = []
        for experiment_id, result in zip(experiment_ids, results):
            if isinstance(result, Exception):
                normalized.append(f"{experiment_id}: failed ({result})")
            else:
                normalized.append(result)
        return normalized

    @staticmethod
    async def _main() -> None:
        statuses = await InterviewAsyncSyntax.fetch_all_statuses(["EXP-1", "EXP-2", "EXP-BAD"])
        for status in statuses:
            print("Interview:", status)

    @staticmethod
    def run() -> None:
        asyncio.run(InterviewAsyncSyntax._main())


@dataclass(slots=True, frozen=True)
class SequencingResult:
    job_id: str
    read_count: int


class SequencingServiceClient:
    """Async context manager simulating a connection to a remote
    sequencing service, ensuring connection cleanup even on failure."""

    def __init__(self, endpoint: str) -> None:
        self.endpoint = endpoint
        self._connected = False

    async def __aenter__(self) -> "SequencingServiceClient":
        await asyncio.sleep(0.01)
        self._connected = True
        return self

    async def __aexit__(self, exc_type: object, exc_value: object, traceback: object) -> None:
        await asyncio.sleep(0.005)
        self._connected = False

    async def fetch_result(self, job_id: str) -> SequencingResult:
        """Time: O(1) plus simulated I/O delay. Raises RuntimeError if
        not connected (must be used within the async context manager)."""
        if not self._connected:
            raise RuntimeError("client is not connected")
        await asyncio.sleep(0.01)
        return SequencingResult(job_id=job_id, read_count=1_500_000)


class IndustryAsyncSyntax:
    """A clean asynchronous scientific data-processing component that
    fetches multiple sequencing job results concurrently through an
    async context-managed client connection - keeping I/O-bound network
    waiting off the CPU-bound processing path.
    """

    @staticmethod
    async def collect_results(job_ids: list[str], endpoint: str) -> list[SequencingResult]:
        """Time: O(max single-fetch latency) for the concurrent phase,
        Space: O(n) for the collected results.
        """
        async with SequencingServiceClient(endpoint) as client:
            results = await asyncio.gather(*(client.fetch_result(job_id) for job_id in job_ids))
        return list(results)

    @staticmethod
    def total_reads(results: list[SequencingResult]) -> int:
        """A CPU-bound aggregation step, deliberately kept synchronous
        since it does no I/O and gains nothing from async execution.

        Time: O(n)
        """
        return sum(result.read_count for result in results)

    @staticmethod
    async def _main() -> None:
        results = await IndustryAsyncSyntax.collect_results(
            ["JOB-1", "JOB-2", "JOB-3"], endpoint="sequencing-service.local"
        )
        for result in results:
            print("Industry:", result)
        print("Industry: total reads across jobs ->", IndustryAsyncSyntax.total_reads(results))

    @staticmethod
    def run() -> None:
        asyncio.run(IndustryAsyncSyntax._main())


if __name__ == "__main__":
    UniversityAsyncSyntax.run()
    InterviewAsyncSyntax.run()
    IndustryAsyncSyntax.run()
