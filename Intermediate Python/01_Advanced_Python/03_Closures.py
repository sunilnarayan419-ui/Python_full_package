from __future__ import annotations

from typing import Callable


class UniversityClosures:
    """Demonstrates a closure that remembers a captured configuration value."""

    @staticmethod
    def make_unit_converter(factor: float) -> Callable[[float], float]:
        def convert(value: float) -> float:
            return value * factor

        return convert

    @staticmethod
    def run() -> None:
        cm_to_mm = UniversityClosures.make_unit_converter(10.0)
        print(cm_to_mm(4.5))
        print(cm_to_mm(7.2))


class InterviewClosures:
    """Demonstrates closures maintaining running state without global
    variables, including correct use of the nonlocal keyword."""

    @staticmethod
    def make_running_average() -> Callable[[float], float]:
        total = 0.0
        count = 0

        def add_reading(value: float) -> float:
            nonlocal total, count
            total += value
            count += 1
            return total / count

        return add_reading

    @staticmethod
    def run() -> None:
        tracker = InterviewClosures.make_running_average()
        for ph_reading in (6.8, 7.0, 7.1, 6.9):
            print(f"running average pH: {tracker(ph_reading):.3f}")


class IndustryClosures:
    """Demonstrates closures used to build configurable, stateful validators
    for a laboratory instrument calibration workflow, avoiding both global
    mutable state and unnecessary class boilerplate."""

    @staticmethod
    def make_calibration_monitor(
        expected: float,
        tolerance: float,
    ) -> tuple[Callable[[float], bool], Callable[[], dict[str, float | int]]]:
        if tolerance <= 0:
            raise ValueError("tolerance must be positive")

        deviations: list[float] = []
        breaches = 0

        def check(reading: float) -> bool:
            nonlocal breaches
            deviation = abs(reading - expected)
            deviations.append(deviation)
            within_tolerance = deviation <= tolerance
            if not within_tolerance:
                breaches += 1
            return within_tolerance

        def summary() -> dict[str, float | int]:
            avg_deviation = sum(deviations) / len(deviations) if deviations else 0.0
            return {
                "readings": len(deviations),
                "breaches": breaches,
                "avg_deviation": round(avg_deviation, 4),
            }

        return check, summary

    @staticmethod
    def run() -> None:
        check, summary = IndustryClosures.make_calibration_monitor(expected=37.0, tolerance=0.5)
        for temperature in (36.8, 37.4, 38.2, 36.9):
            ok = check(temperature)
            print(f"reading={temperature} within_tolerance={ok}")

        print(summary())


if __name__ == "__main__":
    UniversityClosures.run()
    InterviewClosures.run()
    IndustryClosures.run()
