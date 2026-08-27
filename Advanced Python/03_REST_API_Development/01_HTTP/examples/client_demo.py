from __future__ import annotations

import time
from dataclasses import dataclass

import httpx


@dataclass(slots=True)
class HttpClientConfig:
    base_url: str
    connect_timeout: float = 3.0
    read_timeout: float = 10.0
    max_retries: int = 3
    backoff_factor: float = 0.5


class CompoundRegistryClient:
    def __init__(self, config: HttpClientConfig) -> None:
        self._config = config
        self._etag_cache: dict[str, str] = {}
        self._client = httpx.Client(
            base_url=config.base_url,
            timeout=httpx.Timeout(connect=config.connect_timeout, read=config.read_timeout, write=5.0, pool=5.0),
            follow_redirects=True,
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "CompoundRegistryClient":
        return self

    def __exit__(self, *_exc_info: object) -> None:
        self.close()

    def _request_with_retries(self, method: str, url: str, **kwargs: object) -> httpx.Response:
        last_exc: Exception | None = None
        for attempt in range(self._config.max_retries):
            try:
                response = self._client.request(method, url, **kwargs)
                if response.status_code == 429:
                    retry_after = float(response.headers.get("Retry-After", "1"))
                    time.sleep(retry_after)
                    continue
                if response.status_code >= 500:
                    raise httpx.HTTPStatusError("Server error", request=response.request, response=response)
                return response
            except (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.HTTPStatusError) as exc:
                last_exc = exc
                time.sleep(self._config.backoff_factor * (2**attempt))
        assert last_exc is not None
        raise last_exc

    def get_compound(self, compound_id: str) -> httpx.Response | None:
        headers = {}
        cached_etag = self._etag_cache.get(compound_id)
        if cached_etag is not None:
            headers["If-None-Match"] = f'"{cached_etag}"'

        response = self._request_with_retries("GET", f"/api/v1/compounds/{compound_id}", headers=headers)

        if response.status_code == 304:
            return None
        response.raise_for_status()
        etag = response.headers.get("ETag", "").strip('"')
        if etag:
            self._etag_cache[compound_id] = etag
        return response
