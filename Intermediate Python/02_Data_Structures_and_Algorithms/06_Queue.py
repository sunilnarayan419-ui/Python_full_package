from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field


class UniversityQueue:
    """Basic FIFO queue demonstrated with laboratory sample processing order."""

    def __init__(self) -> None:
        self._items: list[str] = []

    def enqueue(self, item: str) -> None:
        """Time: O(1) amortized, Space: O(1)."""
        self._items.append(item)

    def dequeue(self) -> str:
        """Time: O(n) with a plain list (front removal shifts elements), Space: O(1)."""
        return self._items.pop(0)

    def peek_front(self) -> str:
        """Time: O(1), Space: O(1)."""
        return self._items[0]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    @staticmethod
    def run() -> None:
        queue = UniversityQueue()
        for sample in ["S001", "S002", "S003"]:
            queue.enqueue(sample)
        print("University: next to process ->", queue.peek_front())
        processed = queue.dequeue()
        print("University: processed ->", processed)
        print("University: is empty ->", queue.is_empty())


class QueueEmptyError(Exception):
    """Raised when dequeuing/peeking an empty queue."""


class InterviewQueue:
    """Efficient FIFO queue built on collections.deque, with explicit
    edge-case handling, used to process sequencing job requests."""

    def __init__(self) -> None:
        self._items: deque[str] = deque()

    def enqueue(self, job_id: str) -> None:
        """Time: O(1), Space: O(1)."""
        if not job_id:
            raise ValueError("job_id must not be empty")
        self._items.append(job_id)

    def dequeue(self) -> str:
        """Time: O(1), Space: O(1). Raises QueueEmptyError if empty."""
        if not self._items:
            raise QueueEmptyError("no jobs to dequeue")
        return self._items.popleft()

    def peek_front(self) -> str:
        """Time: O(1), Space: O(1). Raises QueueEmptyError if empty."""
        if not self._items:
            raise QueueEmptyError("no jobs queued")
        return self._items[0]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)

    @staticmethod
    def run() -> None:
        job_queue = InterviewQueue()
        try:
            job_queue.dequeue()
        except QueueEmptyError as error:
            print("Interview: edge case (empty) ->", error)

        for job in ["JOB-A", "JOB-B", "JOB-C"]:
            job_queue.enqueue(job)
        print("Interview: front job ->", job_queue.peek_front())
        print("Interview: processing order ->", end=" ")
        while not job_queue.is_empty():
            print(job_queue.dequeue(), end=" ")
        print()
        print("Interview: O(1) enqueue/dequeue via deque, vs O(n) for list-based front removal.")


@dataclass(slots=True)
class SequencingJob:
    job_id: str
    priority: str
    sample_count: int


class IndustryQueue:
    """A reusable scientific processing queue for a sequencing pipeline,
    backed by collections.deque for O(1) amortized enqueue/dequeue,
    with validation and capacity control suitable for production use.
    """

    def __init__(self, max_size: int | None = None) -> None:
        if max_size is not None and max_size <= 0:
            raise ValueError("max_size must be positive when provided")
        self._items: deque[SequencingJob] = deque()
        self._max_size = max_size

    def enqueue(self, job: SequencingJob) -> None:
        """Time: O(1), Space: O(1). Raises OverflowError if at capacity."""
        if job.sample_count <= 0:
            raise ValueError("sample_count must be positive")
        if self._max_size is not None and len(self._items) >= self._max_size:
            raise OverflowError(f"queue capacity of {self._max_size} exceeded")
        self._items.append(job)

    def dequeue(self) -> SequencingJob:
        """Time: O(1), Space: O(1). Raises QueueEmptyError if empty."""
        if not self._items:
            raise QueueEmptyError("no sequencing jobs pending")
        return self._items.popleft()

    def __len__(self) -> int:
        return len(self._items)

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def pending_job_ids(self) -> list[str]:
        """Time: O(n), Space: O(n)."""
        return [job.job_id for job in self._items]

    @staticmethod
    def run() -> None:
        pipeline = IndustryQueue(max_size=10)
        pipeline.enqueue(SequencingJob("JOB-101", priority="standard", sample_count=8))
        pipeline.enqueue(SequencingJob("JOB-102", priority="urgent", sample_count=2))
        pipeline.enqueue(SequencingJob("JOB-103", priority="standard", sample_count=5))

        print("Industry: pending jobs ->", pipeline.pending_job_ids())
        next_job = pipeline.dequeue()
        print(f"Industry: processing {next_job.job_id} ({next_job.sample_count} samples)")
        print("Industry: remaining ->", len(pipeline))


if __name__ == "__main__":
    UniversityQueue.run()
    InterviewQueue.run()
    IndustryQueue.run()
