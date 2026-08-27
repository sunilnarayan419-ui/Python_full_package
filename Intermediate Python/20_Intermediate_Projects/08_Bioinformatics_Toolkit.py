from __future__ import annotations

import io
import logging
from dataclasses import dataclass

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqUtils.ProtParam import ProteinAnalysis

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

VALID_DNA_CHARACTERS = frozenset("ACGTN")
VALID_PROTEIN_CHARACTERS = frozenset("ACDEFGHIKLMNPQRSTVWY")


class ToolkitError(Exception):
    """Base error for bioinformatics toolkit failures."""


class SequenceValidationError(ToolkitError):
    """Raised when a sequence fails alphabet validation."""


@dataclass(frozen=True, slots=True)
class SequenceRecord:
    identifier: str
    description: str
    sequence: str


@dataclass(frozen=True, slots=True)
class SequenceStatistics:
    identifier: str
    length: int
    gc_percent: float


@dataclass(frozen=True, slots=True)
class ProteinProperties:
    identifier: str
    molecular_weight: float
    isoelectric_point: float
    instability_index: float
    aromaticity: float


class FastaParser:
    """Parses FASTA-formatted text into sequence records."""

    def parse(self, fasta_text: str) -> list[SequenceRecord]:
        if not fasta_text.strip():
            raise ToolkitError("FASTA content is empty.")
        handle = io.StringIO(fasta_text)
        records = [
            SequenceRecord(
                identifier=record.id,
                description=record.description,
                sequence=str(record.seq).upper(),
            )
            for record in SeqIO.parse(handle, "fasta")
        ]
        if not records:
            raise ToolkitError("No valid FASTA records were found.")
        return records


class SequenceValidationService:
    """Validates DNA and protein sequences against their expected alphabets."""

    def validate_dna(self, sequence: str) -> None:
        invalid = set(sequence) - VALID_DNA_CHARACTERS
        if invalid:
            raise SequenceValidationError(f"Invalid DNA characters found: {sorted(invalid)}")

    def validate_protein(self, sequence: str) -> None:
        invalid = set(sequence) - VALID_PROTEIN_CHARACTERS
        if invalid:
            raise SequenceValidationError(f"Invalid protein characters found: {sorted(invalid)}")

    def is_valid_dna(self, sequence: str) -> bool:
        return not (set(sequence) - VALID_DNA_CHARACTERS)


class SequenceStatisticsService:
    """Computes basic descriptive statistics for nucleotide sequences."""

    def compute(self, record: SequenceRecord) -> SequenceStatistics:
        length = len(record.sequence)
        gc_count = record.sequence.count("G") + record.sequence.count("C")
        gc_percent = round((gc_count / length) * 100, 2) if length else 0.0
        return SequenceStatistics(identifier=record.identifier, length=length, gc_percent=gc_percent)


class ProteinPropertyService:
    """Computes physicochemical properties for protein sequences."""

    def compute(self, record: SequenceRecord) -> ProteinProperties:
        analysis = ProteinAnalysis(record.sequence)
        return ProteinProperties(
            identifier=record.identifier,
            molecular_weight=round(analysis.molecular_weight(), 2),
            isoelectric_point=round(analysis.isoelectric_point(), 2),
            instability_index=round(analysis.instability_index(), 2),
            aromaticity=round(analysis.aromaticity(), 4),
        )


class MotifSearchService:
    """Searches sequences for exact motif occurrences."""

    def find_positions(self, sequence: str, motif: str) -> tuple[int, ...]:
        motif = motif.upper()
        positions: list[int] = []
        start = 0
        while True:
            index = sequence.find(motif, start)
            if index == -1:
                break
            positions.append(index)
            start = index + 1
        return tuple(positions)


class SequenceFilterService:
    """Filters collections of sequence records by simple criteria."""

    def filter_by_min_length(self, records: list[SequenceRecord], minimum_length: int) -> list[SequenceRecord]:
        return [record for record in records if len(record.sequence) >= minimum_length]

    def filter_by_gc_content(
        self, records: list[SequenceRecord], stats_service: SequenceStatisticsService, minimum_gc_percent: float
    ) -> list[SequenceRecord]:
        return [
            record
            for record in records
            if stats_service.compute(record).gc_percent >= minimum_gc_percent
        ]


class BioinformaticsToolkit:
    """Domain-oriented facade combining FASTA parsing, validation, and analysis."""

    def __init__(self) -> None:
        self.parser = FastaParser()
        self.validator = SequenceValidationService()
        self.dna_stats = SequenceStatisticsService()
        self.protein_stats = ProteinPropertyService()
        self.motif_search = MotifSearchService()
        self.filters = SequenceFilterService()

    def analyze_dna_fasta(self, fasta_text: str) -> list[SequenceStatistics]:
        records = self.parser.parse(fasta_text)
        results: list[SequenceStatistics] = []
        for record in records:
            self.validator.validate_dna(record.sequence)
            results.append(self.dna_stats.compute(record))
        return results

    def analyze_protein_fasta(self, fasta_text: str) -> list[ProteinProperties]:
        records = self.parser.parse(fasta_text)
        results: list[ProteinProperties] = []
        for record in records:
            self.validator.validate_protein(record.sequence)
            results.append(self.protein_stats.compute(record))
        return results


def _sample_dna_fasta() -> str:
    return (
        ">gene_A description=drought response regulator\n"
        "ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG\n"
        ">gene_B description=nitrogen transporter\n"
        "ATGGGCTATCGTTAGCCGGATCGGGCTTAACCGGTTAAA\n"
    )


def _sample_protein_fasta() -> str:
    return (
        ">protein_A description=heat shock protein fragment\n"
        "MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKAVQVKV\n"
    )


def run() -> tuple[list[SequenceStatistics], list[ProteinProperties]]:
    """Runs the bioinformatics toolkit against controlled FASTA examples."""
    toolkit = BioinformaticsToolkit()

    dna_stats = toolkit.analyze_dna_fasta(_sample_dna_fasta())
    for stat in dna_stats:
        logger.info("DNA record %s: length=%d, GC%%=%.2f", stat.identifier, stat.length, stat.gc_percent)

    protein_props = toolkit.analyze_protein_fasta(_sample_protein_fasta())
    for prop in protein_props:
        logger.info(
            "Protein record %s: MW=%.2f, pI=%.2f, instability=%.2f",
            prop.identifier, prop.molecular_weight, prop.isoelectric_point, prop.instability_index,
        )

    dna_records = toolkit.parser.parse(_sample_dna_fasta())
    motif_hits = toolkit.motif_search.find_positions(dna_records[0].sequence, "ATG")
    logger.info("Motif 'ATG' found in %s at positions: %s", dna_records[0].identifier, motif_hits)

    return dna_stats, protein_props


if __name__ == "__main__":
    run()
