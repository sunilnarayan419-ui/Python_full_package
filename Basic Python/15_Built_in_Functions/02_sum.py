"""Demonstrations of the built-in sum() function using experimental measurement data."""


class UniversitySum:
    """Teach the fundamental behavior of sum() on numeric biological data."""

    def __init__(self, leaf_counts: list[int]) -> None:
        self.leaf_counts = leaf_counts

    def total_leaf_count(self) -> int:
        return sum(self.leaf_counts)

    @staticmethod
    def run() -> None:
        leaf_counts = [12, 15, 9, 20, 11]

        processor = UniversitySum(leaf_counts)
        print(f"Total leaf count across plants: {processor.total_leaf_count()}")


class InterviewSum:
    """Aggregate scientific measurements while handling missing/invalid values."""

    def __init__(self, measurements: list[float | None]) -> None:
        self.measurements = measurements

    def total_valid_measurements(self) -> float:
        """Sum only numeric measurements, skipping None values."""
        return sum(value for value in self.measurements if value is not None)

    def total_with_baseline(self, baseline: float) -> float:
        """Sum valid measurements starting from a baseline offset."""
        return sum((value for value in self.measurements if value is not None), baseline)

    @staticmethod
    def run() -> None:
        case_one: list[float | None] = [1.2, 3.4, None, 2.1, None]
        case_two: list[float | None] = [None, None]

        analyzer_one = InterviewSum(case_one)
        analyzer_two = InterviewSum(case_two)

        print(f"Case 1 total: {analyzer_one.total_valid_measurements()}")
        print(f"Case 1 total with 5.0 baseline: {analyzer_one.total_with_baseline(5.0)}")
        print(f"Case 2 total (all missing): {analyzer_two.total_valid_measurements()}")


class IndustrySum:
    """Aggregate and report scientific measurements across experiment batches."""

    def __init__(self, experiment_batches: dict[str, list[float]]) -> None:
        self.experiment_batches = experiment_batches

    def batch_totals(self) -> dict[str, float]:
        return {batch: sum(values) for batch, values in self.experiment_batches.items()}

    def grand_total(self) -> float:
        return sum(sum(values) for values in self.experiment_batches.values())

    @staticmethod
    def run() -> None:
        experiment_batches = {
            "batch_a": [10.5, 12.3, 9.8],
            "batch_b": [8.1, 7.6],
            "batch_c": [],
        }

        reporter = IndustrySum(experiment_batches)
        for batch, total in reporter.batch_totals().items():
            print(f"{batch}: total concentration {total:.2f}")

        print(f"Grand total concentration: {reporter.grand_total():.2f}")


if __name__ == "__main__":
    UniversitySum.run()
    InterviewSum.run()
    IndustrySum.run()
