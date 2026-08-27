"""
05_HTTPX.py

Modern HTTP client usage with `httpx`, contrasted with `requests`
(04_Requests.py):

    requests -> synchronous only; one call blocks the thread until done.
    httpx    -> supports both a synchronous Client (drop-in-ish replacement
                for requests) AND an AsyncClient for non-blocking, concurrent
                I/O-bound calls -- the natural fit inside an async FastAPI
                application, where blocking calls would stall the event loop.

This module demonstrates fetching gene/protein annotations from an external
bioinformatics API, both synchronously and concurrently via asyncio.
"""

from __future__ import annotations

import asyncio
import logging
import os
from dataclasses import dataclass
from typing import Any

try:
    import httpx
except ImportError as exc:  # pragma: no cover - dependency guard
    raise SystemExit(
        "The 'httpx' package is required for this module. "
        "Install it with: pip install httpx"
    ) from exc

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = httpx.Timeout(connect=3.0, read=10.0, write=5.0, pool=3.0)


class ExternalServiceError(RuntimeError):
    """Raised when an outbound annotation lookup ultimately fails."""


@dataclass(slots=True)
class GeneAnnotation:
    gene_id: str
    symbol: str
    chromosome: str


def _parse_annotation(payload: dict[str, Any]) -> GeneAnnotation:
    try:
        return GeneAnnotation(
            gene_id=str(payload["id"]),
            symbol=str(payload["symbol"]),
            chromosome=str(payload["chromosome"]),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise ExternalServiceError("unexpected annotation response shape") from exc


class SyncAnnotationClient:
    """Synchronous httpx client. Prefer this only in synchronous code paths
    (scripts, sync Celery tasks) -- never inside an `async def` endpoint."""

    def __init__(self, base_url: str, timeout: httpx.Timeout = DEFAULT_TIMEOUT) -> None:
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "SyncAnnotationClient":
        return self

    def __exit__(self, *_exc_info: object) -> None:
        self.close()

    def get_gene(self, gene_id: str) -> GeneAnnotation:
        try:
            response = self._client.get(f"/genes/{gene_id}")
            response.raise_for_status()
        except httpx.TimeoutException as exc:
            raise ExternalServiceError(f"timed out fetching gene {gene_id}") from exc
        except httpx.ConnectError as exc:
            raise ExternalServiceError(f"connection failed fetching gene {gene_id}") from exc
        except httpx.HTTPStatusError as exc:
            raise ExternalServiceError(
                f"gene service returned {exc.response.status_code} for {gene_id}"
            ) from exc
        return _parse_annotation(response.json())


class AsyncAnnotationClient:
    """Async httpx client, the right tool for I/O-bound concurrent fan-out
    inside an async application (e.g. annotating many genes in parallel
    from within a FastAPI request handler).

    Connection pooling is shared across calls because a single AsyncClient
    instance is reused rather than being constructed per request.
    """

    def __init__(self, base_url: str, timeout: httpx.Timeout = DEFAULT_TIMEOUT) -> None:
        self._client = httpx.AsyncClient(base_url=base_url, timeout=timeout)

    async def aclose(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> "AsyncAnnotationClient":
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        await self.aclose()

    async def get_gene(self, gene_id: str) -> GeneAnnotation:
        try:
            response = await self._client.get(f"/genes/{gene_id}")
            response.raise_for_status()
        except httpx.TimeoutException as exc:
            raise ExternalServiceError(f"timed out fetching gene {gene_id}") from exc
        except httpx.ConnectError as exc:
            raise ExternalServiceError(f"connection failed fetching gene {gene_id}") from exc
        except httpx.HTTPStatusError as exc:
            raise ExternalServiceError(
                f"gene service returned {exc.response.status_code} for {gene_id}"
            ) from exc
        return _parse_annotation(response.json())

    async def get_genes(self, gene_ids: list[str]) -> list[GeneAnnotation | ExternalServiceError]:
        """Fan out concurrently; a single slow/failing lookup does not
        block the others, and failures are returned per-item rather than
        aborting the whole batch."""

        async def _one(gene_id: str) -> GeneAnnotation | ExternalServiceError:
            try:
                return await self.get_gene(gene_id)
            except ExternalServiceError as exc:
                return exc

        return await asyncio.gather(*(_one(gid) for gid in gene_ids))


async def _async_demo(base_url: str) -> None:
    async with AsyncAnnotationClient(base_url=base_url) as client:
        results = await client.get_genes(["BRCA1", "TP53", "EGFR"])
        for gene_id, result in zip(["BRCA1", "TP53", "EGFR"], results):
            if isinstance(result, ExternalServiceError):
                logger.error("failed to fetch %s: %s", gene_id, result)
            else:
                logger.info("fetched %s: %s", gene_id, result)


def _demo() -> None:
    logging.basicConfig(level=logging.INFO)

    base_url = os.environ.get("GENE_ANNOTATION_API_BASE_URL")
    if not base_url:
        logger.info(
            "GENE_ANNOTATION_API_BASE_URL is not set; skipping live network demo. "
            "Set it to a real or local annotation service to exercise these clients."
        )
        return

    with SyncAnnotationClient(base_url=base_url) as sync_client:
        try:
            gene = sync_client.get_gene("BRCA1")
            logger.info("sync fetch: %s", gene)
        except ExternalServiceError as exc:
            logger.error("sync fetch failed: %s", exc)

    asyncio.run(_async_demo(base_url))


if __name__ == "__main__":
    _demo()
