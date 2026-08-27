from __future__ import annotations

from dataclasses import dataclass
from operator import attrgetter


class UniversitySorting:
    """Implements insertion sort manually to teach the mechanics of
    sorting a small list of lab sample pH readings."""

    def __init__(self, readings: list[float]) -> None:
        self.readings = readings

    def insertion_sort(self) -> list[float]:
        """Build up a sorted prefix by inserting each new element into
        its correct position among the already-sorted elements.

        Time: O(n^2) worst/average case, O(n) best case (nearly sorted)
        Space: O(1) auxiliary - sorts in place on a copy
        """
        values = self.readings.copy()
        for i in range(1, len(values)):
            key = values[i]
            j = i - 1
            while j >= 0 and values[j] > key:
                values[j + 1] = values[j]
                j -= 1
            values[j + 1] = key
        return values

    @staticmethod
    def run() -> None:
        demo = UniversitySorting([7.2, 6.8, 7.9, 6.5, 7.1])
        print("University: unsorted ->", demo.readings)
        print("University: insertion-sorted ->", demo.insertion_sort())


class InterviewSorting:
    """Implements and compares merge sort (guaranteed O(n log n)) and
    quicksort (average O(n log n)) over gene-expression fold-change
    values, exposing their trade-offs."""

    @staticmethod
    def merge_sort(values: list[float]) -> list[float]:
        """Divide-and-conquer, stable, guaranteed O(n log n).

        Time: O(n log n) worst, average, and best case
        Space: O(n) auxiliary for merge buffers
        """
        if len(values) <= 1:
            return values.copy()
        mid = len(values) // 2
        left = InterviewSorting.merge_sort(values[:mid])
        right = InterviewSorting.merge_sort(values[mid:])
        return InterviewSorting._merge(left, right)

    @staticmethod
    def _merge(left: list[float], right: list[float]) -> list[float]:
        merged: list[float] = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged

    @staticmethod
    def quicksort(values: list[float]) -> list[float]:
        """Partition around a pivot; average O(n log n), worst O(n^2)
        on already-sorted or adversarial input with a naive pivot choice.

        Time: O(n log n) average, O(n^2) worst case
        Space: O(log n) average recursion depth, O(n) worst case
        """
        if len(values) <= 1:
            return values.copy()
        pivot = values[len(values) // 2]
        less = [v for v in values if v < pivot]
        equal = [v for v in values if v == pivot]
        greater = [v for v in values if v > pivot]
        return InterviewSorting.quicksort(less) + equal + InterviewSorting.quicksort(greater)

    @staticmethod
    def run() -> None:
        fold_changes = [1.8, -2.3, 0.5, 3.1, -0.9, 2.2]
        print("Interview: unsorted ->", fold_changes)
        print("Interview: merge sort (guaranteed O(n log n)) ->", InterviewSorting.merge_sort(fold_changes))
        print("Interview: quicksort (average O(n log n)) ->", InterviewSorting.quicksort(fold_changes))
        print("Interview: merge sort is preferred when worst-case guarantees matter; "
              "quicksort is often faster in practice due to lower constant factors.")


@dataclass(slots=True)
class ExperimentResult:
    experiment_id: str
    p_value: float
    effect_size: float


class IndustrySorting:
    """Uses Python's production-grade Timsort (via sorted/list.sort)
    rather than a hand-rolled algorithm, since Timsort is highly
    optimized, stable, and already O(n log n) worst case with O(n)
    best case on partially-ordered real-world data.
    """

    @staticmethod
    def sort_by_significance(results: list[ExperimentResult]) -> list[ExperimentResult]:
        """Sort experiment results ascending by p-value (most significant first).

        Time: O(n log n), Space: O(n) for the new sorted list
        """
        return sorted(results, key=attrgetter("p_value"))

    @staticmethod
    def sort_by_multiple_keys(results: list[ExperimentResult]) -> list[ExperimentResult]:
        """Sort by p-value ascending, then by effect_size descending as a
        tiebreaker - demonstrates Timsort's stability and multi-key support.

        Time: O(n log n), Space: O(n)
        """
        return sorted(results, key=lambda r: (r.p_value, -r.effect_size))

    @staticmethod
    def sort_in_place_by_effect_size(results: list[ExperimentResult]) -> None:
        """In-place sort to avoid allocating a second list when the
        original ordering is no longer needed.

        Time: O(n log n), Space: O(n) auxiliary (Timsort's internal merge buffer)
        """
        results.sort(key=attrgetter("effect_size"), reverse=True)

    @staticmethod
    def run() -> None:
        results = [
            ExperimentResult("EXP-1", p_value=0.04, effect_size=1.2),
            ExperimentResult("EXP-2", p_value=0.001, effect_size=0.8),
            ExperimentResult("EXP-3", p_value=0.04, effect_size=2.5),
            ExperimentResult("EXP-4", p_value=0.09, effect_size=0.3),
        ]
        by_significance = IndustrySorting.sort_by_significance(results)
        print("Industry: by significance ->", [r.experiment_id for r in by_significance])

        by_multi_key = IndustrySorting.sort_by_multiple_keys(results)
        print("Industry: by p-value then effect size ->", [r.experiment_id for r in by_multi_key])

        IndustrySorting.sort_in_place_by_effect_size(results)
        print("Industry: in-place by effect size ->", [r.experiment_id for r in results])


if __name__ == "__main__":
    UniversitySorting.run()
    InterviewSorting.run()
    IndustrySorting.run()
