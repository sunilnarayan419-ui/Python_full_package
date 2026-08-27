from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from enum import Enum


class BioinformaticsService(Enum):
    """Supported bioinformatics web-service backends."""

    NCBI_EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    UNIPROT = "https://rest.uniprot.org"
    RCSB_PDB = "https://data.rcsb.org/rest/v1/core"
    ENSEMBL = "https://rest.ensembl.org"


@dataclass
class ApiResponse:
    """Structured, validated result of a single API request."""

    service: str
    endpoint: str
    status_code: int
    success: bool
    payload: dict[str, object] = field(default_factory=dict)
    error_message: str | None = None


class BioinformaticsApiClient:
    """Industry-level API client architecture for bioinformatics web services.

    Separates network transport from biological analysis and keeps
    `run()` fully offline by default. Live requests are explicitly
    opt-in via `execute_live_request` and are never invoked automatically.
    """

    def __init__(
        self,
        service: BioinformaticsService,
        timeout_seconds: float = 10.0,
        max_retries: int = 2,
        contact_identifier: str | None = None,
    ) -> None:
        """Initialize the API client for a specific bioinformatics service.

        Args:
            service: Target bioinformatics web-service backend.
            timeout_seconds: Network timeout applied to each request.
            max_retries: Maximum number of retry attempts on transient failure.
            contact_identifier: Optional caller-supplied tool/contact string
                sent as a descriptive User-Agent (never a credential or key).
        """
        self.service = service
        self.timeout_seconds = timeout_seconds
        self.max_retries = max(0, max_retries)
        self.contact_identifier = contact_identifier or "bioinformatics-api-client/1.0"
        self._request_log: list[str] = []

    def build_endpoint(self, path: str) -> str:
        """Construct a full endpoint URL from the service base and a relative path.

        Args:
            path: Relative resource path (e.g. "einfo.fcgi", "uniprotkb/P01308").
        """
        base = self.service.value.rstrip("/")
        return f"{base}/{path.lstrip('/')}"

    def execute_live_request(
        self, path: str, query_params: dict[str, str] | None = None
    ) -> ApiResponse:
        """Perform a real, rate-limit-aware GET request against the configured service.

        This method performs actual network I/O and is never called from
        `run()`. Retries only occur on transient (5xx or connection) errors,
        never in an uncontrolled loop.

        Args:
            path: Relative resource path appended to the service base URL.
            query_params: Optional query-string parameters.
        """
        endpoint = self.build_endpoint(path)
        if query_params:
            query_string = "&".join(f"{k}={v}" for k, v in query_params.items())
            endpoint = f"{endpoint}?{query_string}"

        request = urllib.request.Request(
            endpoint, headers={"User-Agent": self.contact_identifier}
        )

        attempt = 0
        last_error: str | None = None
        while attempt <= self.max_retries:
            try:
                with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                    status_code = response.getcode()
                    raw_body = response.read().decode("utf-8", errors="replace")
                    payload = self._safe_parse_json(raw_body)
                    self._request_log.append(endpoint)
                    return ApiResponse(
                        service=self.service.name,
                        endpoint=endpoint,
                        status_code=status_code,
                        success=200 <= status_code < 300,
                        payload=payload,
                    )
            except urllib.error.HTTPError as exc:
                if exc.code < 500 or attempt == self.max_retries:
                    return ApiResponse(
                        service=self.service.name,
                        endpoint=endpoint,
                        status_code=exc.code,
                        success=False,
                        error_message=str(exc),
                    )
                last_error = str(exc)
            except (urllib.error.URLError, TimeoutError) as exc:
                last_error = str(exc)
            attempt += 1

        return ApiResponse(
            service=self.service.name,
            endpoint=endpoint,
            status_code=0,
            success=False,
            error_message=last_error or "Request failed after retries",
        )

    @staticmethod
    def _safe_parse_json(raw_body: str) -> dict[str, object]:
        """Safely parse a JSON response body, tolerating non-JSON payloads."""
        try:
            parsed = json.loads(raw_body)
            return parsed if isinstance(parsed, dict) else {"result": parsed}
        except json.JSONDecodeError:
            return {"raw_text_preview": raw_body[:200]}

    def simulate_offline_response(self, path: str, mock_payload: dict[str, object]) -> ApiResponse:
        """Build a structured ApiResponse from a mock payload without any network I/O.

        Args:
            path: Relative resource path this response simulates.
            mock_payload: Pre-defined payload representing an expected response shape.
        """
        return ApiResponse(
            service=self.service.name,
            endpoint=self.build_endpoint(path),
            status_code=200,
            success=True,
            payload=mock_payload,
        )

    def request_history(self) -> list[str]:
        """Return the list of endpoints actually contacted via live requests."""
        return list(self._request_log)

    @staticmethod
    def run() -> None:
        """Demonstrate the API client architecture using offline mock responses only."""
        uniprot_client = BioinformaticsApiClient(
            service=BioinformaticsService.UNIPROT, contact_identifier="compbio-pipeline-demo/1.0"
        )
        mock_uniprot_response = uniprot_client.simulate_offline_response(
            path="uniprotkb/P01308",
            mock_payload={
                "primaryAccession": "P01308",
                "proteinDescription": {"recommendedName": {"fullName": {"value": "Insulin"}}},
                "sequence": {"length": 110},
            },
        )
        print("Simulated UniProt response:", mock_uniprot_response)

        pdb_client = BioinformaticsApiClient(service=BioinformaticsService.RCSB_PDB)
        mock_pdb_response = pdb_client.simulate_offline_response(
            path="entry/4HHB",
            mock_payload={"rcsb_id": "4HHB", "struct": {"title": "HEMOGLOBIN"}},
        )
        print("Simulated RCSB PDB response:", mock_pdb_response)

        ensembl_client = BioinformaticsApiClient(service=BioinformaticsService.ENSEMBL)
        endpoint_preview = ensembl_client.build_endpoint("lookup/id/ENSG00000141510")
        print("Constructed (not executed) Ensembl endpoint:", endpoint_preview)

        print(
            "Live requests are available via execute_live_request() but are "
            "never triggered automatically by run()."
        )


if __name__ == "__main__":
    BioinformaticsApiClient.run()
