from __future__ import annotations

from dataclasses import dataclass


class UniversityBacktracking:
    """Demonstrates the choose-explore-undo backtracking pattern by
    generating all possible experimental treatment combinations from a
    small set of reagents."""

    def generate_combinations(self, reagents: list[str]) -> list[list[str]]:
        """Generate all subsets of reagents using choose/explore/undo.

        Time: O(2^n), Space: O(2^n) for the output, O(n) call stack
        """
        results: list[list[str]] = []
        current: list[str] = []

        def backtrack(start_index: int) -> None:
            results.append(current.copy())
            for i in range(start_index, len(reagents)):
                current.append(reagents[i])          # choose
                backtrack(i + 1)                       # explore
                current.pop()                          # undo

        backtrack(0)
        return results

    @staticmethod
    def run() -> None:
        demo = UniversityBacktracking()
        combos = demo.generate_combinations(["ReagentA", "ReagentB", "ReagentC"])
        print("University: all reagent combinations ->", combos)


class InterviewBacktracking:
    """Solves a standard constrained-search interview problem: select a
    subset of gene expression values that sum exactly to a target
    threshold (subset-sum), with pruning for efficiency."""

    @staticmethod
    def find_subset_summing_to(values: list[float], target: float) -> list[float] | None:
        """Backtrack over inclusion/exclusion decisions, pruning branches
        whose running sum already exceeds the target (assumes non-negative
        values, which is valid for expression magnitudes).

        Time: O(2^n) worst case, pruned in practice
        Space: O(n) call stack and current-path storage
        """
        if not values:
            return [] if target == 0 else None

        sorted_values = sorted(values)
        chosen: list[float] = []

        def backtrack(index: int, running_sum: float) -> bool:
            if abs(running_sum - target) < 1e-9:
                return True
            if index == len(sorted_values) or running_sum > target:
                return False
            # Choose: include sorted_values[index]
            chosen.append(sorted_values[index])
            if backtrack(index + 1, running_sum + sorted_values[index]):
                return True
            chosen.pop()  # undo
            # Explore excluding this value
            return backtrack(index + 1, running_sum)

        found = backtrack(0, 0.0)
        return chosen if found else None

    @staticmethod
    def run() -> None:
        values = [2.5, 4.0, 1.5, 3.0, 6.0]
        result = InterviewBacktracking.find_subset_summing_to(values, 8.5)
        print("Interview: subset summing to 8.5 ->", result)

        no_result = InterviewBacktracking.find_subset_summing_to(values, 100.0)
        print("Interview: subset summing to 100.0 (impossible) ->", no_result)

        print("Interview: empty input edge case ->", InterviewBacktracking.find_subset_summing_to([], 0.0))


@dataclass(slots=True, frozen=True)
class SampleConstraint:
    sample_id: str
    compatible_with: frozenset[str]


class IndustryBacktracking:
    """Implements a constrained sample-selection solver with practical
    pruning: select the largest possible set of samples such that every
    pair of chosen samples is pairwise compatible (e.g. for a combined
    assay run), without unnecessary complexity beyond validation and
    pruning that meaningfully reduce the search space.
    """

    @staticmethod
    def select_max_compatible_samples(constraints: list[SampleConstraint]) -> list[str]:
        """Backtrack over candidate samples, pruning any candidate that
        is incompatible with an already-chosen sample before recursing.

        Time: O(2^n) worst case, substantially pruned by compatibility
        checks in realistic constraint sets
        Space: O(n) call stack and current-selection storage
        """
        if not constraints:
            return []

        constraint_lookup = {c.sample_id: c for c in constraints}
        sample_ids = [c.sample_id for c in constraints]
        best_selection: list[str] = []
        current_selection: list[str] = []

        def is_compatible_with_current(candidate_id: str) -> bool:
            candidate = constraint_lookup[candidate_id]
            return all(
                chosen_id in candidate.compatible_with
                for chosen_id in current_selection
            )

        def backtrack(start_index: int) -> None:
            nonlocal best_selection
            if len(current_selection) > len(best_selection):
                best_selection = current_selection.copy()
            for i in range(start_index, len(sample_ids)):
                candidate_id = sample_ids[i]
                if not is_compatible_with_current(candidate_id):
                    continue  # prune incompatible branch
                current_selection.append(candidate_id)     # choose
                backtrack(i + 1)                             # explore
                current_selection.pop()                      # undo

        backtrack(0)
        return best_selection

    @staticmethod
    def run() -> None:
        constraints = [
            SampleConstraint("S1", frozenset({"S2", "S3"})),
            SampleConstraint("S2", frozenset({"S1", "S3"})),
            SampleConstraint("S3", frozenset({"S1", "S2"})),
            SampleConstraint("S4", frozenset()),  # incompatible with everything
        ]
        best_group = IndustryBacktracking.select_max_compatible_samples(constraints)
        print("Industry: largest pairwise-compatible sample group ->", best_group)


if __name__ == "__main__":
    UniversityBacktracking.run()
    InterviewBacktracking.run()
    IndustryBacktracking.run()
