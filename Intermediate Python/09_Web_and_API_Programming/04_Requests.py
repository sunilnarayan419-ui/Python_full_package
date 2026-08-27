"""
04_Requests.py

Production usage of the `requests` library as a synchronous HTTP client,
used here to call an external bioinformatics/compound-lookup API.

Demonstrates:
    - requests.Session for connection reuse
    - explicit timeouts on every call (never `requests.get(url)` bare)
    - a bounded retry strategy for transient failures only
    - distinguishing client errors, auth failures, and server failures
    - safe handling of Timeout / ConnectionError / HTTPError

The demo entrypoint does NOT call the public internet by default; the base
URL is configurable via environment variable so this file is safe to import
and exercise in CI without network access.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Any

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except ImportError as exc:  # pragma: no cover - dependency guard
    raise SystemExit(
        "The 'requests' package is required for this module. "
        "Install it with: pip install requests"
    ) from exc

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT_SECONDS = (3.05, 10)  # (connect timeout, read timeout)


class ExternalServiceError(RuntimeError):
    """Raised when an outbound call to a dependency ultimately fails."""


class ExternalServiceAuthError(ExternalServiceError):
    """Raised when the dependency rejects our credentials (401/403)."""


class ExternalServiceClientError(ExternalServiceError):
    """Raised for a 4xx response that is our fault (bad request), not
    retried, and not treated the same as a transient server failure."""


@dataclass(slots=True)
class CompoundLookupResult:
    compound_id: str
    name: str
    molecular_weight: float


class CompoundLookupClient:
    """Thin, reusable client around a compound-database REST API.

    A single Session is created once and reused for the lifetime of the
    client, giving connection pooling / keep-alive across calls, and a
    bounded urllib3 Retry policy handles only transient failure classes
    (connection errors and 5xx/429), never blind retries on every failure.
    """

    def __init__(self, base_url: str, api_key: str | None = None, timeout: tuple[float, float] = DEFAULT_TIMEOUT_SECONDS) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._session = requests.Session()

        retry_policy = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset({"GET", "HEAD"}),  # only retry safe methods
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry_policy, pool_maxsize=10)
        self._session.mount("https://", adapter)
        self._session.mount("http://", adapter)

        if api_key:
            self._session.headers["Authorization"] = f"Bearer {api_key}"
        self._session.headers["Accept"] = "application/json"

    def close(self) -> None:
        self._session.close()

    def __enter__(self) -> "CompoundLookupClient":
        return self

    def __exit__(self, *_exc_info: object) -> None:
        self.close()

    def get_compound(self, compound_id: str) -> CompoundLookupResult:
        """GET /compounds/{compound_id}. Raises ExternalServiceError (or a
        subclass) on any failure; never returns a partially-valid result."""
        url = f"{self._base_url}/compounds/{compound_id}"
        try:
            response = self._session.get(url, timeout=self._timeout)
        except requests.exceptions.Timeout as exc:
            raise ExternalServiceError(f"timed out calling {url}") from exc
        except requests.exceptions.ConnectionError as exc:
            raise ExternalServiceError(f"connection failed calling {url}") from exc

        if response.status_code in (401, 403):
            raise ExternalServiceAuthError(
                f"compound service rejected credentials (status={response.status_code})"
            )
        if 400 <= response.status_code < 500:
            raise ExternalServiceClientError(
                f"client error calling {url}: status={response.status_code} body={response.text[:200]!r}"
            )
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            raise ExternalServiceError(f"server error calling {url}: {exc}") from exc

        try:
            payload: dict[str, Any] = response.json()
        except ValueError as exc:
            raise ExternalServiceError(f"non-JSON response from {url}") from exc

        try:
            return CompoundLookupResult(
                compound_id=str(payload["id"]),
                name=str(payload["name"]),
                molecular_weight=float(payload["molecular_weight"]),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ExternalServiceError(f"unexpected response shape from {url}") from exc

    def search_compounds(self, query: str, *, limit: int = 20, offset: int = 0) -> list[CompoundLookupResult]:
        """GET /compounds?q=...&limit=...&offset=... using query params
        rather than string-concatenated URLs."""
        url = f"{self._base_url}/compounds"
        params = {"q": query, "limit": str(limit), "offset": str(offset)}
        try:
            response = self._session.get(url, params=params, timeout=self._timeout)
            response.raise_for_status()
        except requests.exceptions.Timeout as exc:
            raise ExternalServiceError(f"timed out calling {url}") from exc
        except requests.exceptions.ConnectionError as exc:
            raise ExternalServiceError(f"connection failed calling {url}") from exc
        except requests.exceptions.HTTPError as exc:
            raise ExternalServiceError(f"server error calling {url}: {exc}") from exc

        results = response.json().get("results", [])
        return [
            CompoundLookupResult(
                compound_id=str(item["id"]),
                name=str(item["name"]),
                molecular_weight=float(item["molecular_weight"]),
            )
            for item in results
        ]

    def submit_analysis_request(self, compound_id: str, assay: str) -> dict[str, Any]:
        """POST /analyses with a JSON body. Not idempotent, not retried
        automatically (POST is intentionally excluded from the retry
        policy's allowed_methods)."""
        url = f"{self._base_url}/analyses"
        body = {"compound_id": compound_id, "assay": assay}
        try:
            response = self._session.post(url, json=body, timeout=self._timeout)
        except requests.exceptions.Timeout as exc:
            raise ExternalServiceError(f"timed out calling {url}") from exc
        except requests.exceptions.ConnectionError as exc:
            raise ExternalServiceError(f"connection failed calling {url}") from exc

        if response.status_code in (401, 403):
            raise ExternalServiceAuthError("compound service rejected credentials")
        if 400 <= response.status_code < 500:
            raise ExternalServiceClientError(
                f"client error submitting analysis: status={response.status_code}"
            )
        response.raise_for_status()
        return response.json()


def _demo() -> None:
    logging.basicConfig(level=logging.INFO)

    base_url = os.environ.get("COMPOUND_API_BASE_URL")
    if not base_url:
        logger.info(
            "COMPOUND_API_BASE_URL is not set; skipping live network demo. "
            "Set it to a real or local compound-lookup service to exercise "
            "CompoundLookupClient end to end."
        )
        return

    api_key = os.environ.get("COMPOUND_API_KEY")
    with CompoundLookupClient(base_url=base_url, api_key=api_key) as client:
        try:
            result = client.get_compound("CPD-000123")
            logger.info("fetched compound: %s", result)
        except ExternalServiceAuthError:
            logger.error("authentication with compound service failed")
        except ExternalServiceClientError as exc:
            logger.error("bad request to compound service: %s", exc)
        except ExternalServiceError as exc:
            logger.error("compound service call failed: %s", exc)


if __name__ == "__main__":
    _demo()
