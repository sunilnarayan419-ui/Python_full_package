"""Sequence quality-control utilities for a genomics ingestion pipeline.

This module documents WHAT each component does, WHY it exists, its
CONTRACT (inputs/outputs/exceptions), and any IMPORTANT BEHAVIOR a
caller must know -- matching the documentation style expected in a
production codebase rather than a tutorial.
"""

from __future__ import annotations

from dataclasses import dataclass


class InvalidSequenceError(ValueError):
    """Raised when a nucleotide sequence contains invalid characters
    or fails a length constraint.
    """


@dataclass(frozen=True, slots=True)
class QualityControlResult:
    """Outcome of a sequence quality-control check.

    Attributes:
        sequence_id: Identifier of the sequence that was checked.
        gc_fraction: Fraction of G/C bases, in the range [0.0, 1.0].
        passed: Whether the sequence met the configured GC-content bounds.
    """

    sequence_id: str
    gc_fraction: float
    passed: bool


class SequenceQualityChecker:
    """Evaluates whether nucleotide sequences meet GC-content quality bounds.

    WHY: sequences with extreme GC content are frequently associated
    with sequencing artifacts or contamination and are flagged for
    manual review rather than silently passed downstream.
    """

    _VALID_BASES = frozenset("ACGT")

    def __init__(self, min_gc_fraction: float, max_gc_fraction: float) -> None:
        """Initializes the checker with inclusive GC-fraction bounds.

        Args:
            min_gc_fraction: Minimum acceptable GC fraction, in [0.0, 1.0].
            max_gc_fraction: Maximum acceptable GC fraction, in [0.0, 1.0].

        Raises:
            ValueError: If bounds are outside [0.0, 1.0] or min exceeds max.
        """
        if not (0.0 <= min_gc_fraction <= max_gc_fraction <= 1.0):
            raise ValueError(
                "require 0.0 <= min_gc_fraction <= max_gc_fraction <= 1.0"
            )
        self._min_gc_fraction = min_gc_fraction
        self._max_gc_fraction = max_gc_fraction

    def check(self, sequence_id: str, sequence: str) -> QualityControlResult:
        """Checks a single sequence against the configured GC-content bounds.

        Args:
            sequence_id: Identifier used to trace this result back to its
                source read or sample.
            sequence: Nucleotide sequence composed only of A, C, G, T
                (case-insensitive).

        Returns:
            A QualityControlResult describing the computed GC fraction
            and whether it fell within bounds.

        Raises:
            InvalidSequenceError: If the sequence is empty or contains
                characters outside {A, C, G, T}.

        Important behavior:
            This method is pure -- it has no side effects and does not
            log, print, or mutate shared state, so it is safe to call
            concurrently across sequences.
        """
        normalized = sequence.upper()

        if not normalized:
            raise InvalidSequenceError(f"sequence '{sequence_id}' is empty")

        invalid_chars = set(normalized) - self._VALID_BASES
        if invalid_chars:
            raise InvalidSequenceError(
                f"sequence '{sequence_id}' contains invalid bases: {sorted(invalid_chars)}"
            )

        gc_fraction = sum(1 for base in normalized if base in "GC") / len(normalized)
        passed = self._min_gc_fraction <= gc_fraction <= self._max_gc_fraction

        return QualityControlResult(
            sequence_id=sequence_id, gc_fraction=gc_fraction, passed=passed
        )


if __name__ == "__main__":
    # Usage example, doubling as documentation of expected call shape.
    checker = SequenceQualityChecker(min_gc_fraction=0.35, max_gc_fraction=0.65)

    result = checker.check("READ-001", "ATGCATGCATGC")
    print(f"{result.sequence_id}: gc_fraction={result.gc_fraction:.2f} passed={result.passed}")
