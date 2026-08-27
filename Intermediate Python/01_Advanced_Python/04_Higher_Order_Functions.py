from __future__ import annotations

import functools
from typing import Callable, Iterable


class UniversityHigherOrderFunctions:
    """Demonstrates functions accepting other functions as arguments."""

    @staticmethod
    def apply_to_readings(readings: list[float], transform: Callable[[float], float]) -> list[float]:
        return [transform(value) for value in readings]

    @staticmethod
    def run() -> None:
        heights_cm = [12.0, 18.5, 9.3, 22.1]
        doubled = UniversityHigherOrderFunctions.apply_to_readings(heights_cm, lambda x: x * 2)
        print(doubled)


class InterviewHigherOrderFunctions:
    """Demonstrates functions that both accept and return functions, forming
    a small composable filter/transform pipeline over scientific data."""

    @staticmethod
    def compose(*functions: Callable[[float], float]) -> Callable[[float], float]:
        def composed(value: float) -> float:
            for func in functions:
                value = func(value)
            return value

        return composed

    @staticmethod
    def filter_readings(
        readings: Iterable[float], predicate: Callable[[float], bool]
    ) -> list[float]:
        return [r for r in readings if predicate(r)]

    @staticmethod
    def run() -> None:
        normalize = InterviewHigherOrderFunctions.compose(lambda x: x - 32, lambda x: x * 5 / 9)
        fahrenheit_readings = [98.6, 100.4, 97.2]
        celsius_readings = [normalize(f) for f in fahrenheit_readings]
        print([round(c, 2) for c in celsius_readings])

        elevated = InterviewHigherOrderFunctions.filter_readings(celsius_readings, lambda c: c > 37.0)
        print(f"elevated temperatures: {[round(c, 2) for c in elevated]}")


class IndustryHigherOrderFunctions:
    """Demonstrates a realistic, extensible data-processing pipeline built
    from higher-order functions, supporting arbitrary chained stages over
    a batch of scientific samples with reduction and reporting."""

    @staticmethod
    def build_pipeline(
        *stages: Callable[[list[float]], list[float]],
    ) -> Callable[[list[float]], list[float]]:
        def run_pipeline(data: list[float]) -> list[float]:
            for stage in stages:
                data = stage(data)
            return data

        return run_pipeline

    @staticmethod
    def stage_remove_negative(values: list[float]) -> list[float]:
        return [v for v in values if v >= 0]

    @staticmethod
    def stage_scale(factor: float) -> Callable[[list[float]], list[float]]:
        def stage(values: list[float]) -> list[float]:
            return [v * factor for v in values]

        return stage

    @staticmethod
    def reduce_metric(values: list[float], reducer: Callable[[float, float], float], initial: float) -> float:
        return functools.reduce(reducer, values, initial)

    @classmethod
    def run(cls) -> None:
        raw_concentrations = [-1.2, 3.4, 5.6, -0.1, 7.8]
        pipeline = cls.build_pipeline(
            cls.stage_remove_negative,
            cls.stage_scale(factor=1.5),
        )
        processed = pipeline(raw_concentrations)
        print(f"processed concentrations: {processed}")

        total = cls.reduce_metric(processed, lambda acc, x: acc + x, initial=0.0)
        print(f"total concentration: {total:.2f}")

        maximum = cls.reduce_metric(processed, max, initial=float("-inf"))
        print(f"max concentration: {maximum:.2f}")


if __name__ == "__main__":
    UniversityHigherOrderFunctions.run()
    InterviewHigherOrderFunctions.run()
    IndustryHigherOrderFunctions.run()
