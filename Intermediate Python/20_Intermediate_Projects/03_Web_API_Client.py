from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Protocol

import httpx

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

DEFAULT_TIMEOUT_SECONDS = 10.0
DEFAULT_MAX_RETRIES = 3


class ApiClientError(Exception):
    """Base error for API client failures."""


class ApiResponseError(ApiClientError):
    """Raised when the API returns an unsuccessful HTTP status."""

    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        super().__init__(f"API request failed with status {status_code}: {message}")


class ApiTransportError(ApiClientError):
    """Raised when the underlying HTTP transport fails (network, timeout, DNS)."""


@dataclass(frozen=True, slots=True)
class ApiResponse:
    """Structured representation of an API response."""

    status_code: int
    data: Any
    url: str


class Transport(Protocol):
    """Abstraction over the HTTP transport so the client is testable offline."""

    def request(
        self,
        method: str,
        url: str,
        params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | None = None,
    ) -> httpx.Response: ...

    def close(self) -> None: ...


class HttpxTransport:
    """Real HTTP transport backed by httpx, used for live network calls."""

    def __init__(self, timeout: float = DEFAULT_TIMEOUT_SECONDS) -> None:
        self._client = httpx.Client(timeout=timeout)

    def request(
        self,
        method: str,
        url: str,
        params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | None = None,
    ) -> httpx.Response:
        return self._client.request(method, url, params=params, json=json_body)

    def close(self) -> None:
        self._client.close()


class MockTransport:
    """Offline transport that returns deterministic canned responses.

    Used as the default transport so the client demonstration remains
    self-contained and does not depend on live network access.
    """

    def __init__(self, fixtures: dict[str, dict[str, Any]]) -> None:
        self._fixtures = fixtures

    def request(
        self,
        method: str,
        url: str,
        params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | None = None,
    ) -> httpx.Response:
        key = f"{method.upper()} {url}"
        fixture = self._fixtures.get(key)
        if fixture is None:
            request = httpx.Request(method, url)
            return httpx.Response(status_code=404, json={"error": "not found"}, request=request)
        request = httpx.Request(method, url)
        return httpx.Response(status_code=fixture["status_code"], json=fixture["body"], request=request)

    def close(self) -> None:
        return None


class ApiClient:
    """Reusable HTTP API client with retry handling and structured errors."""

    def __init__(
        self,
        base_url: str,
        transport: Transport,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._transport = transport
        self._max_retries = max_retries

    def get(self, endpoint: str, params: dict[str, Any] | None = None) -> ApiResponse:
        return self._request_with_retry("GET", endpoint, params=params)

    def post(self, endpoint: str, json_body: dict[str, Any] | None = None) -> ApiResponse:
        return self._request_with_retry("POST", endpoint, json_body=json_body)

    def close(self) -> None:
        self._transport.close()

    def _request_with_retry(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | None = None,
    ) -> ApiResponse:
        url = f"{self._base_url}/{endpoint.lstrip('/')}"
        last_error: Exception | None = None

        for attempt in range(1, self._max_retries + 1):
            try:
                response = self._transport.request(method, url, params=params, json_body=json_body)
            except httpx.TransportError as exc:
                last_error = exc
                logger.warning("Attempt %d/%d failed: %s", attempt, self._max_retries, exc)
                continue

            if response.status_code >= 500 and attempt < self._max_retries:
                logger.warning(
                    "Server error %d on attempt %d/%d, retrying.",
                    response.status_code,
                    attempt,
                    self._max_retries,
                )
                continue

            return self._parse_response(response, url)

        raise ApiTransportError(
            f"Request to {url} failed after {self._max_retries} attempts."
        ) from last_error

    def _parse_response(self, response: httpx.Response, url: str) -> ApiResponse:
        if response.status_code >= 400:
            try:
                error_body = response.json()
            except (ValueError, TypeError):
                error_body = {"error": "unknown"}
            raise ApiResponseError(response.status_code, str(error_body))

        try:
            data = response.json()
        except (ValueError, TypeError) as exc:
            raise ApiClientError(f"Response from {url} was not valid JSON.") from exc

        return ApiResponse(status_code=response.status_code, data=data, url=url)


class ExperimentApiService:
    """Business-logic layer that consumes ApiClient responses for a domain."""

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def fetch_experiment(self, experiment_id: str) -> dict[str, Any]:
        response = self._client.get(f"/experiments/{experiment_id}")
        if not isinstance(response.data, dict):
            raise ApiClientError("Expected object payload for experiment resource.")
        return response.data

    def list_experiments(self, status: str | None = None) -> list[dict[str, Any]]:
        params = {"status": status} if status else None
        response = self._client.get("/experiments", params=params)
        if not isinstance(response.data, list):
            raise ApiClientError("Expected list payload for experiments collection.")
        return response.data


def _build_mock_transport() -> MockTransport:
    fixtures = {
        "GET https://api.research-lab.example.com/v1/experiments/EXP-001": {
            "status_code": 200,
            "body": {"id": "EXP-001", "title": "Drought Stress Response", "status": "completed"},
        },
        "GET https://api.research-lab.example.com/v1/experiments": {
            "status_code": 200,
            "body": [
                {"id": "EXP-001", "title": "Drought Stress Response", "status": "completed"},
                {"id": "EXP-002", "title": "Nitrogen Uptake Study", "status": "running"},
            ],
        },
    }
    return MockTransport(fixtures)


def run() -> list[dict[str, Any]]:
    """Runs the API client demonstration against an offline mock transport."""
    transport = _build_mock_transport()
    client = ApiClient(base_url="https://api.research-lab.example.com/v1", transport=transport)
    service = ExperimentApiService(client)

    try:
        experiment = service.fetch_experiment("EXP-001")
        logger.info("Fetched experiment: %s", experiment)

        experiments = service.list_experiments()
        logger.info("Listed %d experiments.", len(experiments))
    finally:
        client.close()

    return experiments


if __name__ == "__main__":
    run()
