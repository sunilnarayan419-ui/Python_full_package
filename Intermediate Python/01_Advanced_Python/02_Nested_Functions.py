from __future__ import annotations

from typing import Callable


class UniversityNestedFunctions:
    """Demonstrates a function defined inside another function."""

    @staticmethod
    def celsius_report(readings: list[float]) -> list[str]:
        def format_reading(value: float) -> str:
            return f"{value:.1f} C"

        return [format_reading(v) for v in readings]

    @staticmethod
    def run() -> None:
        readings = [21.4, 22.8, 19.9]
        print(UniversityNestedFunctions.celsius_report(readings))


class InterviewNestedFunctions:
    """Demonstrates nested functions used as private helpers with validation,
    hidden from the module namespace."""

    @staticmethod
    def build_outlier_filter(mean: float, std_dev: float, threshold: float = 2.0) -> Callable[[float], bool]:
        if std_dev <= 0:
            raise ValueError("std_dev must be positive")

        def is_outlier(value: float) -> bool:
            z_score = abs(value - mean) / std_dev
            return z_score > threshold

        return is_outlier

    @staticmethod
    def run() -> None:
        expression_levels = [5.1, 5.4, 5.0, 12.9, 5.3]
        mean = sum(expression_levels) / len(expression_levels)
        variance = sum((x - mean) ** 2 for x in expression_levels) / len(expression_levels)
        std_dev = variance ** 0.5

        is_outlier = InterviewNestedFunctions.build_outlier_filter(mean, std_dev)
        outliers = [v for v in expression_levels if is_outlier(v)]
        print(f"mean={mean:.2f} std_dev={std_dev:.2f} outliers={outliers}")


class IndustryNestedFunctions:
    """Demonstrates nested helper functions inside a well-scoped pipeline
    function, used to keep validation, transformation, and aggregation
    logic private and testable in isolation via the returned callable."""

    @staticmethod
    def build_normalization_pipeline(
        baseline: float,
        precision: int = 2,
    ) -> Callable[[list[float]], list[float]]:
        if precision < 0:
            raise ValueError("precision must be non-negative")

        def validate(values: list[float]) -> None:
            if not values:
                raise ValueError("values must not be empty")
            if any(v < 0 for v in values):
                raise ValueError("gene expression values must be non-negative")

        def normalize(value: float) -> float:
            return round(value / baseline, precision) if baseline else 0.0

        def pipeline(values: list[float]) -> list[float]:
            validate(values)
            return [normalize(v) for v in values]

        return pipeline

    @staticmethod
    def run() -> None:
        pipeline = IndustryNestedFunctions.build_normalization_pipeline(baseline=10.0, precision=3)
        result = pipeline([10.0, 20.0, 5.0, 12.5])
        print(f"normalized expression: {result}")

        try:
            pipeline([])
        except ValueError as exc:
            print(f"caught expected error: {exc}")


if __name__ == "__main__":
    UniversityNestedFunctions.run()
    InterviewNestedFunctions.run()
    IndustryNestedFunctions.run()
