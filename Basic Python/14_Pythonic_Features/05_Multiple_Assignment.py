"""Multiple assignment demonstrated through sample metadata and lab results."""


class UniversityMultipleAssignment:
    """Teach the fundamental syntax of assigning multiple values at once."""

    def __init__(self, sample_id: str, species: str, height_cm: float) -> None:
        self.sample_id = sample_id
        self.species = species
        self.height_cm = height_cm

    def describe(self) -> str:
        """Return a human-readable description of the sample metadata."""
        sample_id, species, height_cm = self.sample_id, self.species, self.height_cm
        return f"{sample_id}: {species}, {height_cm}cm"

    @staticmethod
    def run() -> None:
        sample_id, species, height_cm = "S001", "Arabidopsis", 12.5

        record = UniversityMultipleAssignment(sample_id, species, height_cm)
        print(f"Sample description: {record.describe()}")

        left_value, right_value = 5, 10
        left_value, right_value = right_value, left_value
        print(f"Swapped values: left={left_value}, right={right_value}")


class InterviewMultipleAssignment:
    """Solve a practical multi-value processing problem for lab measurements."""

    def __init__(self, raw_measurements: list[float]) -> None:
        self.raw_measurements = raw_measurements

    def compute_statistics(self) -> tuple[float, float, float]:
        """Return minimum, maximum, and average of the measurements.

        Raises a clear error for empty input rather than failing silently.
        """
        if not self.raw_measurements:
            raise ValueError("Cannot compute statistics on an empty dataset.")

        minimum, maximum = min(self.raw_measurements), max(self.raw_measurements)
        average = sum(self.raw_measurements) / len(self.raw_measurements)
        return minimum, maximum, average

    @staticmethod
    def run() -> None:
        measurements = [7.2, 5.9, 8.4, 6.1]

        processor = InterviewMultipleAssignment(measurements)
        low, high, mean = processor.compute_statistics()
        print(f"Min: {low}, Max: {high}, Mean: {round(mean, 2)}")

        try:
            empty_processor = InterviewMultipleAssignment([])
            empty_processor.compute_statistics()
        except ValueError as error:
            print(f"Handled error: {error}")


class IndustryMultipleAssignment:
    """Handle structured multi-value results from a scientific workflow."""

    def __init__(self, experiment_log: list[tuple[str, float, float]]) -> None:
        self.experiment_log = experiment_log

    def run_quality_pipeline(self) -> tuple[int, int, float]:
        """Return counts of passed, failed, and the overall pass rate.

        Each log entry is (sample_id, ph_level, purity_score); unpacked
        directly for clarity within the processing loop.
        """
        passed_count, failed_count = 0, 0

        for sample_id, ph_level, purity_score in self.experiment_log:
            is_valid = 6.5 <= ph_level <= 7.5 and purity_score >= 0.9
            passed_count, failed_count = (
                (passed_count + 1, failed_count)
                if is_valid
                else (passed_count, failed_count + 1)
            )

        total = passed_count + failed_count
        pass_rate = round(passed_count / total, 2) if total else 0.0
        return passed_count, failed_count, pass_rate

    @staticmethod
    def run() -> None:
        log: list[tuple[str, float, float]] = [
            ("S001", 6.9, 0.95),
            ("S002", 7.8, 0.92),
            ("S003", 7.1, 0.88),
        ]

        pipeline = IndustryMultipleAssignment(log)
        passed, failed, rate = pipeline.run_quality_pipeline()

        print(f"Passed: {passed}, Failed: {failed}, Pass rate: {rate}")


if __name__ == "__main__":
    UniversityMultipleAssignment.run()
    InterviewMultipleAssignment.run()
    IndustryMultipleAssignment.run()
