from __future__ import annotations

from dataclasses import dataclass
from io import StringIO

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.SeqUtils import gc_fraction

# Small multi-contig mock draft-genome assembly (illustrative only,
# not representative of a real organism's genome).
_MOCK_ASSEMBLY_FASTA = """\
>contig_001 length=180
ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAGCGCTAATTCGGCTAGCATCT
AGCTAGCTAGCTAGCTAAATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAGCG
CTAATTCGGCTAGCATCTAGCTAGCTAGCTAGCTAAATGGCCATTGTAATGGGCCGCTG
>contig_002 length=90
GGGCCCGGGAAATTTCCCGGGAAATTTGGGCCCTTTAAACCCGGGTTTAAACCCGGGAA
ATTTCCCGGGAAATTTGGGCCC
>contig_003 length=45
ATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATG
>contig_004 length=260
ATGAAACGCATTAGCACCACCATTACCACCACCATCACCATTACCACAGGTAACGGTG
CGGGCTGACGCGTACAGGAAACACAGAAAAAAGCCCGCACCTGACAGTGCGGGCTTTTT
TTTTCGACCAAAGGTAACGAGGTAACAACCATGCGAGTGTTGAAGTTCGGCGGTACATC
AGTGGCAAATGCAGAACGTTTTCTGCGTGTTGCCGATATTCTGGAAAGCAATGCCAGGC
"""


@dataclass
class GenomeAssemblyStats:
    """Aggregate contig-level statistics for a draft genome assembly."""

    contig_count: int
    total_length: int
    gc_percent: float
    min_contig_length: int
    max_contig_length: int
    mean_contig_length: float
    n50: int


@dataclass
class OpenReadingFrame:
    """Structured representation of a detected open reading frame."""

    contig_id: str
    strand: str
    frame: int
    start: int
    end: int
    length_nt: int


class GenomeAnalysisWorkflow:
    """Industry-level genome/contig analysis workflow using Biopython.

    Computes assembly-level statistics (GC%, N50, length distribution)
    and performs simple ORF detection across a multi-contig FASTA input,
    reusable for real assembler output.
    """

    _START_CODON = "ATG"
    _STOP_CODONS = {"TAA", "TAG", "TGA"}

    def __init__(self, assembly_fasta: str) -> None:
        """Initialize by parsing a multi-contig FASTA assembly.

        Args:
            assembly_fasta: Raw FASTA text containing one or more contigs.
        """
        self.contigs: list[SeqRecord] = list(SeqIO.parse(StringIO(assembly_fasta), "fasta"))
        if not self.contigs:
            raise ValueError("No contigs parsed from assembly FASTA input")

    def contig_lengths(self) -> list[int]:
        """Return the length of every contig in the assembly."""
        return [len(contig.seq) for contig in self.contigs]

    @staticmethod
    def _compute_n50(lengths: list[int]) -> int:
        """Compute the N50 statistic from a list of contig lengths."""
        sorted_lengths = sorted(lengths, reverse=True)
        total = sum(sorted_lengths)
        cumulative = 0
        half_total = total / 2.0
        for length in sorted_lengths:
            cumulative += length
            if cumulative >= half_total:
                return length
        return 0

    def assembly_statistics(self) -> GenomeAssemblyStats:
        """Compute standard assembly-level statistics across all contigs."""
        lengths = self.contig_lengths()
        concatenated_seq = "".join(str(contig.seq) for contig in self.contigs)
        gc_percent = round(float(gc_fraction(Seq(concatenated_seq))) * 100.0, 2)

        return GenomeAssemblyStats(
            contig_count=len(lengths),
            total_length=sum(lengths),
            gc_percent=gc_percent,
            min_contig_length=min(lengths),
            max_contig_length=max(lengths),
            mean_contig_length=round(sum(lengths) / len(lengths), 2),
            n50=self._compute_n50(lengths),
        )

    def nucleotide_composition(self) -> dict[str, int]:
        """Compute raw nucleotide counts across the entire assembly."""
        counts = {"A": 0, "C": 0, "G": 0, "T": 0, "N": 0, "other": 0}
        for contig in self.contigs:
            for base in str(contig.seq).upper():
                if base in counts:
                    counts[base] += 1
                else:
                    counts["other"] += 1
        return counts

    def find_orfs(self, min_length_nt: int = 90) -> list[OpenReadingFrame]:
        """Detect simple open reading frames across all six reading frames.

        Args:
            min_length_nt: Minimum ORF length in nucleotides (including stop codon)
                to be reported.
        """
        orfs: list[OpenReadingFrame] = []
        for contig in self.contigs:
            for strand_label, seq in (("forward", contig.seq), ("reverse", contig.seq.reverse_complement())):
                sequence_str = str(seq).upper()
                for frame in range(3):
                    orfs.extend(
                        self._scan_frame(
                            sequence_str, contig.id, strand_label, frame, min_length_nt
                        )
                    )
        return orfs

    def _scan_frame(
        self, sequence: str, contig_id: str, strand: str, frame: int, min_length_nt: int
    ) -> list[OpenReadingFrame]:
        """Scan a single reading frame for start/stop codon-delimited ORFs."""
        found: list[OpenReadingFrame] = []
        codon_start: int | None = None
        position = frame
        while position + 3 <= len(sequence):
            codon = sequence[position:position + 3]
            if codon_start is None and codon == self._START_CODON:
                codon_start = position
            elif codon_start is not None and codon in self._STOP_CODONS:
                orf_length = position + 3 - codon_start
                if orf_length >= min_length_nt:
                    found.append(
                        OpenReadingFrame(
                            contig_id=contig_id,
                            strand=strand,
                            frame=frame,
                            start=codon_start,
                            end=position + 3,
                            length_nt=orf_length,
                        )
                    )
                codon_start = None
            position += 3
        return found

    @staticmethod
    def run() -> None:
        """Demonstrate assembly statistics, composition, and ORF detection."""
        workflow = GenomeAnalysisWorkflow(_MOCK_ASSEMBLY_FASTA)

        stats = workflow.assembly_statistics()
        print("Assembly statistics:", stats)

        composition = workflow.nucleotide_composition()
        print("Nucleotide composition:", composition)

        orfs = workflow.find_orfs(min_length_nt=60)
        print(f"Detected {len(orfs)} candidate ORFs (min 60 nt):")
        for orf in orfs:
            print(
                f"  {orf.contig_id} [{orf.strand} frame {orf.frame}] "
                f"{orf.start}-{orf.end} ({orf.length_nt} nt)"
            )


if __name__ == "__main__":
    GenomeAnalysisWorkflow.run()
