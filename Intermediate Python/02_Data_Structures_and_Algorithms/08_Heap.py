from __future__ import annotations

import heapq
from dataclasses import dataclass, field


class UniversityHeap:
    """Basic min-heap demonstration using heapq over drug candidate
    binding-affinity scores (lower score = stronger binding = higher priority)."""

    def __init__(self) -> None:
        self._heap: list[float] = []

    def push(self, score: float) -> None:
        """Time: O(log n), Space: O(1)."""
        heapq.heappush(self._heap, score)

    def pop_min(self) -> float:
        """Time: O(log n), Space: O(1)."""
        return heapq.heappop(self._heap)

    def peek_min(self) -> float:
        """Time: O(1), Space: O(1)."""
        return self._heap[0]

    @staticmethod
    def run() -> None:
        heap = UniversityHeap()
        for score in [4.2, 1.1, 3.7, 0.9, 2.5]:
            heap.push(score)
        print("University: best (lowest) binding score ->", heap.peek_min())
        print("University: processing order (best first) ->", end=" ")
        while heap._heap:
            print(heap.pop_min(), end=" ")
        print()


@dataclass(order=True)
class _RankedResult:
    sort_score: float
    label: str = field(compare=False)


class InterviewHeap:
    """Solves the classic top-k problem: given many experimental
    p-values, find the k most statistically significant (smallest)
    results using a bounded max-heap for O(n log k) instead of O(n log n).
    """

    @staticmethod
    def top_k_significant(results: dict[str, float], k: int) -> list[tuple[str, float]]:
        """Return the k results with the smallest p-values.

        Time: O(n log k), Space: O(k)

        Uses a max-heap of size k (via negation) so we only ever hold k
        elements, which is more efficient than sorting all n results
        when k is much smaller than n.
        """
        if k <= 0 or not results:
            return []
        max_heap: list[_RankedResult] = []
        for label, p_value in results.items():
            candidate = _RankedResult(sort_score=-p_value, label=label)
            if len(max_heap) < k:
                heapq.heappush(max_heap, candidate)
            elif candidate.sort_score > max_heap[0].sort_score:
                heapq.heapreplace(max_heap, candidate)
        ranked = sorted(max_heap, key=lambda r: -r.sort_score)
        return [(r.label, -r.sort_score) for r in ranked]

    @staticmethod
    def run() -> None:
        p_values = {
            "gene_A": 0.041,
            "gene_B": 0.003,
            "gene_C": 0.211,
            "gene_D": 0.0007,
            "gene_E": 0.089,
        }
        top_3 = InterviewHeap.top_k_significant(p_values, 3)
        print("Interview: top 3 most significant genes (O(n log k)) ->", top_3)
        print("Interview: naive alternative would sort all n results in O(n log n).")


@dataclass(order=True)
class _PriorityJob:
    sort_key: float
    job_id: str = field(compare=False)
    urgency: str = field(compare=False)


class IndustryHeap:
    """A reusable priority-processing component for a lab job scheduler,
    where lower urgency numbers are processed first (min-heap semantics),
    built on heapq for production-grade O(log n) push/pop.
    """

    def __init__(self) -> None:
        self._heap: list[_PriorityJob] = []
        self._counter = 0  # tie-breaker to keep insertion order stable

    def schedule(self, job_id: str, priority: float, urgency: str) -> None:
        """Time: O(log n), Space: O(1).

        Raises ValueError for invalid priority.
        """
        if priority < 0:
            raise ValueError("priority must be non-negative")
        heapq.heappush(self._heap, _PriorityJob(sort_key=priority, job_id=job_id, urgency=urgency))
        self._counter += 1

    def process_next(self) -> _PriorityJob:
        """Pop and return the highest-priority (lowest sort_key) job.

        Time: O(log n), Space: O(1)
        Raises IndexError if no jobs remain.
        """
        if not self._heap:
            raise IndexError("no jobs scheduled")
        return heapq.heappop(self._heap)

    def peek_next(self) -> _PriorityJob:
        """Time: O(1), Space: O(1)."""
        if not self._heap:
            raise IndexError("no jobs scheduled")
        return self._heap[0]

    def __len__(self) -> int:
        return len(self._heap)

    @staticmethod
    def run() -> None:
        scheduler = IndustryHeap()
        scheduler.schedule("JOB-A", priority=3.0, urgency="normal")
        scheduler.schedule("JOB-B", priority=1.0, urgency="critical")
        scheduler.schedule("JOB-C", priority=2.0, urgency="high")

        print("Industry: next job ->", scheduler.peek_next().job_id)
        print("Industry: processing order ->", end=" ")
        while len(scheduler) > 0:
            job = scheduler.process_next()
            print(f"{job.job_id}({job.urgency})", end=" ")
        print()


if __name__ == "__main__":
    UniversityHeap.run()
    InterviewHeap.run()
    IndustryHeap.run()
