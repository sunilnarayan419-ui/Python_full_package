"""Demonstrates the time module for benchmarking scientific data processing."""

import time


class UniversityTime:
    """Introduces basic time operations using a simulated processing delay."""

    def __init__(self) -> None:
        self.start_timestamp: float | None = None

    def record_start(self) -> float:
        self.start_timestamp = time.time()
        return self.start_timestamp

    def simulate_processing(self, delay_seconds: float) -> None:
        time.sleep(delay_seconds)

    @staticmethod
    def run() -> None:
        demo = UniversityTime()
        start = demo.record_start()
        demo.simulate_processing(delay_seconds=0.01)
        elapsed = time.time() - start

        print(f"Start timestamp (epoch seconds): {start:.2f}")
        print(f"Elapsed wall-clock time: {elapsed:.4f}s")


class InterviewTime:
    """Solves an execution-time measurement problem using perf_counter."""

    def measure_execution(self, operation: object, *args: object) -> tuple[object, float]:
        """Time the execution of a callable, returning its result and duration.

        Raises TypeError if operation is not callable, since silently returning
        an unusable result would hide a caller mistake.
        """
        if not callable(operation):
            raise TypeError("operation must be callable.")

        start = time.perf_counter()
        result = operation(*args)
        elapsed = time.perf_counter() - start
        return result, elapsed

    @staticmethod
    def run() -> None:
        solver = InterviewTime()

        def sum_of_squares(values: list[int]) -> int:
            return sum(value * value for value in values)

        # Test case 1: normal callable
        data = list(range(1000))
        result, elapsed = solver.measure_execution(sum_of_squares, data)
        print(f"Sum of squares: {result}, measured in {elapsed:.6f}s")

        # Test case 2: edge case, non-callable input
        try:
            solver.measure_execution(42, data)
        except TypeError as error:
            print(f"Handled invalid operation: {error}")


class IndustryTime:
    """Lightweight, reusable performance-measurement utility for pipelines."""

    def __init__(self) -> None:
        self.timings: dict[str, float] = {}

    def time_stage(self, stage_name: str, operation: object, *args: object) -> object:
        """Run and time a named pipeline stage, recording its duration for reporting."""
        start = time.perf_counter()
        result = operation(*args)
        self.timings[stage_name] = time.perf_counter() - start
        return result

    def report(self) -> dict[str, str]:
        return {stage: f"{duration:.6f}s" for stage, duration in self.timings.items()}

    @staticmethod
    def run() -> None:
        benchmark = IndustryTime()

        def normalize_readings(values: list[float]) -> list[float]:
            maximum = max(values)
            return [round(value / maximum, 4) for value in values]

        def flag_outliers(values: list[float], threshold: float) -> list[float]:
            return [value for value in values if value > threshold]

        readings = [4.2, 5.1, 4.8, 6.0, 5.5, 9.9]

        normalized = benchmark.time_stage("normalize", normalize_readings, readings)
        outliers = benchmark.time_stage("flag_outliers", flag_outliers, readings, 6.0)

        print(f"Normalized readings: {normalized}")
        print(f"Outliers detected: {outliers}")
        print(f"Stage timings: {benchmark.report()}")


if __name__ == "__main__":
    UniversityTime.run()
    InterviewTime.run()
    IndustryTime.run()
