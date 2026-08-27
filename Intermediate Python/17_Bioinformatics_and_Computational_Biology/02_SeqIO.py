from __future__ import annotations

from io import StringIO

from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

_MOCK_FASTA = """\
>NP_000537.3 cellular tumor antigen p53 [Homo sapiens]
MEEPQSDPSVEPPLSQETFSDLWKLLPENNVLSPLPSQAMDDLMLSPDDIEQWFTEDPG
>NP_004439.2 receptor tyrosine-protein kinase erbB-2 [Homo sapiens]
MELAALCRWGLLLALLPPGAASTQVCTGTDMKLRLPASPETHLDMLRHLYQGCQVVQGN
>NP_001333827.1 hypothetical short peptide [Homo sapiens]
MEEP
>XP_016869030.1 mock low-complexity fragment [Homo sapiens]
MEEPQSDPSVEPPLSQETFSDLWKLLPENNVLSPLPSQAMDDLMLSPDDIEQWFTEDPG
"""

_MOCK_GENBANK = """\
LOCUS       NM_000546               2591 bp    mRNA    linear   PRI 01-JAN-2024
DEFINITION  Homo sapiens tumor protein p53 (TP53), mRNA.
ACCESSION   NM_000546
VERSION     NM_000546.6
SOURCE      Homo sapiens (human)
FEATURES             Location/Qualifiers
     source          1..2591
                     /organism="Homo sapiens"
     gene            1..2591
                     /gene="TP53"
     CDS             203..1384
                     /gene="TP53"
                     /product="cellular tumor antigen p53"
ORIGIN
        1 atgggcatgg gccgcgagcc atgtgctgat cgccgcgcgc gcgctagcta gctacgcgcg
       61 cgcgctacgc gcgcgcatgc gctagctagc tagctagcta gctagctagc tagctagcta
      121 gctagctagc tagctagcta gctagctagc tagctagcta gctagctagc tagctagcta
      181 gctagctagc tagctagcta gctatgacgg aggttcacgt actgtcagag gcagcgaggg
      241 gcccagcctg ggtccctgcc gcagctcgat gcagagacca agcaagacct cagcggaggc
      301 taatcaggac cccaaaatgg ccatcgtaac ggcctagcta gctagctagc tagctagcta
      361 gctagctaaa aaaaaaaaaa aaaaaaaaaa aaaaaaaaaa aaaaaaaaaa aaaaaaaaaa
//
"""


class SeqIOWorkflow:
    """Industry-level sequence input/output workflow built on Bio.SeqIO.

    Encapsulates parsing, filtering, summarization, and controlled
    writing of biological sequence records without depending on any
    machine-specific filesystem path.
    """

    def __init__(self, source_handle: StringIO, file_format: str) -> None:
        """Initialize with an in-memory file-like handle and its format.

        Args:
            source_handle: A StringIO (or compatible) handle to parse.
            file_format: Bio.SeqIO format identifier (e.g. "fasta", "genbank").
        """
        self.file_format = file_format
        self._records: list[SeqRecord] = list(SeqIO.parse(source_handle, file_format))
        if not self._records:
            raise ValueError(f"No records parsed from {file_format!r} source")

    def parse_records(self) -> list[SeqRecord]:
        """Return the parsed sequence records held by this workflow."""
        return self._records

    def filter_records(
        self,
        min_length: int = 0,
        max_length: int | None = None,
        id_contains: str | None = None,
    ) -> list[SeqRecord]:
        """Filter records by sequence length and optional identifier substring.

        Args:
            min_length: Minimum acceptable sequence length, inclusive.
            max_length: Maximum acceptable sequence length, inclusive; None disables the cap.
            id_contains: Optional substring that must appear in the record id.
        """
        filtered: list[SeqRecord] = []
        for record in self._records:
            length_ok = len(record.seq) >= min_length and (
                max_length is None or len(record.seq) <= max_length
            )
            id_ok = id_contains is None or id_contains in record.id
            if length_ok and id_ok:
                filtered.append(record)
        return filtered

    def summarize_records(self) -> dict[str, float | int]:
        """Compute aggregate length statistics across all parsed records."""
        lengths = [len(record.seq) for record in self._records]
        return {
            "record_count": len(lengths),
            "min_length": min(lengths),
            "max_length": max(lengths),
            "mean_length": round(sum(lengths) / len(lengths), 2),
            "total_length": sum(lengths),
        }

    @staticmethod
    def deduplicate_by_sequence(records: list[SeqRecord]) -> list[SeqRecord]:
        """Remove records whose sequence string has already been observed."""
        seen: set[str] = set()
        unique: list[SeqRecord] = []
        for record in records:
            sequence_str = str(record.seq)
            if sequence_str not in seen:
                seen.add(sequence_str)
                unique.append(record)
        return unique

    @staticmethod
    def write_records(records: list[SeqRecord], file_format: str) -> str:
        """Serialize records back out to a string in the given format."""
        buffer = StringIO()
        SeqIO.write(records, buffer, file_format)
        return buffer.getvalue()

    @staticmethod
    def run() -> None:
        """Demonstrate a full parse -> filter -> summarize -> write cycle."""
        fasta_workflow = SeqIOWorkflow(StringIO(_MOCK_FASTA), "fasta")
        all_records = fasta_workflow.parse_records()
        print(f"Parsed {len(all_records)} FASTA records")

        long_records = fasta_workflow.filter_records(min_length=20)
        print(f"Records with length >= 20: {len(long_records)}")

        unique_records = SeqIOWorkflow.deduplicate_by_sequence(all_records)
        print(f"Unique sequences after deduplication: {len(unique_records)}")

        print("Length statistics:", fasta_workflow.summarize_records())

        output_fasta = SeqIOWorkflow.write_records(unique_records, "fasta")
        print("Re-serialized FASTA (first 120 chars):")
        print(output_fasta[:120])

        genbank_workflow = SeqIOWorkflow(StringIO(_MOCK_GENBANK), "genbank")
        gb_record = genbank_workflow.parse_records()[0]
        print(f"GenBank record {gb_record.id}: {len(gb_record.seq)} bp, "
              f"{len(gb_record.features)} features")


if __name__ == "__main__":
    SeqIOWorkflow.run()
