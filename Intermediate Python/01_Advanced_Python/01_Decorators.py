from __future__ import annotations

import functools
import time
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


class UniversityDecorators:
    """Demonstrates a basic function decorator that logs calls."""

    @staticmethod
    def log_measurement(func: Callable[..., float]) -> Callable[..., float]:
        def wrapper(*args: Any, **kwargs: Any) -> float:
            result = func(*args, **kwargs)
            print(f"[log] {func.__name__} recorded value {result}")
            return result

        return wrapper

    @staticmethod
    def run() -> None:
        @UniversityDecorators.log_measurement
        def leaf_length_cm(sample_id: str, length: float) -> float:
            return length

        leaf_length_cm("plant-01", 4.2)
        leaf_length_cm("plant-02", 5.7)


class InterviewDecorators:
    """Demonstrates decorators that preserve metadata and validate inputs."""

    @staticmethod
    def validate_positive(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for value in list(args) + list(kwargs.values()):
                if isinstance(value, (int, float)) and value < 0:
                    raise ValueError(f"Measurement must be non-negative, got {value}")
            return func(*args, **kwargs)

        return wrapper  # type: ignore[return-value]

    @staticmethod
    def timed(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed_ms = (time.perf_counter() - start) * 1000
            print(f"[timed] {func.__name__} took {elapsed_ms:.3f} ms")
            return result

        return wrapper  # type: ignore[return-value]

    @staticmethod
    def run() -> None:
        @InterviewDecorators.timed
        @InterviewDecorators.validate_positive
        def growth_rate(initial_height_cm: float, final_height_cm: float, days: int) -> float:
            return (final_height_cm - initial_height_cm) / days

        print(growth_rate(3.0, 9.0, 6))
        print(f"__name__ preserved: {growth_rate.__name__}")

        try:
            growth_rate(-1.0, 5.0, 3)
        except ValueError as exc:
            print(f"caught expected error: {exc}")


class IndustryDecorators:
    """Demonstrates a reusable, type-aware, parameterized decorator suite
    for validating and auditing scientific measurement functions."""

    _AUDIT_LOG: list[str] = []

    @classmethod
    def audited(cls, category: str) -> Callable[[F], F]:
        """Parameterized decorator that tags calls with a measurement category."""

        def decorator(func: F) -> F:
            @functools.wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                try:
                    result = func(*args, **kwargs)
                except Exception as exc:
                    cls._AUDIT_LOG.append(f"FAILED[{category}] {func.__name__}: {exc}")
                    raise
                cls._AUDIT_LOG.append(f"OK[{category}] {func.__name__} -> {result!r}")
                return result

            return wrapper  # type: ignore[return-value]

        return decorator

    @staticmethod
    def range_checked(minimum: float, maximum: float) -> Callable[[F], F]:
        def decorator(func: F) -> F:
            @functools.wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                result = func(*args, **kwargs)
                if not (minimum <= result <= maximum):
                    raise ValueError(
                        f"{func.__name__} produced {result}, expected within "
                        f"[{minimum}, {maximum}]"
                    )
                return result

            return wrapper  # type: ignore[return-value]

        return decorator

    @classmethod
    def run(cls) -> None:
        @cls.audited(category="photosynthesis")
        @cls.range_checked(minimum=0.0, maximum=100.0)
        def photosynthetic_efficiency(light_absorbed: float, light_available: float) -> float:
            if light_available == 0:
                raise ZeroDivisionError("light_available must be non-zero")
            return (light_absorbed / light_available) * 100

        print(photosynthetic_efficiency(45.0, 60.0))

        try:
            photosynthetic_efficiency(0.0, 0.0)
        except ZeroDivisionError as exc:
            print(f"caught expected error: {exc}")

        for entry in cls._AUDIT_LOG:
            print(entry)


if __name__ == "__main__":
    UniversityDecorators.run()
    InterviewDecorators.run()
    IndustryDecorators.run()
