from __future__ import annotations

from dataclasses import dataclass


class UniversityGreedyAlgorithms:
    """Demonstrates the greedy choice property using coin-change-style
    dosage assembly: greedily pick the largest available tablet size
    that fits, at each step."""

    def assemble_dosage_greedy(self, target_mg: float, available_tablets_mg: list[float]) -> list[float]:
        """Greedily select the largest tablet that fits the remaining dosage.

        Time: O(n log n) for sorting + O(n) selection, Space: O(n) for the result

        Note: this greedy approach works correctly only when tablet sizes
        form a "canonical" system (like standard coin denominations); it
        is not guaranteed optimal for arbitrary tablet size sets.
        """
        remaining = target_mg
        sizes = sorted(available_tablets_mg, reverse=True)
        chosen: list[float] = []
        for size in sizes:
            while remaining >= size:
                chosen.append(size)
                remaining -= size
        return chosen

    @staticmethod
    def run() -> None:
        demo = UniversityGreedyAlgorithms()
        tablets = [50.0, 25.0, 10.0, 5.0]
        result = demo.assemble_dosage_greedy(85.0, tablets)
        print("University: tablets chosen for 85mg ->", result, "total ->", sum(result))


class InterviewGreedyAlgorithms:
    """Implements and justifies a greedy strategy for the classic
    activity-selection problem: scheduling the maximum number of
    non-overlapping instrument time slots for experiments."""

    @staticmethod
    def select_max_experiments(
        experiments: list[tuple[str, float, float]]
    ) -> list[str]:
        """Each experiment is (experiment_id, start_time, end_time).
        Greedily pick the experiment that finishes earliest at each
        step, then skip any experiment overlapping it.

        Time: O(n log n) for the sort, O(n) for the scan
        Space: O(n) for the result

        Justification: sorting by earliest finish time and always
        taking the next non-conflicting activity is provably optimal
        for maximizing the count of non-overlapping intervals - taking
        the earliest-finishing option always leaves at least as much
        room for future choices as any other valid choice.
        """
        if not experiments:
            return []
        sorted_experiments = sorted(experiments, key=lambda e: e[2])
        selected: list[str] = [sorted_experiments[0][0]]
        last_end_time = sorted_experiments[0][2]
        for experiment_id, start_time, end_time in sorted_experiments[1:]:
            if start_time >= last_end_time:
                selected.append(experiment_id)
                last_end_time = end_time
        return selected

    @staticmethod
    def run() -> None:
        experiments = [
            ("EXP-A", 9.0, 10.5),
            ("EXP-B", 10.0, 11.0),
            ("EXP-C", 11.0, 12.0),
            ("EXP-D", 9.5, 13.0),
            ("EXP-E", 12.5, 14.0),
        ]
        selected = InterviewGreedyAlgorithms.select_max_experiments(experiments)
        print("Interview: max non-overlapping experiments scheduled ->", selected)
        print("Interview: empty input (edge case) ->", InterviewGreedyAlgorithms.select_max_experiments([]))


@dataclass(slots=True, frozen=True)
class SequencingJob:
    job_id: str
    processing_minutes: float
    deadline_minutes: float
    priority_weight: float


class IndustryGreedyAlgorithms:
    """Applies a greedy weighted-scheduling heuristic to order
    sequencing jobs on a single machine to minimize weighted completion
    time, a realistic lab-workflow scheduling scenario.

    Important limitation documented explicitly: this greedy strategy
    (shortest weighted processing time first) is provably optimal for
    minimizing total weighted completion time on a single machine with
    no deadlines, but it does NOT guarantee deadline satisfaction or
    optimality for other objectives (e.g. minimizing lateness) - not
    every scheduling optimization problem has a greedy-optimal solution.
    """

    @staticmethod
    def schedule_by_weighted_shortest_processing_time(jobs: list[SequencingJob]) -> list[str]:
        """Order jobs by processing_minutes / priority_weight ascending,
        which greedily minimizes total weighted completion time.

        Time: O(n log n), Space: O(n)
        """
        if not jobs:
            return []
        ordered = sorted(jobs, key=lambda job: job.processing_minutes / job.priority_weight)
        return [job.job_id for job in ordered]

    @staticmethod
    def estimate_missed_deadlines(jobs: list[SequencingJob], schedule_order: list[str]) -> list[str]:
        """Given a greedy schedule order, report which jobs would miss
        their deadlines - demonstrating that the greedy weighted-time
        schedule is not deadline-aware and may need a different
        algorithm (e.g. Earliest Deadline First) when deadlines matter.

        Time: O(n), Space: O(n)
        """
        job_lookup = {job.job_id: job for job in jobs}
        missed: list[str] = []
        elapsed = 0.0
        for job_id in schedule_order:
            job = job_lookup[job_id]
            elapsed += job.processing_minutes
            if elapsed > job.deadline_minutes:
                missed.append(job_id)
        return missed

    @staticmethod
    def run() -> None:
        jobs = [
            SequencingJob("SEQ-1", processing_minutes=30, deadline_minutes=40, priority_weight=2.0),
            SequencingJob("SEQ-2", processing_minutes=10, deadline_minutes=15, priority_weight=1.0),
            SequencingJob("SEQ-3", processing_minutes=20, deadline_minutes=90, priority_weight=1.5),
        ]
        schedule = IndustryGreedyAlgorithms.schedule_by_weighted_shortest_processing_time(jobs)
        print("Industry: greedy weighted schedule order ->", schedule)

        missed = IndustryGreedyAlgorithms.estimate_missed_deadlines(jobs, schedule)
        print("Industry: jobs that would miss their deadline under this greedy order ->", missed)
        print("Industry: note - greedy minimizes weighted completion time, not deadline adherence.")


if __name__ == "__main__":
    UniversityGreedyAlgorithms.run()
    InterviewGreedyAlgorithms.run()
    IndustryGreedyAlgorithms.run()
