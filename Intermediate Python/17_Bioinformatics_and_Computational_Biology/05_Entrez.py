from __future__ import annotations

from dataclasses import dataclass
from io import StringIO

from Bio import Entrez, SeqIO

_MOCK_ESEARCH_IDS = ["NM_000546", "NM_007294", "NM_000059"]

_MOCK_EFETCH_FASTA = """\
>NM_000546.6 Homo sapiens tumor protein p53 (TP53), mRNA
ATGGAGGAGCCGCAGTCAGATCCTAGCGTCGAGCCCCCTCTGAGTCAGGAAACATTTTC
>NM_007294.4 Homo sapiens BRCA1 DNA repair associated (BRCA1), mRNA
ATGGATTTATCTGCTCTTCGCGTTGAAGAAGTACAAAATGTCATTAATGCTATGCAGAA
>NM_000059.4 Homo sapiens BRCA2 DNA repair associated (BRCA2), mRNA
ATGCCTATTGGATCCAAAGAGAGGCCAACATTTTTTGAAATTTTTAAGACACGCTGCAA
"""


@dataclass
class EntrezSearchResult:
    """Structured result of an Entrez ESearch call."""

    query_term: str
    database: str
    ids: list[str]
    total_count: int


class EntrezWorkflow:
    """Industry-level NCBI Entrez workflow wrapping Bio.Entrez.

    Live calls to NCBI are strictly opt-in via `live_mode=True` and
    require a caller-supplied contact email. The default `run()` path
    exercises the same parsing logic against embedded mock responses,
    keeping the module network-safe by default.
    """

    def __init__(self, contact_email: str, live_mode: bool = False, request_delay: float = 0.34) -> None:
        """Initialize the workflow.

        Args:
            contact_email: Contact email required by NCBI for Entrez usage
                (caller-supplied; never hard-coded).
            live_mode: When True, network calls are permitted.
            request_delay: Minimum delay in seconds between live requests,
                respecting NCBI's rate-limit guidance (max ~3 req/s).
        """
        if live_mode and (not contact_email or "@" not in contact_email):
            raise ValueError("A valid contact_email is required when live_mode is enabled")
        self.contact_email = contact_email
        self.live_mode = live_mode
        self.request_delay = request_delay
        if live_mode:
            Entrez.email = self.contact_email

    def search(self, database: str, term: str, retmax: int = 20) -> EntrezSearchResult:
        """Run an ESearch query, live or against mock data depending on live_mode.

        Args:
            database: Entrez database name (e.g. "nucleotide", "protein").
            term: Search query term.
            retmax: Maximum number of identifiers to return.
        """
        if not term.strip():
            raise ValueError("Search term must not be empty")

        if not self.live_mode:
            ids = _MOCK_ESEARCH_IDS[:retmax]
            return EntrezSearchResult(
                query_term=term, database=database, ids=ids, total_count=len(ids)
            )

        try:
            import time

            handle = Entrez.esearch(db=database, term=term, retmax=retmax)
            record = Entrez.read(handle)
            handle.close()
            time.sleep(self.request_delay)
            ids = list(record.get("IdList", []))
            return EntrezSearchResult(
                query_term=term,
                database=database,
                ids=ids,
                total_count=int(record.get("Count", len(ids))),
            )
        except (OSError, RuntimeError) as exc:
            raise RuntimeError(f"Live Entrez search failed: {exc}") from exc

    def fetch_sequences(self, database: str, ids: list[str], rettype: str = "fasta") -> list[SeqIO.SeqRecord]:
        """Fetch sequence records for a list of identifiers.

        Args:
            database: Entrez database name.
            ids: Identifiers previously returned by `search`.
            rettype: Entrez return type (e.g. "fasta", "gb").
        """
        if not ids:
            raise ValueError("At least one identifier is required")

        if not self.live_mode:
            return list(SeqIO.parse(StringIO(_MOCK_EFETCH_FASTA), "fasta"))

        try:
            import time

            handle = Entrez.efetch(
                db=database, id=",".join(ids), rettype=rettype, retmode="text"
            )
            records = list(SeqIO.parse(handle, rettype))
            handle.close()
            time.sleep(self.request_delay)
            return records
        except (OSError, ValueError) as exc:
            raise RuntimeError(f"Live Entrez fetch failed: {exc}") from exc

    @staticmethod
    def summarize_records(records: list[SeqIO.SeqRecord]) -> dict[str, int | float]:
        """Compute basic statistics across fetched sequence records."""
        lengths = [len(record.seq) for record in records]
        if not lengths:
            return {"record_count": 0, "mean_length": 0.0}
        return {
            "record_count": len(lengths),
            "mean_length": round(sum(lengths) / len(lengths), 2),
            "max_length": max(lengths),
        }

    @staticmethod
    def run() -> None:
        """Demonstrate the search -> fetch -> summarize workflow using mock data."""
        workflow = EntrezWorkflow(contact_email="", live_mode=False)

        search_result = workflow.search(
            database="nucleotide", term="TP53[gene] AND Homo sapiens[orgn]"
        )
        print(f"ESearch (mock) returned {search_result.total_count} ids: {search_result.ids}")

        records = workflow.fetch_sequences(database="nucleotide", ids=search_result.ids)
        print(f"EFetch (mock) returned {len(records)} sequence records")
        for record in records:
            print(f"  {record.id}: {len(record.seq)} bp")

        print("Summary:", EntrezWorkflow.summarize_records(records))
        print(
            "To enable live NCBI access, instantiate with "
            "live_mode=True and a valid contact_email."
        )


if __name__ == "__main__":
    EntrezWorkflow.run()
