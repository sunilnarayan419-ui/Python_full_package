from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from dataclasses import dataclass
from types import TracebackType
from typing import Any, Self

import httpx


class BioinformaticsServiceError(Exception):
    pass


class BioinformaticsServiceTimeoutError(BioinformaticsServiceError):
    pass


class BioinformaticsServiceUnavailableError(BioinformaticsServiceError):
    pass


@dataclass(slots=True, frozen=True)
class GeneAnnotation:
    gene_id: str
    symbol: str
    organism: str
    biotype: str


class ExternalBioinformaticsClient:
    """Async client for an external gene-annotation service.

    Maintains a single pooled AsyncClient for the lifetime of the client
    instance and supports bounded concurrency for batch lookups.
    """

    def __init__(
        self,
        base_url: str,
        api_key: str,
        *,
        max_connections: int = 20,
        max_concurrent_requests: int = 10,
        connect_timeout: float = 2.0,
        read_timeout: float = 8.0,
        max_retries: int = 3,
    ) -> None:
        self._max_retries = max_retries
        self._semaphore = asyncio.Semaphore(max_concurrent_requests)
        self._client = httpx.AsyncClient(
            base_url=base_url,
            headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"},
            limits=httpx.Limits(max_connections=max_connections, max_keepalive_connections=max_connections),
            timeout=httpx.Timeout(connect=connect_timeout, read=read_timeout, write=5.0, pool=5.0),
        )

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        await self._client.aclose()

    async def _get_with_retries(self, path: str, *, params: dict[str, Any] | None = None) -> httpx.Response:
        last_exc: Exception | None = None
        for attempt in range(self._max_retries):
            try:
                async with self._semaphore:
                    response = await self._client.get(path, params=params)
                if response.status_code == 429:
                    retry_after = float(response.headers.get("Retry-After", "1"))
                    await asyncio.sleep(retry_after)
                    continue
                if response.status_code >= 500:
                    raise BioinformaticsServiceUnavailableError(f"Upstream returned {response.status_code}")
                response.raise_for_status()
                return response
            except httpx.TimeoutException as exc:
                last_exc = BioinformaticsServiceTimeoutError(str(exc))
            except BioinformaticsServiceUnavailableError as exc:
                last_exc = exc
            except httpx.HTTPStatusError as exc:
                last_exc = BioinformaticsServiceError(str(exc))
            await asyncio.sleep(0.25 * (2**attempt))
        assert last_exc is not None
        raise last_exc

    async def get_gene_annotation(self, gene_id: str) -> GeneAnnotation:
        response = await self._get_with_retries(f"/genes/{gene_id}")
        payload = response.json()
        return GeneAnnotation(
            gene_id=payload["gene_id"],
            symbol=payload["symbol"],
            organism=payload["organism"],
            biotype=payload["biotype"],
        )

    async def get_gene_annotations_batch(self, gene_ids: list[str]) -> list[GeneAnnotation]:
        tasks = [self.get_gene_annotation(gene_id) for gene_id in gene_ids]
        return await asyncio.gather(*tasks)

    async def stream_large_dataset(self, dataset_id: str) -> AsyncIterator[bytes]:
        async with self._semaphore:
            async with self._client.stream("GET", f"/datasets/{dataset_id}/export") as response:
                response.raise_for_status()
                async for chunk in response.aiter_bytes(chunk_size=65536):
                    yield chunk
