from __future__ import annotations

from dataclasses import dataclass
from io import StringIO

from Bio.Blast import NCBIXML

_MOCK_BLAST_XML = """<?xml version="1.0"?>
<!DOCTYPE BlastOutput PUBLIC "-//NCBI//NCBI BlastOutput/EN" "http://www.ncbi.nlm.nih.gov/dtd/NCBI_BlastOutput.dtd">
<BlastOutput>
  <BlastOutput_program>blastp</BlastOutput_program>
  <BlastOutput_version>BLASTP 2.15.0+</BlastOutput_version>
  <BlastOutput_db>nr</BlastOutput_db>
  <BlastOutput_query-ID>Query_1</BlastOutput_query-ID>
  <BlastOutput_query-len>393</BlastOutput_query-len>
  <BlastOutput_param>
    <Parameters>
      <Parameters_matrix>BLOSUM62</Parameters_matrix>
      <Parameters_expect>10</Parameters_expect>
      <Parameters_gap-open>11</Parameters_gap-open>
      <Parameters_gap-extend>1</Parameters_gap-extend>
      <Parameters_filter>F</Parameters_filter>
    </Parameters>
  </BlastOutput_param>
  <BlastOutput_iterations>
    <Iteration>
      <Iteration_iter-num>1</Iteration_iter-num>
      <Iteration_hits>
        <Hit>
          <Hit_num>1</Hit_num>
          <Hit_id>ref|NP_000537.3|</Hit_id>
          <Hit_def>cellular tumor antigen p53 [Homo sapiens]</Hit_def>
          <Hit_accession>NP_000537</Hit_accession>
          <Hit_len>393</Hit_len>
          <Hit_hsps>
            <Hsp>
              <Hsp_bit-score>620.5</Hsp_bit-score>
              <Hsp_evalue>0.0</Hsp_evalue>
              <Hsp_identity>380</Hsp_identity>
              <Hsp_align-len>393</Hsp_align-len>
              <Hsp_qseq>MEEPQSDPSVEPPLSQETFSDLWKLLPENNVLSPLPSQAMDDLMLSPDDIEQWFTEDPG</Hsp_qseq>
              <Hsp_hseq>MEEPQSDPSVEPPLSQETFSDLWKLLPENNVLSPLPSQAMDDLMLSPDDIEQWFTEDPG</Hsp_hseq>
            </Hsp>
          </Hit_hsps>
        </Hit>
        <Hit>
          <Hit_num>2</Hit_num>
          <Hit_id>ref|XP_016869030.1|</Hit_id>
          <Hit_def>p53-like tumor suppressor isoform X1 [Pan troglodytes]</Hit_def>
          <Hit_accession>XP_016869030</Hit_accession>
          <Hit_len>390</Hit_len>
          <Hit_hsps>
            <Hsp>
              <Hsp_bit-score>598.2</Hsp_bit-score>
              <Hsp_evalue>1e-172</Hsp_evalue>
              <Hsp_identity>365</Hsp_identity>
              <Hsp_align-len>393</Hsp_align-len>
              <Hsp_qseq>MEEPQSDPSVEPPLSQETFSDLWKLLPENNVLSPLPSQAMDDLMLSPDDIEQWFTEDPG</Hsp_qseq>
              <Hsp_hseq>MEEPQSDPSVEPPLSQETFSDLWKLLPENNVLSPLPSQAMDDLMLSPDDVEQWFTEDPG</Hsp_hseq>
            </Hsp>
          </Hit_hsps>
        </Hit>
      </Iteration_hits>
    </Iteration>
  </BlastOutput_iterations>
</BlastOutput>
"""


@dataclass
class BlastHitSummary:
    """Structured representation of a single BLAST hit."""

    hit_id: str
    definition: str
    accession: str
    hit_length: int
    bit_score: float
    e_value: float
    percent_identity: float


