from __future__ import annotations

import sys
import time
from functools import lru_cache
from typing import Callable, TypeVar

T = TypeVar("T")


class RecursiveEditDistanceWorkflow:
    """Demonstrates lru_cache on overlapping recursive sequence-alignment subproblems.

    Workload: recursive (Levenshtein) edit distance between two biological
    sequences, computed naively without memoization and again with
    functools.lru_cache, illustrating exponential-to-polynomial collapse
    from memoizing overlapping subproblems.
    """

    def __init__(self, sequence_a: str, sequence_b: str, maxsize: int = 4096) -> None:
        if not sequence_a or not sequence_b:
            raise ValueError("sequence_a and sequence_b must be non-empty")
        self.sequence_a = sequence_a
        self.sequence_b = sequence_b
        self.maxsize = maxsize
        self._cached_edit_distance = lru_cache(maxsize=maxsize)(self._edit_distance_recursive_uncached)

    def _edit_distance_recursive_uncached(self, i: int, j: int) -> int:
        if i == 0:
            return j
        if j == 0:
            return i
        cost_substitute = 0 if self.sequence_a[i - 1] == self.sequence_b[j - 1] else 1
        return min(
            self._edit_distance_recursive_uncached(i - 1, j) + 1,
            self._edit_distance_recursive_uncached(i, j - 1) + 1,
            self._edit_distance_recursive_uncached(i - 1, j - 1) + cost_substitute,
        )

    def edit_distance_naive(self) -> int:
        sys.setrecursionlimit(max(sys.getrecursionlimit(), len(self.sequence_a) + len(self.sequence_b) + 100))
        return self._edit_distance_recursive_uncached(len(self.sequence_a), len(self.sequence_b))

    def _edit_distance_cached(self, i: int, j: int) -> int:
        if i == 0:
            return j
        if j == 0:
            return i
        cost_substitute = 0 if self.sequence_a[i - 1] == self.sequence_b[j - 1] else 1
        return min(
            self._cached_edit_distance_dispatch(i - 1, j) + 1,
            self._cached_edit_distance_dispatch(i, j - 1) + 1,
            self._cached_edit_distance_dispatch(i - 1, j - 1) + cost_substitute,
        )

    def _cached_edit_distance_dispatch(self, i: int, j: int) -> int:
        return self._memoized(i, j)

    def edit_distance_lru(self) -> int:
        sys.setrecursionlimit(max(sys.getrecursionlimit(), len(self.sequence_a) + len(self.sequence_b) + 100))
        self._memoized = lru_cache(maxsize=self.maxsize)(self._edit_distance_cached)
        return self._memoized(len(self.sequence_a), len(self.sequence_b))

    def cache_info(self) -> str:
        return str(self._memoized.cache_info())

    def clear_cache(self) -> None:
        self._memoized.cache_clear()

    def benchmark(self, function: Callable[..., T], *args: object, **kwargs: object) -> tuple[T, float]:
        start = time.perf_counter()
        result = function(*args, **kwargs)
        elapsed = time.perf_counter() - start
        return result, elapsed

    @staticmethod
    def run() -> None:
        sequence_a = "GATTACAGA"
        sequence_b = "GACTATACG"
        workflow = RecursiveEditDistanceWorkflow(sequence_a, sequence_b, maxsize=2048)

        naive_result, naive_elapsed = workflow.benchmark(workflow.edit_distance_naive)
        print(f"naive recursive: distance={naive_result}, elapsed={naive_elapsed:.6f}s")

        lru_result, lru_elapsed = workflow.benchmark(workflow.edit_distance_lru)
        print(f"lru_cache recursive: distance={lru_result}, elapsed={lru_elapsed:.6f}s")

        if naive_result != lru_result:
            raise RuntimeError("Optimized implementation changed the numerical result.")

        print(f"cache_info: {workflow.cache_info()}")

        # Re-run with a warm cache to demonstrate cache hits.
        _, warm_elapsed = workflow.benchmark(workflow._memoized, len(sequence_a), len(sequence_b))
        print(f"warm cache re-query: elapsed={warm_elapsed:.6f}s")
        print(f"cache_info after warm query: {workflow.cache_info()}")

        workflow.clear_cache()
        print(f"cache_info after clear: {workflow.cache_info()}")

        speedup = naive_elapsed / lru_elapsed if lru_elapsed > 0 else float("inf")
        print(f"speedup: {speedup:.2f}x")


if __name__ == "__main__":
    RecursiveEditDistanceWorkflow.run()
