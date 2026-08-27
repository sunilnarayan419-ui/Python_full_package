"""
11_Magic_Methods.py

Concept: Magic Methods
Special ("dunder") methods let custom objects integrate naturally with
Python's built-in protocols: printing, len(), comparisons, iteration,
membership testing, and context management. This file selects a
purposeful subset at each level rather than implementing every possible
magic method.
"""

from __future__ import annotations

from typing import Iterator


# --------------------------------------------------------------------------- #
# University Level
# --------------------------------------------------------------------------- #
class UniversityMagicMethods:
    """Focuses on __init__, __str__, and __len__ for a DNA sequence
    wrapper."""

    def __init__(self, sequence: str) -> None:
        self.sequence = sequence.upper()

    def __str__(self) -> str:
        return f"DNASequence('{self.sequence}')"

    def __len__(self) -> int:
        return len(self.sequence)

    @staticmethod
    def run() -> None:
        print("--- UniversityMagicMethods ---")
        seq = UniversityMagicMethods("acgtacgt")
        print(str(seq))
        print(f"Length: {len(seq)}")


# --------------------------------------------------------------------------- #
# Interview Level
# --------------------------------------------------------------------------- #
class InterviewMagicMethods:
    """Adds comparison (__eq__, __lt__) and iteration (__iter__) behavior
    for a gene-expression record, so records can be sorted and compared
    naturally with built-in operators."""

    def __init__(self, gene_symbol: str, expression_level: float) -> None:
        if expression_level < 0:
            raise ValueError("expression_level cannot be negative")
        self.gene_symbol = gene_symbol
        self.expression_level = expression_level

    def __str__(self) -> str:
        return f"{self.gene_symbol}={self.expression_level:.2f}"

    def __repr__(self) -> str:
        return f"InterviewMagicMethods({self.gene_symbol!r}, {self.expression_level!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, InterviewMagicMethods):
            return NotImplemented
        return (
            self.gene_symbol == other.gene_symbol
            and self.expression_level == other.expression_level
        )

    def __lt__(self, other: "InterviewMagicMethods") -> bool:
        if not isinstance(other, InterviewMagicMethods):
            return NotImplemented
        return self.expression_level < other.expression_level

    @staticmethod
    def run() -> None:
        print("--- InterviewMagicMethods ---")
        records = [
            InterviewMagicMethods("GAPDH", 12.4),
            InterviewMagicMethods("ACTB", 30.1),
            InterviewMagicMethods("TP53", 5.9),
        ]
        print(sorted(records))
        print(f"Equal? {records[0] == InterviewMagicMethods('GAPDH', 12.4)}")


# --------------------------------------------------------------------------- #
# Industry Level
# --------------------------------------------------------------------------- #
class IndustryMagicMethods:
    """Designs a small collection of experiment readings that naturally
    integrates with Python protocols: iteration, membership testing
    (__contains__), and context management (__enter__/__exit__) to
    represent an open measurement session that must be explicitly closed.

    Operators are only overloaded where they add real clarity, not
    merely because Python allows it.
    """

    def __init__(self, session_name: str) -> None:
        if not session_name.strip():
            raise ValueError("session_name cannot be empty")
        self.session_name = session_name
        self._readings: list[float] = []
        self._is_open = False

    def __str__(self) -> str:
        return f"MeasurementSession('{self.session_name}', {len(self)} readings)"

    def __len__(self) -> int:
        return len(self._readings)

    def __iter__(self) -> Iterator[float]:
        return iter(self._readings)

    def __contains__(self, value: float) -> bool:
        return value in self._readings

    def __enter__(self) -> "IndustryMagicMethods":
        self._is_open = True
        return self

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None:
        self._is_open = False

    def record(self, value: float) -> None:
        if not self._is_open:
            raise RuntimeError("session must be open (use 'with') to record readings")
        if value < 0:
            raise ValueError("value cannot be negative")
        self._readings.append(value)

    @staticmethod
    def run() -> None:
        print("--- IndustryMagicMethods ---")
        with IndustryMagicMethods("Fluorescence Assay") as session:
            session.record(0.42)
            session.record(0.58)
            session.record(0.31)

            print(session)
            print(f"Readings: {list(session)}")
            print(f"Contains 0.58? {0.58 in session}")

        try:
            session.record(0.10)
        except RuntimeError as error:
            print(f"Rejected write after session closed: {error}")


if __name__ == "__main__":
    UniversityMagicMethods.run()
    InterviewMagicMethods.run()
    IndustryMagicMethods.run()
