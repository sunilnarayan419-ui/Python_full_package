from __future__ import annotations

import sys
from dataclasses import dataclass, field


class UniversityRecursion:
    """Demonstrates base case / recursive case using recursive
    computation of bacterial population growth under doubling."""

    def population_after_generations(self, initial_population: int, generations: int) -> int:
        """Population doubles each generation.

        Base case: generations == 0 -> return initial_population
        Recursive case: double the result of one fewer generation

        Time: O(n), Space: O(n) call stack depth
        """
        if generations < 0:
            raise ValueError("generations must be non-negative")
        if generations == 0:
            return initial_population
        return 2 * self.population_after_generations(initial_population, generations - 1)

    def sum_of_readings(self, readings: list[float]) -> float:
        """Recursively sum a list of readings.

        Base case: empty list -> 0
        Recursive case: first element + sum of the rest

        Time: O(n), Space: O(n) call stack depth
        """
        if not readings:
            return 0.0
        return readings[0] + self.sum_of_readings(readings[1:])

    @staticmethod
    def run() -> None:
        demo = UniversityRecursion()
        print("University: population after 5 generations (start=100) ->",
              demo.population_after_generations(100, 5))
        print("University: recursive sum of readings ->", demo.sum_of_readings([1.5, 2.5, 3.0, 4.0]))


class InterviewRecursion:
    """Solves a classic recursive interview problem: generating all
    valid combinations of experimental conditions from a set, with
    correct base-case handling for empty input."""

    @staticmethod
    def generate_condition_subsets(conditions: list[str]) -> list[list[str]]:
        """Generate every subset (the power set) of experimental conditions.

        Base case: no conditions left to decide on -> yield the current subset
        Recursive case: branch on including vs excluding the next condition

        Time: O(2^n), Space: O(2^n) for all subsets, O(n) call stack depth
        """
        results: list[list[str]] = []

        def backtrack(index: int, current: list[str]) -> None:
            if index == len(conditions):
                results.append(current.copy())
                return
            # Exclude the current condition
            backtrack(index + 1, current)
            # Include the current condition
            current.append(conditions[index])
            backtrack(index + 1, current)
            current.pop()

        backtrack(0, [])
        return results

    @staticmethod
    def fibonacci_memoized(n: int, cache: dict[int, int] | None = None) -> int:
        """Fibonacci sequence used to model idealized unconstrained
        population growth, with memoization to avoid the exponential
        blowup of naive recursion.

        Time: O(n) with memoization vs O(2^n) naive
        Space: O(n) for the cache and call stack
        """
        if n < 0:
            raise ValueError("n must be non-negative")
        if cache is None:
            cache = {}
        if n in (0, 1):
            return n
        if n in cache:
            return cache[n]
        cache[n] = InterviewRecursion.fibonacci_memoized(n - 1, cache) + InterviewRecursion.fibonacci_memoized(n - 2, cache)
        return cache[n]

    @staticmethod
    def run() -> None:
        subsets = InterviewRecursion.generate_condition_subsets(["heat", "light", "nutrient"])
        print("Interview: all condition subsets ->", subsets)
        print("Interview: empty input (edge case) ->", InterviewRecursion.generate_condition_subsets([]))
        print("Interview: fibonacci(20) memoized ->", InterviewRecursion.fibonacci_memoized(20))


@dataclass(slots=True)
class TaxonomyNode:
    name: str
    children: list["TaxonomyNode"] = field(default_factory=list)


class IndustryRecursion:
    """Uses recursion where it naturally fits (traversing a bounded
    biological taxonomy tree) and deliberately avoids recursion for
    processing large flat sequences, using iteration instead to avoid
    Python's recursion-depth limits in production.
    """

    @staticmethod
    def count_species(node: TaxonomyNode) -> int:
        """Recursively count leaf species nodes in a taxonomy tree.
        Appropriate here because taxonomy depth is naturally small and
        bounded (a handful of ranks), so stack depth is not a concern.

        Time: O(n), Space: O(h) call stack where h is tree height
        """
        if not node.children:
            return 1
        return sum(IndustryRecursion.count_species(child) for child in node.children)

    @staticmethod
    def cumulative_read_counts_iterative(read_counts: list[int]) -> list[int]:
        """Compute a running total over a potentially very large list of
        sequencing read counts using iteration rather than recursion,
        since a naive recursive version would risk hitting Python's
        recursion limit (sys.getrecursionlimit()) on large datasets.

        Time: O(n), Space: O(n) for the output list
        """
        cumulative: list[int] = []
        running_total = 0
        for count in read_counts:
            running_total += count
            cumulative.append(running_total)
        return cumulative

    @staticmethod
    def run() -> None:
        taxonomy = TaxonomyNode(
            "Plantae",
            children=[
                TaxonomyNode("Angiosperms", children=[TaxonomyNode("Rosaceae"), TaxonomyNode("Fabaceae")]),
                TaxonomyNode("Gymnosperms", children=[TaxonomyNode("Pinaceae")]),
            ],
        )
        print("Industry: species count (recursive, bounded depth) ->", IndustryRecursion.count_species(taxonomy))

        large_read_counts = list(range(1, 50_000))
        cumulative = IndustryRecursion.cumulative_read_counts_iterative(large_read_counts)
        print(
            "Industry: cumulative read counts (iterative, avoids recursion-depth risk) ->",
            f"first={cumulative[0]}, last={cumulative[-1]}, count={len(cumulative)}",
        )
        print(f"Industry: sys recursion limit for reference -> {sys.getrecursionlimit()}")


if __name__ == "__main__":
    UniversityRecursion.run()
    InterviewRecursion.run()
    IndustryRecursion.run()
