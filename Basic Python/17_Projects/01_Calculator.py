"""A professional command-line calculator application.

Provides a small, extensible arithmetic engine with input validation,
calculation history, and a clean CLI. No arbitrary expression evaluation
is performed; every operation is an explicit, whitelisted function.
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


class CalculatorError(Exception):
    """Base exception for calculator failures."""


class DivisionByZeroError(CalculatorError):
    """Raised when a division or modulo by zero is attempted."""


class InvalidOperationError(CalculatorError):
    """Raised when an unknown operation is requested."""


class Operation(Enum):
    ADD = "1"
    SUBTRACT = "2"
    MULTIPLY = "3"
    DIVIDE = "4"
    POWER = "5"
    MODULO = "6"
    SQUARE_ROOT = "7"

    @property
    def label(self) -> str:
        return {
            Operation.ADD: "Addition",
            Operation.SUBTRACT: "Subtraction",
            Operation.MULTIPLY: "Multiplication",
            Operation.DIVIDE: "Division",
            Operation.POWER: "Exponentiation",
            Operation.MODULO: "Modulo",
            Operation.SQUARE_ROOT: "Square Root",
        }[self]

    @property
    def is_unary(self) -> bool:
        return self is Operation.SQUARE_ROOT


@dataclass(slots=True, frozen=True)
class CalculationRecord:
    """Immutable record of a single calculation."""

    operation: str
    operands: tuple[float, ...]
    result: float
    timestamp: datetime = field(default_factory=datetime.now)

    def format(self) -> str:
        operands_str = ", ".join(str(o) for o in self.operands)
        return f"[{self.timestamp:%H:%M:%S}] {self.operation}({operands_str}) = {self.result}"


class CalculatorService:
    """Encapsulates arithmetic logic and calculation history."""

    def __init__(self) -> None:
        self._history: list[CalculationRecord] = []

    @property
    def history(self) -> tuple[CalculationRecord, ...]:
        return tuple(self._history)

    def compute(self, operation: Operation, *operands: float) -> float:
        """Perform the requested operation and record the result.

        Raises:
            DivisionByZeroError: On division/modulo by zero.
            InvalidOperationError: On invalid operand counts or domains.
        """
        handlers = {
            Operation.ADD: self._add,
            Operation.SUBTRACT: self._subtract,
            Operation.MULTIPLY: self._multiply,
            Operation.DIVIDE: self._divide,
            Operation.POWER: self._power,
            Operation.MODULO: self._modulo,
            Operation.SQUARE_ROOT: self._square_root,
        }
        handler = handlers.get(operation)
        if handler is None:
            raise InvalidOperationError(f"Unsupported operation: {operation}")

        result = handler(*operands)
        self._history.append(CalculationRecord(operation.label, operands, result))
        return result

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
            raise DivisionByZeroError("Cannot divide by zero.")
        return a / b

    @staticmethod
    def _power(a: float, b: float) -> float:
        return math.pow(a, b)

    @staticmethod
    def _modulo(a: float, b: float) -> float:
        if b == 0:
            raise DivisionByZeroError("Cannot compute modulo with a zero divisor.")
        return math.fmod(a, b)

    @staticmethod
    def _square_root(a: float) -> float:
        if a < 0:
            raise InvalidOperationError("Cannot take the square root of a negative number.")
        return math.sqrt(a)


def _read_float(prompt: str) -> float:
    while True:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print("Please enter a valid number.")


def _print_menu() -> None:
    print("\n==============================")
    print("        CALCULATOR")
    print("==============================")
    for op in Operation:
        print(f"{op.value}. {op.label}")
    print("H. Show history")
    print("0. Exit")


def _run_operation(service: CalculatorService, choice: str) -> None:
    try:
        operation = Operation(choice)
    except ValueError:
        print("Invalid choice. Please try again.")
        return

    try:
        if operation.is_unary:
            value = _read_float("Enter value: ")
            result = service.compute(operation, value)
        else:
            first = _read_float("Enter first number: ")
            second = _read_float("Enter second number: ")
            result = service.compute(operation, first, second)
        print(f"Result: {result}")
    except CalculatorError as exc:
        print(f"Error: {exc}")
    except OverflowError:
        print("Error: the result is too large to represent.")


def main() -> None:
    """Entry point for the interactive calculator CLI."""
    service = CalculatorService()
    print("Welcome to the Professional Calculator.")

    while True:
        _print_menu()
        choice = input("Select an option: ").strip().upper()

        if choice == "0":
            print("Goodbye.")
            break
        if choice == "H":
            if not service.history:
                print("No calculations yet.")
            for record in service.history:
                print(record.format())
            continue

        _run_operation(service, choice)


if __name__ == "__main__":
    main()
