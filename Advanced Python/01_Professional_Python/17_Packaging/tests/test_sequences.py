from __future__ import annotations

import pytest

from bioseqkit import summarize, validate_sequence
from bioseqkit.sequences import InvalidSequenceError


def test_validate_sequence_accepts_valid_dna() -> None:
    validate_sequence("ACGTN")


def test_validate_sequence_rejects_invalid_characters() -> None:
    with pytest.raises(InvalidSequenceError):
        validate_sequence("ACGTX")


def test_validate_sequence_rejects_empty_string() -> None:
    with pytest.raises(InvalidSequenceError):
        validate_sequence("")


def test_summarize_computes_gc_content_and_counts() -> None:
    stats = summarize("GGCC")
    assert stats.length == 4
    assert stats.gc_content == 1.0
    assert stats.base_counts == {"C": 2, "G": 2}
