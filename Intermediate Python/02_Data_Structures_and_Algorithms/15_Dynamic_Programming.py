from __future__ import annotations

from dataclasses import dataclass


class UniversityDynamicProgramming:
    """Demonstrates memoization vs. tabulation on a simple example:
    the number of distinct ways to reach a target dosage (mg) using
    available tablet sizes, where order does not matter (unbounded
    knapsack-style counting), shown here in its simplest 1D form:
    the classic staircase / climbing-doses problem.
    """

    def ways_memoized(self, target_steps: int, cache: dict[int, int] | None = None) -> int:
        """Number of ways to climb target_steps taking 1 or 2 steps at a time.

        State: ways(n) = ways(n-1) + ways(n-2)
        Time: O(n) with memoization vs O(2^n) naive recursion
        Space: O(n) for cache and call stack
        """
        if cache is None:
            cache = {}
        if target_steps < 0:
            return 0
        if target_steps in (0, 1):
            return 1
        if target_steps in cache:
            return cache[target_steps]
        cache[target_steps] = self.ways_memoized(target_steps - 1, cache) + self.ways_memoized(target_steps - 2, cache)
        return cache[target_steps]

    def ways_tabulated(self, target_steps: int) -> int:
        """Bottom-up tabulation building the same result iteratively.

        Time: O(n), Space: O(n) for the table
        """
        if target_steps < 0:
            return 0
        table = [0] * (target_steps + 1)
        table[0] = 1
        if target_steps >= 1:
            table[1] = 1
        for step in range(2, target_steps + 1):
            table[step] = table[step - 1] + table[step - 2]
        return table[target_steps]

    @staticmethod
    def run() -> None:
        demo = UniversityDynamicProgramming()
        print("University: ways (memoized) for 6 steps ->", demo.ways_memoized(6))
        print("University: ways (tabulated) for 6 steps ->", demo.ways_tabulated(6))


class InterviewDynamicProgramming:
    """Solves the classic longest common subsequence (LCS) problem on
    two DNA sequences, with clear state definition and transitions."""

    @staticmethod
    def longest_common_subsequence(sequence_a: str, sequence_b: str) -> int:
        """State: dp[i][j] = LCS length of sequence_a[:i] and sequence_b[:j]

        Transition:
          if sequence_a[i-1] == sequence_b[j-1]: dp[i][j] = dp[i-1][j-1] + 1
          else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])

        Time: O(m * n), Space: O(m * n)
        """
        if not sequence_a or not sequence_b:
            return 0
        m, n = len(sequence_a), len(sequence_b)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if sequence_a[i - 1] == sequence_b[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        return dp[m][n]

    @staticmethod
    def longest_common_subsequence_space_optimized(sequence_a: str, sequence_b: str) -> int:
        """Same LCS length using only two rolling rows instead of a full table.

        Time: O(m * n), Space: O(min(m, n))
        """
        if not sequence_a or not sequence_b:
            return 0
        if len(sequence_a) < len(sequence_b):
            sequence_a, sequence_b = sequence_b, sequence_a
        previous = [0] * (len(sequence_b) + 1)
        for char_a in sequence_a:
            current = [0] * (len(sequence_b) + 1)
            for j, char_b in enumerate(sequence_b, start=1):
                if char_a == char_b:
                    current[j] = previous[j - 1] + 1
                else:
                    current[j] = max(previous[j], current[j - 1])
            previous = current
        return previous[-1]

    @staticmethod
    def run() -> None:
        seq_a, seq_b = "GACGTACG", "GTCGTCAG"
        full_table_result = InterviewDynamicProgramming.longest_common_subsequence(seq_a, seq_b)
        optimized_result = InterviewDynamicProgramming.longest_common_subsequence_space_optimized(seq_a, seq_b)
        print(f"Interview: LCS length ({seq_a}, {seq_b}) full table ->", full_table_result)
        print(f"Interview: LCS length space-optimized ->", optimized_result)
        print("Interview: empty-sequence edge case ->", InterviewDynamicProgramming.longest_common_subsequence("", "ACGT"))


@dataclass(slots=True, frozen=True)
class LabTask:
    task_id: str
    duration_minutes: int
    value_score: float


class IndustryDynamicProgramming:
    """A 0/1 knapsack-style resource-allocation solver: given a fixed
    instrument-time budget, select the subset of lab tasks maximizing
    total value score without exceeding the time budget. This models a
    realistic scientific scheduling optimization problem.
    """

    @staticmethod
    def maximize_value_within_budget(tasks: list[LabTask], time_budget_minutes: int) -> tuple[float, list[str]]:
        """State: dp[i][t] = best achievable value using the first i tasks
        with t minutes of budget remaining.

        Transition: for each task, either skip it or take it (if it fits)
          dp[i][t] = max(dp[i-1][t], dp[i-1][t-duration] + value) if it fits
                   = dp[i-1][t] otherwise

        Time: O(n * budget), Space: O(n * budget)

        Returns the best achievable value and the list of selected task IDs.
        """
        if time_budget_minutes < 0:
            raise ValueError("time_budget_minutes must be non-negative")
        if not tasks:
            return 0.0, []

        n = len(tasks)
        dp = [[0.0] * (time_budget_minutes + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            task = tasks[i - 1]
            for t in range(time_budget_minutes + 1):
                dp[i][t] = dp[i - 1][t]
                if task.duration_minutes <= t:
                    candidate = dp[i - 1][t - task.duration_minutes] + task.value_score
                    if candidate > dp[i][t]:
                        dp[i][t] = candidate

        # Backtrack to recover which tasks were selected.
        selected: list[str] = []
        remaining_budget = time_budget_minutes
        for i in range(n, 0, -1):
            if dp[i][remaining_budget] != dp[i - 1][remaining_budget]:
                task = tasks[i - 1]
                selected.append(task.task_id)
                remaining_budget -= task.duration_minutes
        selected.reverse()

        return dp[n][time_budget_minutes], selected

    @staticmethod
    def run() -> None:
        tasks = [
            LabTask("PCR_RUN", duration_minutes=45, value_score=8.0),
            LabTask("SEQ_PREP", duration_minutes=30, value_score=6.5),
            LabTask("MICROSCOPY", duration_minutes=20, value_score=4.0),
            LabTask("ASSAY_SETUP", duration_minutes=60, value_score=9.5),
        ]
        best_value, selected = IndustryDynamicProgramming.maximize_value_within_budget(tasks, time_budget_minutes=90)
        print(f"Industry: best achievable value within 90-minute budget -> {best_value}")
        print("Industry: selected tasks ->", selected)


if __name__ == "__main__":
    UniversityDynamicProgramming.run()
    InterviewDynamicProgramming.run()
    IndustryDynamicProgramming.run()
