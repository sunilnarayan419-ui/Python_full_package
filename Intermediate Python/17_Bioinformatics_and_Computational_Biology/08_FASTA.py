from __future__ import annotations

from dataclasses import dataclass
from io import StringIO

from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.SeqUtils import gc_fraction

_MOCK_DNA_FASTA = """\
>NM_000546.6 Homo sapiens TP53 mRNA fragment
ATGGAGGAGCCGCAGTCAGATCCTAGCGTCGAGCCCCCTCTGAGTCAGGAAACATTTTC
>nm_007294.4 homo sapiens brca1 mrna fragment lowercase-id
atggatttatctgctcttcgcgttgaagaagtacaaaatgtcattaatgctatgcagaa
>NM_000546.6_duplicate Homo sapiens TP53 mRNA fragment duplicate
ATGGAGGAGCCGCAGTCAGATCCTAGCGTCGAGCCCCCTCTGAGTCAGGAAACATTTTC
>XR_001737536.1 short noncoding fragment
ATGC
"""

_MOCK_PROTEIN_FASTA = """\
>NP_000537.3 cellular tumor antigen p53 [Homo sapiens]
MEEPQSDPSVEPPLSQETFSDLWKLLPENNVLSPLPSQAMDDLMLSPDDIEQWFTEDPG
>NP_009225.1 breast cancer type 1 susceptibility protein [Homo sapiens]
MDLSALRVEEVQNVINAMQKILECPICLELIKEPVSTKCDHIFCKFCMLKLLNQKKGPS
"""


@dataclass
class FastaLengthStats:
    """Aggregate length statistics for a set of FASTA records."""

    record_count: int
    min_length: int
    max_length: int
    mean_length: float


class FastaWorkflow:
    """Industry-level FASTA processing workflow using Bio.SeqIO.

    Distinguishes DNA from protein records so that GC-content and other
    nucleotide-specific transformations are never applied to protein
    sequences.
    """

    _VALID_DNA = frozenset("ACGTN")
    _VALID_PROTEIN = frozenset("ACDEFGHIKLMNPQRSTVWYBXZJUO*")

    def __init__(self, fasta_text: str, sequence_type: str) -> None:
        """Initialize by parsing FASTA text of a declared sequence type.

        Args:
            fasta_text: Raw FASTA-format content.
            sequence_type: One of {"DNA", "protein"}.
        """
        self.sequence_type = sequence_type.upper()
        if self.sequence_type not in {"DNA", "PROTEIN"}:
            raise ValueError(f"Unsupported sequence_type: {sequence_type!r}")

        self.records: list[SeqRecord] = list(SeqIO.parse(StringIO(fasta_text), "fasta"))
        if not self.records:
            raise ValueError("No FASTA records parsed from input")

    def validate_records(self) -> dict[str, bool]:
        """Validate every record's sequence characters against its declared type.

        Returns:
            Mapping of record id -> whether the sequence is valid for its type.
        """
        alphabet = self._VALID_DNA if self.sequence_type == "DNA" else self._VALID_PROTEIN
        return {
            record.id: set(str(record.seq).upper()).issubset(alphabet)
            for record in self.records
        }

    def normalize_records(self) -> list[SeqRecord]:
        """Return records with sequences upper-cased and IDs stripped of whitespace.

        Note: normalization never alters the biological alphabet, only
        casing and identifier formatting.
        """
        normalized: list[SeqRecord] = []
        for record in self.records:
            new_record = record[:]
            new_record.seq = record.seq.upper()
            new_record.id = record.id.strip()
            normalized.append(new_record)
        return normalized

    def filter_records(self, min_length: int) -> list[SeqRecord]:
        """Filter out records shorter than a minimum length.

        Args:
            min_length: Minimum sequence length, inclusive.
        """
        return [r for r in self.records if len(r.seq) >= min_length]

    def length_statistics(self) -> FastaLengthStats:
        """Compute aggregate length statistics across all parsed records."""
        lengths = [len(r.seq) for r in self.records]
        return FastaLengthStats(
            record_count=len(lengths),
            min_length=min(lengths),
            max_length=max(lengths),
            mean_length=round(sum(lengths) / len(lengths), 2),
        )

    def gc_content_by_record(self) -> dict[str, float]:
        """Compute GC content per record. DNA sequences only.

        Raises:
            ValueError: If called on a protein-typed workflow, to avoid
                corrupting protein sequences with a nucleotide-only metric.
        """
        if self.sequence_type != "DNA":
            raise ValueError("GC content is only defined for DNA sequences")
        return {
            record.id: round(float(gc_fraction(record.seq)) * 100.0, 2)
            for record in self.records
        }

    def find_duplicate_sequences(self) -> dict[str, list[str]]:
        """Group record ids that share an identical sequence string."""
        groups: dict[str, list[str]] = {}
        for record in self.records:
            sequence_str = str(record.seq).upper()
            groups.setdefault(sequence_str, []).append(record.id)
        return {seq: ids for seq, ids in groups.items() if len(ids) > 1}

    @staticmethod
    def to_fasta_string(records: list[SeqRecord]) -> str:
        """Serialize a list of records back to FASTA-format text."""
        buffer = StringIO()
        SeqIO.write(records, buffer, "fasta")
        return buffer.getvalue()

    @staticmethod
    def run() -> None:
        """Demonstrate validation, normalization, statistics, and dedup on DNA and protein FASTA."""
        dna_workflow = FastaWorkflow(_MOCK_DNA_FASTA, sequence_type="DNA")
        print("DNA record validity:", dna_workflow.validate_records())
        print("DNA length statistics:", dna_workflow.length_statistics())
        print("DNA GC content by record:", dna_workflow.gc_content_by_record())
        print("Duplicate DNA sequences:", dna_workflow.find_duplicate_sequences())

        filtered = dna_workflow.filter_records(min_length=10)
        print(f"DNA records with length >= 10: {len(filtered)}")

        protein_workflow = FastaWorkflow(_MOCK_PROTEIN_FASTA, sequence_type="PROTEIN")
        print("Protein record validity:", protein_workflow.validate_records())
        print("Protein length statistics:", protein_workflow.length_statistics())

        try:
            protein_workflow.gc_content_by_record()
        except ValueError as exc:
            print(f"Expected guard triggered: {exc}")

        normalized = dna_workflow.normalize_records()
        print("Normalized FASTA output (first 100 chars):")
        print(FastaWorkflow.to_fasta_string(normalized)[:100])


if __name__ == "__main__":
    FastaWorkflow.run()
