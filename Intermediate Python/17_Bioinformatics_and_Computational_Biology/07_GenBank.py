from __future__ import annotations

from dataclasses import dataclass
from io import StringIO

from Bio import SeqIO
from Bio.SeqFeature import SeqFeature
from Bio.SeqRecord import SeqRecord

_MOCK_GENBANK_RECORD = """\
LOCUS       NM_000546               1200 bp    mRNA    linear   PRI 01-JAN-2024
DEFINITION  Homo sapiens tumor protein p53 (TP53), mRNA.
ACCESSION   NM_000546
VERSION     NM_000546.6
KEYWORDS    RefSeq.
SOURCE      Homo sapiens (human)
  ORGANISM  Homo sapiens
            Eukaryota; Metazoa; Chordata; Craniata; Vertebrata; Mammalia.
FEATURES             Location/Qualifiers
     source          1..1200
                     /organism="Homo sapiens"
                     /mol_type="mRNA"
                     /db_xref="taxon:9606"
                     /chromosome="17"
     gene            1..1200
                     /gene="TP53"
                     /db_xref="GeneID:7157"
     CDS             61..1113
                     /gene="TP53"
                     /codon_start=1
                     /product="cellular tumor antigen p53"
                     /protein_id="NP_000537.3"
                     /translation="MEEPQSDPSVEPPLSQETFSDLWKLLPENNVLSPLPSQAMDDLM"
     mRNA            1..1200
                     /gene="TP53"
     exon            1..150
                     /gene="TP53"
                     /number=1
ORIGIN
        1 gtcagatcct agcgtcgagc ccccctctga gtcaggaaac attttcagac ctatggaaac
       61 tacttcctga aaacaacgtt ctgtcccccc ttgccgtccc aagcaatgga tgatttgatg
      121 ctgtccccgg acgatattga acaatggttc actgaagacc caggtccaga tgaagctccc
      181 agaatgccag aggctgctcc ccccgtggcc cctgcaccag cagctcctac accggcggcc
      241 cctgcaccag ccccctcctg gcccctgtca tcttctgtcc cttcccagaa aacctaccag
//
"""


@dataclass
class CodingSequenceInfo:
    """Structured representation of a coding sequence (CDS) feature."""

    gene: str
    protein_id: str
    product: str
    location: str
    translation_preview: str


class GenBankWorkflow:
    """Industry-level GenBank record processing workflow using Bio.SeqIO.

    Extracts record-level metadata and feature-level annotations (genes,
    CDS, exons) from an embedded GenBank-format record, requiring no
    network access.
    """

    def __init__(self, genbank_text: str) -> None:
        """Initialize by parsing a single embedded GenBank record.

        Args:
            genbank_text: Raw GenBank-format record text.
        """
        if not genbank_text.strip().startswith("LOCUS"):
            raise ValueError("Input does not appear to be a valid GenBank record")
        self.record: SeqRecord = SeqIO.read(StringIO(genbank_text), "genbank")

    def parse_record(self) -> SeqRecord:
        """Return the parsed GenBank SeqRecord."""
        return self.record

    def extract_features(self, feature_type: str | None = None) -> list[SeqFeature]:
        """Return record features, optionally filtered by feature type.

        Args:
            feature_type: If given, restrict results to this feature type
                (e.g. "gene", "CDS", "exon").
        """
        if feature_type is None:
            return list(self.record.features)
        return [f for f in self.record.features if f.type == feature_type]

    def extract_coding_sequences(self) -> list[CodingSequenceInfo]:
        """Extract structured information for every CDS feature in the record."""
        coding_sequences: list[CodingSequenceInfo] = []
        for feature in self.extract_features(feature_type="CDS"):
            qualifiers = feature.qualifiers
            gene = qualifiers.get("gene", ["unknown"])[0]
            protein_id = qualifiers.get("protein_id", ["unavailable"])[0]
            product = qualifiers.get("product", ["unannotated product"])[0]
            translation = qualifiers.get("translation", [""])[0]
            preview = translation[:20] + ("..." if len(translation) > 20 else "")
            coding_sequences.append(
                CodingSequenceInfo(
                    gene=gene,
                    protein_id=protein_id,
                    product=product,
                    location=str(feature.location),
                    translation_preview=preview,
                )
            )
        return coding_sequences

    def gene_annotations(self) -> list[dict[str, str]]:
        """Return simplified annotations for every gene feature."""
        annotations: list[dict[str, str]] = []
        for feature in self.extract_features(feature_type="gene"):
            annotations.append(
                {
                    "gene": feature.qualifiers.get("gene", ["unknown"])[0],
                    "db_xref": ";".join(feature.qualifiers.get("db_xref", [])),
                    "location": str(feature.location),
                }
            )
        return annotations

    def summarize_record(self) -> dict[str, str | int]:
        """Compute a high-level summary of the GenBank record."""
        organism = self.record.annotations.get("organism", "unknown")
        return {
            "accession": self.record.id,
            "description": self.record.description,
            "organism": organism,
            "sequence_length": len(self.record.seq),
            "feature_count": len(self.record.features),
        }

    @staticmethod
    def run() -> None:
        """Demonstrate GenBank parsing, feature extraction, and summarization."""
        workflow = GenBankWorkflow(_MOCK_GENBANK_RECORD)

        print("Record summary:", workflow.summarize_record())

        gene_annotations = workflow.gene_annotations()
        print(f"Gene annotations ({len(gene_annotations)}):")
        for annotation in gene_annotations:
            print(f"  {annotation}")

        coding_sequences = workflow.extract_coding_sequences()
        print(f"Coding sequences ({len(coding_sequences)}):")
        for cds in coding_sequences:
            print(
                f"  gene={cds.gene} protein_id={cds.protein_id} "
                f"product={cds.product!r} location={cds.location} "
                f"translation_preview={cds.translation_preview!r}"
            )

        exon_features = workflow.extract_features(feature_type="exon")
        print(f"Exon features found: {len(exon_features)}")


if __name__ == "__main__":
    GenBankWorkflow.run()