class BlastWorkflow:
    """Industry-level BLAST workflow built on Bio.Blast.

    Separates network submission (explicitly opt-in) from XML result
    parsing, which is the safe, default, offline-capable code path.
    """

    _VALID_PROTEIN = frozenset("ACDEFGHIKLMNPQRSTVWYBXZJUO*")

    def __init__(self, query_sequence: str, program: str = "blastp", database: str = "nr") -> None:
        """Initialize a BLAST workflow for a single protein query.

        Args:
            query_sequence: Protein query sequence to be searched.
            program: BLAST program identifier (e.g. "blastp", "blastn").
            database: Target BLAST database name.
        """
        if not self.validate_query(query_sequence):
            raise ValueError("Query sequence contains invalid amino-acid symbols")
        self.query_sequence = query_sequence.strip().upper()
        self.program = program
        self.database = database

    @staticmethod
    def validate_query(sequence: str) -> bool:
        """Validate that a query sequence is a non-empty valid protein sequence."""
        cleaned = sequence.strip().upper()
        return bool(cleaned) and set(cleaned).issubset(BlastWorkflow._VALID_PROTEIN)

    def parse_blast_xml(self, xml_source: str) -> list[BlastHitSummary]:
        """Parse a BLAST XML result string into structured hit summaries.

        Args:
            xml_source: Raw BLAST XML content, typically produced by NCBIWWW
                or a local BLAST+ command-line run.
        """
        handle = StringIO(xml_source)
        blast_record = NCBIXML.read(handle)

        summaries: list[BlastHitSummary] = []
        for alignment in blast_record.alignments:
            best_hsp = min(alignment.hsps, key=lambda hsp: hsp.expect)
            percent_identity = round(
                (best_hsp.identities / best_hsp.align_length) * 100.0, 2
            )
            summaries.append(
                BlastHitSummary(
                    hit_id=alignment.hit_id,
                    definition=alignment.hit_def,
                    accession=alignment.accession,
                    hit_length=alignment.length,
                    bit_score=round(best_hsp.bits, 2),
                    e_value=best_hsp.expect,
                    percent_identity=percent_identity,
                )
            )
        return summaries

    def top_hits(self, hits: list[BlastHitSummary], n: int = 5) -> list[BlastHitSummary]:
        """Return the top-N hits ranked by ascending e-value then descending score."""
        return sorted(hits, key=lambda hit: (hit.e_value, -hit.bit_score))[:n]

    def submit_live_blast(
        self,
        entrez_email: str,
        expect_threshold: float = 10.0,
        timeout_seconds: float = 60.0,
    ) -> str:
        """Submit a live BLAST search against NCBI. Explicitly opt-in only.

        This method performs a real network request and is intentionally
        never invoked from run(). Callers must supply a valid contact
        email per NCBI usage policy and are responsible for job cost/time.

        Args:
            entrez_email: Contact email required by NCBI for API usage.
            expect_threshold: E-value cutoff for the search.
            timeout_seconds: Network timeout applied to the request.

        Returns:
            Raw BLAST XML result as a string.
        """
        from Bio.Blast import NCBIWWW  # local import: only needed for live calls
        import socket

        if not entrez_email or "@" not in entrez_email:
            raise ValueError("A valid contact email is required for live NCBI BLAST access")

        socket.setdefaulttimeout(timeout_seconds)
        try:
            result_handle = NCBIWWW.qblast(
                program=self.program,
                database=self.database,
                sequence=self.query_sequence,
                expect=expect_threshold,
            )
            return result_handle.read()
        except (OSError, ValueError) as exc:
            raise RuntimeError(f"Live BLAST submission failed: {exc}") from exc

    @staticmethod
    def run() -> None:
        """Demonstrate the offline-safe BLAST XML parsing workflow."""
        query = "MEEPQSDPSVEPPLSQETFSDLWKLLPENNVLSPLPSQAMDDLMLSPDDIEQWFTEDPG"
        workflow = BlastWorkflow(query_sequence=query, program="blastp", database="nr")

        hits = workflow.parse_blast_xml(_MOCK_BLAST_XML)
        print(f"Parsed {len(hits)} BLAST hits from embedded XML")

        for hit in workflow.top_hits(hits, n=3):
            print(
                f"  {hit.accession} | {hit.definition} | "
                f"identity={hit.percent_identity}% | e-value={hit.e_value} | "
                f"bit-score={hit.bit_score}"
            )

        print(
            "Live NCBI submission is available via submit_live_blast() "
            "but is not invoked automatically."
        )


if __name__ == "__main__":
    BlastWorkflow.run()
