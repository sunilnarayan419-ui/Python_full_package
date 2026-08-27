"""Demonstrates PEP 8-compliant production code style: consistent naming,
organized imports, proper whitespace, and readable expressions.

Style principles followed throughout this file:
    - snake_case for functions and variables, PascalCase for classes
    - UPPER_SNAKE_CASE for module-level constants
    - two blank lines between top-level definitions
    - imports grouped as: standard library, then local (none here)
    - lines kept within a readable length
    - no trailing whitespace, consistent 4-space indentation
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, pstdev

DEFAULT_OUTLIER_THRESHOLD_STD_DEVIATIONS = 2.0
MINIMUM_SAMPLE_COUNT_FOR_STATISTICS = 3


class InsufficientDataError(ValueError):
    """Raised when too few samples are available for statistical analysis."""


@dataclass(frozen=True, slots=True)
class Measurement:
    sample_id: str
    value: float


class OutlierDetector:
    """Flags measurements that fall far from the sample mean."""

    def __init__(
        self, threshold_std_deviations: float = DEFAULT_OUTLIER_THRESHOLD_STD_DEVIATIONS
    ) -> None:
        self.threshold_std_deviations = threshold_std_deviations

    def detect(self, measurements: list[Measurement]) -> list[Measurement]:
        if len(measurements) < MINIMUM_SAMPLE_COUNT_FOR_STATISTICS:
            raise InsufficientDataError(
                "at least "
                f"{MINIMUM_SAMPLE_COUNT_FOR_STATISTICS} measurements are required"
            )

        values = [measurement.value for measurement in measurements]
        mean_value = mean(values)
        std_deviation = pstdev(values)

        if std_deviation == 0:
            return []

        outliers = [
            measurement
            for measurement in measurements
            if self._is_outlier(measurement.value, mean_value, std_deviation)
        ]
        return outliers

    def _is_outlier(self, value: float, mean_value: float, std_deviation: float) -> bool:
        distance = abs(value - mean_value) / std_deviation
        return distance > self.threshold_std_deviations


def summarize_measurements(measurements: list[Measurement]) -> str:
    detector = OutlierDetector()
    outliers = detector.detect(measurements)

    if not outliers:
        return "No outliers detected."

    outlier_ids = ", ".join(measurement.sample_id for measurement in outliers)
    return f"Outliers detected: {outlier_ids}"


if __name__ == "__main__":
    measurements = [
        Measurement(sample_id="S-01", value=10.1),
        Measurement(sample_id="S-02", value=10.3),
        Measurement(sample_id="S-03", value=9.9),
        Measurement(sample_id="S-04", value=45.0),
    ]

    print(summarize_measurements(measurements))
