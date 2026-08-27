from __future__ import annotations

import httpx
import pytest

from src.bioinformatics_client import BioinformaticsServiceUnavailableError, ExternalBioinformaticsClient

pytestmark = pytest.mark.asyncio


def _mock_transport(responses: list[httpx.Response]) -> httpx.MockTransport:
    call_count = {"value": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        response = responses[min(call_count["value"], len(responses) - 1)]
        call_count["value"] += 1
        return response

    return httpx.MockTransport(handler)


async def test_get_gene_annotation_returns_parsed_result() -> None:
    client = ExternalBioinformaticsClient(base_url="https://bio-service.test", api_key="test-key")
    client._client._transport = _mock_transport(
        [httpx.Response(200, json={"gene_id": "ENSG001", "symbol": "TP53", "organism": "human", "biotype": "protein_coding"})]
    )

    annotation = await client.get_gene_annotation("ENSG001")

    assert annotation.symbol == "TP53"
    await client.aclose()


async def test_retries_on_server_error_then_succeeds() -> None:
    client = ExternalBioinformaticsClient(base_url="https://bio-service.test", api_key="test-key", max_retries=3)
    client._client._transport = _mock_transport(
        [
            httpx.Response(503),
            httpx.Response(200, json={"gene_id": "ENSG002", "symbol": "BRCA1", "organism": "human", "biotype": "protein_coding"}),
        ]
    )

    annotation = await client.get_gene_annotation("ENSG002")

    assert annotation.symbol == "BRCA1"
    await client.aclose()


async def test_raises_after_exhausting_retries() -> None:
    client = ExternalBioinformaticsClient(base_url="https://bio-service.test", api_key="test-key", max_retries=2)
    client._client._transport = _mock_transport([httpx.Response(503), httpx.Response(503)])

    with pytest.raises(BioinformaticsServiceUnavailableError):
        await client.get_gene_annotation("ENSG003")

    await client.aclose()
