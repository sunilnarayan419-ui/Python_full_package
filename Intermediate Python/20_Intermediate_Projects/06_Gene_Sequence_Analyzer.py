from __future__ import annotations

import logging
import re
from dataclasses import dataclass

from Bio.Seq import Seq

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

VALID_DNA_CHARACTERS = frozenset("ACGTN")


class InvalidSequenceError(Exception):
    """Raised when a sequence contains characters outside the accepted DNA alphabet."""


@dataclass(frozen=True, slots=True)
class CompositionReport:
    adenine: int
    cytosine: int
    guanine: int
    thymine: int
    unknown: int
    gc_percent: float


@dataclass(frozen=True, slots=True)
class SequenceSummary:
    length: int
    composition: CompositionReport
    reverse_complement: str
    transcript_rna: str
    protein_translation: str
    motif_positions: dict[str, tuple[int, ...]]


class SequenceValidator:
    """Validates raw DNA sequence input against the accepted nucleotide alphabet."""

    def __init__(self, allowed_characters: frozenset[str] = VALID_DNA_CHARACTERS) -> None:
        self._allowed_characters = allowed_characters

    def validate(self, raw_sequence: str) -> str:
        if not raw_sequence:
            raise InvalidSequenceError("Sequence cannot be empty.")

        normalized = raw_sequence.strip().upper()
        invalid_chars = set(normalized) - self._allowed_characters
        if invalid_chars:
            raise InvalidSequenceError(
                f"Sequence contains invalid characters: {sorted(invalid_chars)}"
            )
        return normalized


class GeneSequenceAnalyzer:
    """Analyzes validated DNA sequences using Biopython primitives."""

    def __init__(self, validator: SequenceValidator | None = None) -> None:
        self._validator = validator or SequenceValidator()

    def composition(self, sequence: str) -> CompositionReport:
        length = len(sequence)
        a = sequence.count("A")
        c = sequence.count("C")
        g = sequence.count("G")
        t = sequence.count("T")
        n = sequence.count("N")
        gc_count = g + c
        gc_percent = round((gc_count / length) * 100, 2) if length else 0.0
        return CompositionReport(
            adenine=a, cytosine=c, guanine=g, thymine=t, unknown=n, gc_percent=gc_percent
        )

    def reverse_complement(self, sequence: str) -> str:
        seq_obj = Seq(sequence.replace("N", ""))
        return str(seq_obj.reverse_complement())

    def transcribe(self, sequence: str) -> str:
        seq_obj = Seq(sequence.replace("N", ""))
        return str(seq_obj.transcribe())

    def translate(self, sequence: str) -> str:
        coding_length = len(sequence) - (len(sequence) % 3)
        if coding_length == 0:
            return ""
        seq_obj = Seq(sequence[:coding_length].replace("N", ""))
        if len(seq_obj) % 3 != 0:
            return ""
        return str(seq_obj.translate(to_stop=False))

    def find_motif(self, sequence: str, motif: str) -> tuple[int, ...]:
        motif = motif.strip().upper()
        if not motif:
            return ()
        positions = [match.start() for match in re.finditer(f"(?={re.escape(motif)})", sequence)]
        return tuple(positions)

    def summarize(self, raw_sequence: str, motifs: tuple[str, ...] = ("ATG", "TATA")) -> SequenceSummary:
        sequence = self._validator.validate(raw_sequence)
        composition = self.composition(sequence)
        motif_positions = {motif: self.find_motif(sequence, motif) for motif in motifs}

        return SequenceSummary(
            length=len(sequence),
            composition=composition,
            reverse_complement=self.reverse_complement(sequence),
            transcript_rna=self.transcribe(sequence),
            protein_translation=self.translate(sequence),
            motif_positions=motif_positions,
        )


def run() -> SequenceSummary:
    """Runs the gene sequence analyzer against a controlled example sequence."""
    example_sequence = "ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAGNNATGTTTAAACGGGATCC"

    analyzer = GeneSequenceAnalyzer()
    try:
        summary = analyzer.summarize(example_sequence)
    except InvalidSequenceError:
        logger.exception("Sequence validation failed.")
        raise

    logger.info("Length: %d", summary.length)
    logger.info("Composition: %s", summary.composition)
    logger.info("Reverse complement: %s", summary.reverse_complement)
    logger.info("Transcript (RNA): %s", summary.transcript_rna)
    logger.info("Protein translation: %s", summary.protein_translation)
    logger.info("Motif positions: %s", summary.motif_positions)

    return summary


if __name__ == "__main__":
    run()
