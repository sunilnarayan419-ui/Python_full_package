"""Demonstrations of the built-in abs() function using experimental deviation data."""


class UniversityAbs:
    """Teach the fundamental behavior of abs() on measurement differences."""

    def __init__(self, observed: float, expected: float) -> None:
        self.observed = observed
        self.expected = expected

    def absolute_difference(self) -> float:
        return abs(self.observed - self.expected)

    @staticmethod
    def run() -> None:
        processor = UniversityAbs(observed=58.3, expected=60.0)
        print(f"Absolute height difference: {processor.absolute_difference()} cm")


class InterviewAbs:
    """Calculate experimental deviation from control values with edge cases."""

    def __init__(self, control_value: float) -> None:
        self.control_value = control_value

    def deviation_for(self, sample_value: float) -> float:
        return abs(sample_value - self.control_value)

    def deviations_for_batch(self, sample_values: list[float]) -> list[float]:
        """Return absolute deviations for each sample, ignoring an empty batch."""
        if not sample_values:
            return []
        return [self.deviation_for(value) for value in sample_values]

    @staticmethod
    def run() -> None:
        analyzer = InterviewAbs(control_value=50.0)

        case_one = [48.5, 52.3, 45.0, 61.2]
        case_two: list[float] = []

        print(f"Deviations (case 1): {analyzer.deviations_for_batch(case_one)}")
        print(f"Deviations (case 2, empty): {analyzer.deviations_for_batch(case_two)}")


class IndustryAbs:
    """Quality-control deviation analysis for a batch of scientific samples."""

    def __init__(self, reference_value: float, tolerance: float) -> None:
        self.reference_value = reference_value
        self.tolerance = tolerance

    def is_within_tolerance(self, measured_value: float) -> bool:
        return abs(measured_value - self.reference_value) <= self.tolerance

    def flag_out_of_tolerance(self, samples: dict[str, float]) -> list[str]:
        """Return sample IDs whose measurement deviates beyond tolerance."""
        return [
            sample_id
            for sample_id, value in samples.items()
            if not self.is_within_tolerance(value)
        ]

    @staticmethod
    def run() -> None:
        qc = IndustryAbs(reference_value=100.0, tolerance=2.5)
        samples = {
            "S001": 101.2,
            "S002": 96.0,
            "S003": 100.1,
            "S004": 104.8,
        }

        flagged = qc.flag_out_of_tolerance(samples)
        print(f"Samples flagged out of tolerance: {flagged}")


if __name__ == "__main__":
    UniversityAbs.run()
    InterviewAbs.run()
    IndustryAbs.run()
