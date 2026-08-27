"""The walrus operator (:=) demonstrated through sample quality checks."""


class UniversityWalrusOperator:
    """Teach the fundamental syntax of the assignment expression."""

    def __init__(self, purity_scores: list[float]) -> None:
        self.purity_scores = purity_scores

    def report_high_scores(self, threshold: float) -> list[float]:
        """Assign and reuse a value within a single conditional expression."""
        results: list[float] = []
        for score in self.purity_scores:
            if (adjusted := score * 100) >= threshold:
                results.append(adjusted)
        return results

    @staticmethod
    def run() -> None:
        scores = [0.72, 0.91, 0.65, 0.88]

        processor = UniversityWalrusOperator(scores)
        high_scores = processor.report_high_scores(threshold=80.0)

        print(f"High purity scores (as percentages): {high_scores}")


class InterviewWalrusOperator:
    """Solve a practical repeated-calculation problem using assignment expressions."""

    def __init__(self, samples: dict[str, float]) -> None:
        self.samples = samples

    def calculate_quality(self, sample_id: str) -> float:
        """Simulate an expensive quality calculation for a given sample."""
        raw_value = self.samples.get(sample_id, 0.0)
        return round(raw_value * 0.97, 3)

    def find_first_passing_sample(self, threshold: float) -> str | None:
        """Return the first sample that passes quality, without recomputing.

        Uses the walrus operator to avoid calling calculate_quality twice
        per sample: once to check the threshold and once to use the value.
        """
        if not self.samples:
            return None

        for sample_id in self.samples:
            if (score := self.calculate_quality(sample_id)) >= threshold:
                return f"{sample_id} passed with score {score}"

        return None

    @staticmethod
    def run() -> None:
        samples = {"S001": 0.80, "S002": 0.95, "S003": 0.70}
        empty_samples: dict[str, float] = {}

        case_one = InterviewWalrusOperator(samples)
        case_two = InterviewWalrusOperator(empty_samples)

        print(f"First passing sample: {case_one.find_first_passing_sample(0.85)}")
        print(f"Empty dataset result: {case_two.find_first_passing_sample(0.85)}")


class IndustryWalrusOperator:
    """Demonstrate disciplined, readability-first use of assignment expressions."""

    def __init__(self, readings: list[float]) -> None:
        self.readings = readings

    def filter_and_log_outliers(self, upper_bound: float) -> list[float]:
        """Collect outlier readings, using := only where it aids clarity.

        The walrus operator is used here because the computed deviation is
        both the filter condition and the value stored, avoiding duplicate
        computation. A normal assignment is used elsewhere for readability.
        """
        outliers: list[float] = []
        baseline = sum(self.readings) / len(self.readings) if self.readings else 0.0

        for reading in self.readings:
            if (deviation := abs(reading - baseline)) > upper_bound:
                outliers.append(deviation)

        return outliers

    @staticmethod
    def run() -> None:
        readings = [12.0, 13.5, 45.2, 12.8, 11.9]

        analyzer = IndustryWalrusOperator(readings)
        outliers = analyzer.filter_and_log_outliers(upper_bound=10.0)

        print(f"Detected outlier deviations: {outliers}")


if __name__ == "__main__":
    UniversityWalrusOperator.run()
    InterviewWalrusOperator.run()
    IndustryWalrusOperator.run()
