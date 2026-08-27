"""Demonstrations of the built-in round() function using scientific measurement data."""


class UniversityRound:
    """Teach the fundamental behavior of round() on biological measurements."""

    def __init__(self, raw_value: float) -> None:
        self.raw_value = raw_value

    def rounded_value(self) -> float:
        return round(self.raw_value)

    @staticmethod
    def run() -> None:
        processor = UniversityRound(raw_value=58.678)
        print(f"Raw measurement: {processor.raw_value}")
        print(f"Rounded measurement: {processor.rounded_value()}")


class InterviewRound:
    """Round measurements to a controlled, configurable decimal precision."""

    def __init__(self, precision: int) -> None:
        self.precision = precision

    def round_measurement(self, value: float) -> float:
        return round(value, self.precision)

    def round_batch(self, values: list[float]) -> list[float]:
        """Round a batch of measurements, skipping non-numeric entries."""
        return [
            self.round_measurement(value)
            for value in values
            if isinstance(value, (int, float))
        ]

    @staticmethod
    def run() -> None:
        analyzer = InterviewRound(precision=2)

        case_one = [3.14159, 2.71828, 1.41421]
        case_two: list[float] = []

        print(f"Rounded batch (case 1): {analyzer.round_batch(case_one)}")
        print(f"Rounded batch (case 2, empty): {analyzer.round_batch(case_two)}")


class IndustryRound:
    """Normalize and format scientific measurements for reporting purposes."""

    def __init__(self, report_precision: int) -> None:
        self.report_precision = report_precision

    def normalize_report(self, measurements: dict[str, float]) -> dict[str, float]:
        """Return a new dict with each measurement rounded for reporting.

        Note: this does not alter the original underlying scientific data;
        it only affects the value used in the generated report.
        """
        return {
            key: round(value, self.report_precision)
            for key, value in measurements.items()
        }

    @staticmethod
    def run() -> None:
        reporter = IndustryRound(report_precision=3)
        raw_measurements = {
            "gene_expression": 4.567891,
            "concentration_mg_ml": 12.345678,
            "purity_ratio": 0.998765,
        }

        report = reporter.normalize_report(raw_measurements)
        for key, value in report.items():
            print(f"{key}: {value}")


if __name__ == "__main__":
    UniversityRound.run()
    InterviewRound.run()
    IndustryRound.run()
