from __future__ import annotations

import logging
import math
from dataclasses import dataclass
from typing import Callable

import numpy as np

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")


class CalculatorError(Exception):
    """Base error for calculator operations."""


class DomainError(CalculatorError):
    """Raised when an operation receives a mathematically invalid input."""


class UnknownOperationError(CalculatorError):
    """Raised when an unregistered operation is requested."""


@dataclass(frozen=True, slots=True)
class OperationResult:
    """Structured result of a calculator operation."""

    operation: str
    inputs: tuple[float, ...]
    value: float


class ScientificCalculator:
    """A reusable scientific calculator engine with a controlled operation registry."""

    def __init__(self) -> None:
        self._operations: dict[str, Callable[..., float]] = {
            "add": self._add,
            "subtract": self._subtract,
            "multiply": self._multiply,
            "divide": self._divide,
            "power": self._power,
            "sqrt": self._sqrt,
            "nth_root": self._nth_root,
            "log": self._log,
            "ln": self._ln,
            "sin": self._sin,
            "cos": self._cos,
            "tan": self._tan,
            "exp": self._exp,
            "mean": self._mean,
            "std": self._std,
        }

    def available_operations(self) -> tuple[str, ...]:
        return tuple(sorted(self._operations))

    def calculate(self, operation: str, *args: float) -> OperationResult:
        handler = self._operations.get(operation)
        if handler is None:
            raise UnknownOperationError(f"Unknown operation: '{operation}'.")
        value = handler(*args)
        return OperationResult(operation=operation, inputs=tuple(args), value=value)

    @staticmethod
    def _add(a: float, b: float) -> float:
        return a + b

    @staticmethod
    def _subtract(a: float, b: float) -> float:
        return a - b

    @staticmethod
    def _multiply(a: float, b: float) -> float:
        return a * b

    @staticmethod
    def _divide(a: float, b: float) -> float:
        if b == 0:
            raise DomainError("Division by zero is undefined.")
        return a / b

    @staticmethod
    def _power(base: float, exponent: float) -> float:
        try:
            return math.pow(base, exponent)
        except (ValueError, OverflowError) as exc:
            raise DomainError(f"Cannot compute {base} ** {exponent}.") from exc

    @staticmethod
    def _sqrt(value: float) -> float:
        if value < 0:
            raise DomainError("Square root of a negative number is undefined in the real domain.")
        return math.sqrt(value)

    @staticmethod
    def _nth_root(value: float, n: float) -> float:
        if n == 0:
            raise DomainError("Zeroth root is undefined.")
        if value < 0 and n % 2 == 0:
            raise DomainError("Even root of a negative number is undefined in the real domain.")
        sign = -1.0 if value < 0 else 1.0
        return sign * (abs(value) ** (1.0 / n))

    @staticmethod
    def _log(value: float, base: float = 10.0) -> float:
        if value <= 0:
            raise DomainError("Logarithm is undefined for values <= 0.")
        if base <= 0 or base == 1:
            raise DomainError("Logarithm base must be positive and not equal to 1.")
        return math.log(value, base)

    @staticmethod
    def _ln(value: float) -> float:
        if value <= 0:
            raise DomainError("Natural logarithm is undefined for values <= 0.")
        return math.log(value)

    @staticmethod
    def _sin(radians: float) -> float:
        return math.sin(radians)

    @staticmethod
    def _cos(radians: float) -> float:
        return math.cos(radians)

    @staticmethod
    def _tan(radians: float) -> float:
        cos_value = math.cos(radians)
        if math.isclose(cos_value, 0.0, abs_tol=1e-12):
            raise DomainError("Tangent is undefined at this angle (cosine is zero).")
        return math.tan(radians)

    @staticmethod
    def _exp(value: float) -> float:
        try:
            return math.exp(value)
        except OverflowError as exc:
            raise DomainError(f"Exponential overflow for input {value}.") from exc

    @staticmethod
    def _mean(*values: float) -> float:
        if not values:
            raise DomainError("Mean requires at least one value.")
        return float(np.mean(values))

    @staticmethod
    def _std(*values: float) -> float:
        if len(values) < 2:
            raise DomainError("Standard deviation requires at least two values.")
        return float(np.std(values, ddof=1))


def run() -> list[OperationResult]:
    """Runs a deterministic set of scientific calculator demonstrations."""
    calculator = ScientificCalculator()

    demonstrations: list[tuple[str, tuple[float, ...]]] = [
        ("add", (12.5, 7.3)),
        ("divide", (100.0, 4.0)),
        ("power", (2.0, 10.0)),
        ("sqrt", (144.0,)),
        ("nth_root", (27.0, 3.0)),
        ("log", (1000.0, 10.0)),
        ("ln", (math.e,)),
        ("sin", (math.pi / 2,)),
        ("exp", (1.0,)),
        ("mean", (2.0, 4.0, 6.0, 8.0)),
        ("std", (2.0, 4.0, 6.0, 8.0)),
    ]

    results: list[OperationResult] = []
    for operation, args in demonstrations:
        try:
            result = calculator.calculate(operation, *args)
            results.append(result)
            logger.info("%s%s = %.6f", operation, args, result.value)
        except DomainError as exc:
            logger.error("Domain error for %s%s: %s", operation, args, exc)

    return results


if __name__ == "__main__":
    run()
