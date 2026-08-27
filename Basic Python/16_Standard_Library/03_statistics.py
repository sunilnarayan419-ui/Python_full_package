"""Demonstrates the statistics module using plant and gene-expression data."""

import statistics


class UniversityStatistics:
    """Introduces basic descriptive statistics using plant height data."""

    def __init__(self, heights_cm: list[float]) -> None:
        self.heights_cm = heights_cm

    def describe(self) -> dict[str, float]:
        return {
            "mean": statistics.mean(self.heights_cm),
            "median": statistics.median(self.heights_cm),
            "stdev": statistics.stdev(self.heights_cm),
        }

    @staticmethod
    def run() -> None:
        heights_cm = [24.5, 27.1, 25.8, 26.3, 28.0]
        processor = UniversityStatistics(heights_cm)

        summary = processor.describe()
        print(f"Mean height: {summary['mean']:.2f} cm")
        print(f"Median height: {summary['median']:.2f} cm")
        print(f"Standard deviation: {summary['stdev']:.2f} cm")


class InterviewStatistics:
    """Solves a statistical-summary problem with empty/small-sample edge cases."""

    def summarize_expression_levels(self, values: list[float]) -> dict[str, float | str]:
        """Summarize gene-expression measurements, guarding against invalid input.

        - Empty input raises a clear error rather than letting statistics.mean fail
          with an unclear StatisticsError.
        - A single-value sample cannot have a standard deviation, so it is reported
          explicitly rather than raised as an error.
        """
        if not values:
            raise ValueError("values must not be empty.")

        summary: dict[str, float | str] = {
            "mean": statistics.mean(values),
            "median": statistics.median(values),
        }

        if len(values) >= 2:
            summary["stdev"] = statistics.stdev(values)
        else:
            summary["stdev"] = "undefined (n < 2)"

        return summary

    @staticmethod
    def run() -> None:
        solver = InterviewStatistics()

        # Test case 1: normal dataset
        expression_levels = [4.2, 5.1, 4.8, 6.0, 5.5, 4.9]
        print(solver.summarize_expression_levels(expression_levels))

        # Test case 2: single-value edge case
        print(solver.summarize_expression_levels([5.0]))

        # Test case 3: empty edge case, handled defensively
        try:
            solver.summarize_expression_levels([])
        except ValueError as error:
            print(f"Handled empty input: {error}")


class IndustryStatistics:
    """Reusable experimental-data summary utility for laboratory assay results."""

    def __init__(self, min_sample_size: int = 3) -> None:
        self.min_sample_size = min_sample_size

    def summarize_assay(self, replicate_values: list[float]) -> dict[str, float | int]:
        """Produce a structured statistical summary for a set of assay replicates.

        Enforces a minimum sample size, since summary statistics from very small
        samples can be misleading in a production reporting pipeline.
        """
        if len(replicate_values) < self.min_sample_size:
            raise ValueError(
                f"Need at least {self.min_sample_size} replicates, "
                f"got {len(replicate_values)}."
            )

        return {
            "n": len(replicate_values),
            "mean": round(statistics.mean(replicate_values), 4),
            "median": round(statistics.median(replicate_values), 4),
            "stdev": round(statistics.stdev(replicate_values), 4),
            "variance": round(statistics.variance(replicate_values), 4),
        }

    def compare_conditions(
        self, condition_results: dict[str, list[float]]
    ) -> dict[str, dict[str, float | int]]:
        """Summarize assay results across multiple experimental conditions.

        Note: this provides descriptive summaries only. Formal hypothesis testing
        (e.g. t-tests, ANOVA) requires a dedicated statistical library and is
        intentionally out of scope for the standard-library statistics module.
        """
        return {
            condition: self.summarize_assay(values)
            for condition, values in condition_results.items()
        }

    @staticmethod
    def run() -> None:
        analyzer = IndustryStatistics(min_sample_size=3)

        condition_results = {
            "control": [12.1, 11.8, 12.5, 12.0],
            "drug_treated": [8.4, 8.9, 8.1, 8.6],
        }

        summaries = analyzer.compare_conditions(condition_results)
        for condition, summary in summaries.items():
            print(f"{condition}: {summary}")


if __name__ == "__main__":
    UniversityStatistics.run()
    InterviewStatistics.run()
    IndustryStatistics.run()
