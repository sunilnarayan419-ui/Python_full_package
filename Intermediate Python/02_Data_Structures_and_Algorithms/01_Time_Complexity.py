from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass, field


class UniversityTimeComplexity:
    """Demonstrates fundamental Big-O time complexity classes using
    simple operations on a small dataset of plant heights (cm).

    Complexity is a description of how the number of operations grows
    with input size n. Python cannot measure Big-O directly; timing
    only approximates it, so these methods illustrate the *shape* of
    growth by counting operations, not by trusting wall-clock time.
    """

    def __init__(self, plant_heights: list[float]) -> None:
        self.plant_heights = plant_heights

    def constant_time_first_height(self) -> float:
        """Access the first recorded height.

        Time: O(1)
        Space: O(1)
        """
        return self.plant_heights[0]

    def linear_time_average_height(self) -> float:
        """Compute the average height by visiting every element once.

        Time: O(n)
        Space: O(1)
        """
        total = 0.0
        for height in self.plant_heights:
            total += height
        return total / len(self.plant_heights)

    def logarithmic_time_find_height(self, target: float) -> int:
        """Binary search for a height in a SORTED list.

        Time: O(log n)
        Space: O(1)
        """
        sorted_heights = sorted(self.plant_heights)
        low, high = 0, len(sorted_heights) - 1
        while low <= high:
            mid = (low + high) // 2
            if sorted_heights[mid] == target:
                return mid
            if sorted_heights[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        return -1

    def quadratic_time_pairwise_differences(self) -> list[float]:
        """Compute the difference between every pair of plant heights.

        Time: O(n^2)
        Space: O(n^2) for the output list
        """
        differences: list[float] = []
        for i in range(len(self.plant_heights)):
            for j in range(len(self.plant_heights)):
                differences.append(abs(self.plant_heights[i] - self.plant_heights[j]))
        return differences

    @staticmethod
    def run() -> None:
        heights = [12.5, 20.1, 9.3, 15.7, 30.2]
        demo = UniversityTimeComplexity(heights)
        print("University: first height (O(1)) ->", demo.constant_time_first_height())
        print("University: average height (O(n)) ->", round(demo.linear_time_average_height(), 2))
        print("University: index of 15.7 (O(log n)) ->", demo.logarithmic_time_find_height(15.7))
        print("University: pairwise diffs count (O(n^2)) ->", len(demo.quadratic_time_pairwise_differences()))


class InterviewTimeComplexity:
    """Compares multiple approaches to the same interview-style problem
    and identifies the asymptotically optimal one.

    Problem: given gene expression readings, find whether any two
    readings sum to a target threshold value.
    """

    @staticmethod
    def has_pair_sum_brute_force(readings: list[float], target: float) -> bool:
        """Check every pair explicitly.

        Time: O(n^2)
        Space: O(1)
        """
        n = len(readings)
        for i in range(n):
            for j in range(i + 1, n):
                if readings[i] + readings[j] == target:
                    return True
        return False

    @staticmethod
    def has_pair_sum_optimal(readings: list[float], target: float) -> bool:
        """Use a hash set of seen complements for a single pass.

        Time: O(n) average
        Space: O(n)
        """
        seen: set[float] = set()
        for value in readings:
            complement = target - value
            if complement in seen:
                return True
            seen.add(value)
        return False

    @classmethod
    def compare_approaches(cls, readings: list[float], target: float) -> dict[str, bool]:
        """Run both approaches and confirm they agree.

        Time: O(n^2) dominated by the brute-force call
        Space: O(n)
        """
        if not readings:
            return {"brute_force": False, "optimal": False}
        return {
            "brute_force": cls.has_pair_sum_brute_force(readings, target),
            "optimal": cls.has_pair_sum_optimal(readings, target),
        }

    @staticmethod
    def run() -> None:
        readings = [2.1, 5.4, 7.9, 3.3, 1.0]
        target = 8.7
        result = InterviewTimeComplexity.compare_approaches(readings, target)
        print(f"Interview: brute force O(n^2) result -> {result['brute_force']}")
        print(f"Interview: optimal O(n) result -> {result['optimal']}")
        print("Interview: optimal approach preferred for large expression datasets.")


@dataclass
class ComplexityBenchmark:
    label: str
    input_size: int
    elapsed_seconds: float


class IndustryTimeComplexity:
    """A small algorithm-analysis component for a scientific pipeline
    that empirically benchmarks candidate search strategies over
    genomic marker datasets before one is selected for production use.

    This does not claim to derive exact Big-O from timings; it reports
    observed elapsed time across growing input sizes so an engineer can
    sanity-check theoretical complexity against real behaviour.
    """

    def __init__(self) -> None:
        self._benchmarks: list[ComplexityBenchmark] = []

    @staticmethod
    def _linear_marker_search(markers: list[str], marker_id: str) -> bool:
        """Time: O(n), Space: O(1)."""
        return marker_id in markers

    @staticmethod
    def _hashed_marker_search(marker_index: set[str], marker_id: str) -> bool:
        """Time: O(1) average, Space: O(n) for the index."""
        return marker_id in marker_index

    def benchmark_strategy(
        self,
        label: str,
        strategy: Callable[[], object],
    ) -> ComplexityBenchmark:
        """Time a single callable invocation and record the result.

        Time: dominated by the callable itself
        Space: O(1) beyond the callable's own usage
        """
        start = time.perf_counter()
        strategy()
        elapsed = time.perf_counter() - start
        benchmark = ComplexityBenchmark(label=label, input_size=-1, elapsed_seconds=elapsed)
        self._benchmarks.append(benchmark)
        return benchmark

    def compare_marker_lookup(self, markers: list[str], marker_id: str) -> dict[str, float]:
        """Benchmark linear vs. hashed marker lookup on the same dataset.

        Time: O(n) to build results (dominated by the linear scan)
        Space: O(n) for the hashed index
        """
        marker_index = set(markers)
        linear_result = self.benchmark_strategy(
            "linear_scan", lambda: self._linear_marker_search(markers, marker_id)
        )
        hashed_result = self.benchmark_strategy(
            "hashed_lookup", lambda: self._hashed_marker_search(marker_index, marker_id)
        )
        return {
            linear_result.label: linear_result.elapsed_seconds,
            hashed_result.label: hashed_result.elapsed_seconds,
        }

    @staticmethod
    def run() -> None:
        markers = [f"MRK{i:05d}" for i in range(20_000)]
        analyzer = IndustryTimeComplexity()
        timings = analyzer.compare_marker_lookup(markers, "MRK19999")
        print("Industry: marker lookup timings (seconds):")
        for label, seconds in timings.items():
            print(f"  {label}: {seconds:.8f}")
        print("Industry: hashed lookup scales O(1) average; linear scan scales O(n).")


if __name__ == "__main__":
    UniversityTimeComplexity.run()
    InterviewTimeComplexity.run()
    IndustryTimeComplexity.run()
