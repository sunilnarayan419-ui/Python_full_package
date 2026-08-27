"""
bioutils.sequence_tools

Reusable DNA sequence utilities.
"""

_COMPLEMENT_MAP = {"A": "T", "T": "A", "G": "C", "C": "G"}


def gc_content(sequence: str) -> float:
    """Return the GC content of a DNA sequence as a percentage."""
    if not sequence:
        raise ValueError("sequence must be a non-empty string.")

    sequence = sequence.upper()
    gc_count = sum(1 for base in sequence if base in ("G", "C"))
    return gc_count / len(sequence) * 100


def reverse_complement(sequence: str) -> str:
    """Return the reverse complement of a DNA sequence."""
    if not sequence:
        raise ValueError("sequence must be a non-empty string.")

    sequence = sequence.upper()
    try:
        complemented = [_COMPLEMENT_MAP[base] for base in sequence]
    except KeyError as error:
        raise ValueError(f"Invalid DNA base encountered: {error.args[0]}") from error

    return "".join(reversed(complemented))
