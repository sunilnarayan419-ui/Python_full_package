from __future__ import annotations

from dataclasses import dataclass, field

from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.SeqUtils import gc_fraction


@dataclass
class SequenceSummary:
    """Structured summary of a biological sequence."""

    identifier: str
    alphabet_type: str
    length: int
    gc_content: float | None


class BiopythonSequenceWorkflow:
    """Industry-level workflow for core Biopython sequence operations.

    Wraps Bio.Seq / Bio.SeqRecord functionality used in production
    bioinformatics pipelines: transcription, translation, reverse
    complementation, and sequence metadata extraction.
    """

    _VALID_DNA = frozenset("ACGTN")
    _VALID_RNA = frozenset("ACGUN")
    _VALID_PROTEIN = frozenset("ACDEFGHIKLMNPQRSTVWYBXZJUO*")

    def __init__(self, sequence: str, identifier: str, molecule_type: str) -> None:
        """Initialize with a raw sequence string, its identifier and molecule type.

        Args:
            sequence: Raw biological sequence characters.
            identifier: Accession-style identifier (e.g. GenBank/RefSeq style).
            molecule_type: One of {"DNA", "RNA", "protein"}.
        """
        self.molecule_type = molecule_type.upper()
        if self.molecule_type not in {"DNA", "RNA", "PROTEIN"}:
            raise ValueError(f"Unsupported molecule_type: {molecule_type!r}")

        normalized = sequence.strip().upper()
        if not self.validate_sequence(normalized, self.molecule_type):
            raise ValueError(f"Sequence contains invalid characters for {molecule_type}")

        self.record: SeqRecord = SeqRecord(
            Seq(normalized),
            id=identifier,
            name=identifier,
            description=f"{molecule_type} sequence loaded via BiopythonSequenceWorkflow",
        )

    @staticmethod
    def validate_sequence(sequence: str, molecule_type: str) -> bool:
        """Validate that a sequence only contains symbols legal for its type."""
        if not sequence:
            return False
        alphabet = {
            "DNA": BiopythonSequenceWorkflow._VALID_DNA,
            "RNA": BiopythonSequenceWorkflow._VALID_RNA,
            "PROTEIN": BiopythonSequenceWorkflow._VALID_PROTEIN,
        }[molecule_type]
        return set(sequence).issubset(alphabet)

    def sequence_summary(self) -> SequenceSummary:
        """Return structured metadata describing the loaded sequence."""
        gc: float | None = None
        if self.molecule_type in {"DNA", "RNA"}:
            gc = round(float(gc_fraction(self.record.seq)) * 100.0, 2)
        return SequenceSummary(
            identifier=str(self.record.id),
            alphabet_type=self.molecule_type,
            length=len(self.record.seq),
            gc_content=gc,
        )

    def transcribe_sequence(self) -> Seq:
        """Transcribe a coding DNA strand into mRNA (DNA -> RNA only)."""
        if self.molecule_type != "DNA":
            raise ValueError("Transcription requires a DNA sequence")
        return self.record.seq.transcribe()

    def translate_sequence(self, to_stop: bool = True, table: int = 1) -> Seq:
        """Translate a DNA or RNA sequence into a protein sequence.

        Args:
            to_stop: Stop translation at the first stop codon.
            table: NCBI genetic code table identifier.
        """
        if self.molecule_type not in {"DNA", "RNA"}:
            raise ValueError("Translation requires a DNA or RNA sequence")
        return self.record.seq.translate(table=table, to_stop=to_stop)

    def reverse_complement(self) -> Seq:
        """Compute the reverse complement of a DNA or RNA sequence."""
        if self.molecule_type not in {"DNA", "RNA"}:
            raise ValueError("Reverse complement requires a DNA or RNA sequence")
        return self.record.seq.reverse_complement()

    @staticmethod
    def run() -> None:
        """Demonstrate the core Biopython sequence workflow end to end."""
        coding_strand = (
            "ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAGCGCTAATTCGGCTAGCA"
            "TCTAGCTAGCTAGCTAGCTAA"
        )
        workflow = BiopythonSequenceWorkflow(
            sequence=coding_strand,
            identifier="NM_000546.6_mock_cds",
            molecule_type="DNA",
        )

        summary = workflow.sequence_summary()
        print("Sequence summary:", summary)

        mrna = workflow.transcribe_sequence()
        print("mRNA transcript:", mrna)

        protein = workflow.translate_sequence(to_stop=True)
        print("Translated protein:", protein)

        rev_comp = workflow.reverse_complement()
        print("Reverse complement:", rev_comp)

        protein_workflow = BiopythonSequenceWorkflow(
            sequence=str(protein) if protein else "MAIV*",
            identifier="mock_protein_product",
            molecule_type="protein",
        )
        print("Protein summary:", protein_workflow.sequence_summary())


if __name__ == "__main__":
    BiopythonSequenceWorkflow.run()
