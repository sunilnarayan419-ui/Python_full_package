from __future__ import annotations

from dataclasses import dataclass
from types import TracebackType
from typing import Any, Self

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class DrugDatabaseError(Exception):
    pass


class DrugNotFoundError(DrugDatabaseError):
    def __init__(self, drug_id: str) -> None:
        super().__init__(f"Drug '{drug_id}' was not found in the external database.")
        self.drug_id = drug_id


@dataclass(slots=True, frozen=True)
class DrugRecord:
    drug_id: str
    name: str
    approval_status: str
    indications: list[str]


class DrugDatabaseClient:
    """Reusable synchronous client for an external drug database provider.

    Wraps a single `requests.Session` configured with connection pooling,
    a bounded retry policy for transient failures, and explicit timeouts
    on every call site.
    """

    _DEFAULT_TIMEOUT = (3.0, 10.0)

    def __init__(self, base_url: str, api_key: str, *, pool_maxsize: int = 20, max_retries: int = 3) -> None:
        self._base_url = base_url.rstrip("/")
        self._session = requests.Session()
        self._session.headers.update({"Authorization": f"Bearer {api_key}", "Accept": "application/json"})

        retry_policy = Retry(
            total=max_retries,
            backoff_factor=0.5,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset({"GET", "POST", "PUT", "PATCH", "DELETE"}),
            raise_on_status=False,
        )
        adapter = HTTPAdapter(pool_maxsize=pool_maxsize, max_retries=retry_policy)
        self._session.mount("https://", adapter)
        self._session.mount("http://", adapter)

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    def close(self) -> None:
        self._session.close()

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        kwargs.setdefault("timeout", self._DEFAULT_TIMEOUT)
        try:
            response = self._session.request(method, f"{self._base_url}{path}", **kwargs)
        except requests.exceptions.Timeout as exc:
            raise DrugDatabaseError(f"Request to {path} timed out.") from exc
        except requests.exceptions.ConnectionError as exc:
            raise DrugDatabaseError(f"Connection to drug database failed: {exc}") from exc

        if response.status_code == 404:
            raise DrugNotFoundError(path.rsplit("/", 1)[-1])
        if response.status_code >= 400:
            raise DrugDatabaseError(f"Drug database request failed with status {response.status_code}: {response.text}")
        return response

    def get_drug(self, drug_id: str) -> DrugRecord:
        response = self._request("GET", f"/drugs/{drug_id}")
        payload = response.json()
        return DrugRecord(
            drug_id=payload["drug_id"],
            name=payload["name"],
            approval_status=payload["approval_status"],
            indications=payload.get("indications", []),
        )

    def search_drugs(self, query: str, *, limit: int = 20) -> list[DrugRecord]:
        response = self._request("GET", "/drugs", params={"q": query, "limit": limit})
        return [
            DrugRecord(
                drug_id=item["drug_id"],
                name=item["name"],
                approval_status=item["approval_status"],
                indications=item.get("indications", []),
            )
            for item in response.json().get("results", [])
        ]

    def stream_bulk_export(self, dataset_id: str, *, chunk_size: int = 65536):
        with self._session.get(
            f"{self._base_url}/datasets/{dataset_id}/export",
            stream=True,
            timeout=self._DEFAULT_TIMEOUT,
        ) as response:
            response.raise_for_status()
            yield from response.iter_content(chunk_size=chunk_size)
