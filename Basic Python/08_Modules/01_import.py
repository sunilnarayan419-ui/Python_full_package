"""
01_import.py

Topic: The `import module` statement.

Demonstrates namespace-qualified access to standard-library functionality
using biological measurement data.
"""

import math
import statistics
import datetime


class UniversityImport:
    """Introduces `import module` and namespace-qualified access."""

    @staticmethod
    def run() -> None:
        leaf_lengths_cm: list[float] = [4.2, 5.1, 3.8, 6.0, 4.9]

        mean_length = statistics.mean(leaf_lengths_cm)
        stdev_length = statistics.stdev(leaf_lengths_cm)
        rounded_stdev = math.sqrt(stdev_length ** 2)

        print("University: import module")
        print(f"  Leaf lengths (cm): {leaf_lengths_cm}")
        print(f"  Mean length: {mean_length:.2f} cm")
        print(f"  Std deviation (via math.sqrt check): {rounded_stdev:.2f} cm")


class InterviewImport:
    """Uses imported modules to solve a small realistic problem."""

    @staticmethod
    def _summarize_sample(measurements: list[float]) -> dict[str, float]:
        if not measurements:
            raise ValueError("Sample must contain at least one measurement.")

        return {
            "mean": statistics.mean(measurements),
            "median": statistics.median(measurements),
            "variance": statistics.variance(measurements) if len(measurements) > 1 else 0.0,
        }

    @staticmethod
    def run() -> None:
        plant_heights_mm: list[float] = [152.3, 148.9, 160.1, 155.4, 149.7, 158.2]

        summary = InterviewImport._summarize_sample(plant_heights_mm)
        experiment_timestamp = datetime.datetime.now().isoformat(timespec="seconds")

        print("Interview: import module")
        print(f"  Sample size: {len(plant_heights_mm)}")
        print(f"  Summary: {summary}")
        print(f"  Recorded at: {experiment_timestamp}")


class IndustryImport:
    """Demonstrates maintainable use of imported modules in a small workflow."""

    def __init__(self, sample_id: str, measurements: list[float]) -> None:
        if not sample_id:
            raise ValueError("sample_id must be a non-empty string.")
        if not measurements:
            raise ValueError("measurements must contain at least one value.")

        self._sample_id = sample_id
        self._measurements = measurements
        self._collected_at = datetime.datetime.now()

    @property
    def sample_id(self) -> str:
        return self._sample_id

    def mean_measurement(self) -> float:
        return statistics.mean(self._measurements)

    def coefficient_of_variation(self) -> float:
        mean_value = self.mean_measurement()
        if mean_value == 0:
            return 0.0
        stdev_value = statistics.stdev(self._measurements) if len(self._measurements) > 1 else 0.0
        return stdev_value / mean_value

    def report(self) -> str:
        return (
            f"Sample {self._sample_id} | "
            f"mean={self.mean_measurement():.2f} | "
            f"cv={self.coefficient_of_variation():.3f} | "
            f"n={len(self._measurements)} | "
            f"collected={self._collected_at.isoformat(timespec='seconds')}"
        )

    @staticmethod
    def run() -> None:
        enzyme_activity_units: list[float] = [12.4, 11.9, 13.1, 12.7, 12.0, 13.4]

        analyzer = IndustryImport("ENZ-2024-018", enzyme_activity_units)
        print("Industry: import module")
        print(f"  {analyzer.report()}")


if __name__ == "__main__":
    UniversityImport.run()
    InterviewImport.run()
    IndustryImport.run()
