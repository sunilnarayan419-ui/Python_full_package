"""Core sequence-validation and summarization logic."""
from __future__ import annotations

from dataclasses import dataclass

_VALID_DNA_BASES = frozenset("ACGTN")


class InvalidSequenceError(ValueError):
    pass


def validate_sequence(sequence: str, *, alphabet: frozenset[str] = _VALID_DNA_BASES) -> None:
    if not sequence:
        raise InvalidSequenceError("sequence must not be empty")
    invalid = set(sequence.upper()) - alphabet
    if invalid:
        raise InvalidSequenceError(f"sequence contains invalid characters: {sorted(invalid)}")


@dataclass(frozen=True, slots=True)
class SequenceStats:
    length: int
    gc_content: float
    base_counts: dict[str, int]


def summarize(sequence: str) -> SequenceStats:
    validate_sequence(sequence)
    upper = sequence.upper()
    base_counts = {base: upper.count(base) for base in sorted(set(upper))}
    gc_count = base_counts.get("G", 0) + base_counts.get("C", 0)
    return SequenceStats(length=len(upper), gc_content=gc_count / len(upper), base_counts=base_counts)
