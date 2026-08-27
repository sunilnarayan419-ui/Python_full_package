from __future__ import annotations

import json
from decimal import Decimal
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from app.repositories.gene_expression_repository import (
    GeneAnnotationMatch,
    GeneExpressionRepository,
)


@pytest.mark.asyncio
async def test_find_genes_by_pathway_parses_jsonb() -> None:
    gene_id = uuid4()
    mock_conn = AsyncMock()
    mock_conn.fetch.return_value = [
        {"gene_id": gene_id, "symbol": "MAPK1", "annotations": json.dumps({"pathway": "MAPK"})}
    ]
    with patch("app.repositories.gene_expression_repository.acquire_connection") as mock_acquire:
        mock_acquire.return_value.__aenter__.return_value = mock_conn
        repo = GeneExpressionRepository()
        result = await repo.find_genes_by_pathway("MAPK")

    assert result == [
        GeneAnnotationMatch(gene_id=gene_id, symbol="MAPK1", annotations={"pathway": "MAPK"})
    ]
    query_arg, param_arg = mock_conn.fetch.call_args.args
    assert "@> $1::jsonb" in query_arg
    assert json.loads(param_arg) == {"pathway": "MAPK"}


@pytest.mark.asyncio
async def test_claim_sequenced_samples_updates_only_claimed_rows() -> None:
    sample_id = uuid4()
    mock_conn = AsyncMock()
    mock_conn.fetch.return_value = [{"sample_id": sample_id}]
    with patch("app.repositories.gene_expression_repository.acquire_connection") as mock_acquire:
        mock_acquire.return_value.__aenter__.return_value = mock_conn
        repo = GeneExpressionRepository()
        claimed = await repo.claim_sequenced_samples(batch_size=5)

    assert claimed == [sample_id]
    mock_conn.execute.assert_awaited_once()
    update_query, ids_arg = mock_conn.execute.call_args.args
    assert "SKIP LOCKED" not in update_query
    assert ids_arg == [sample_id]


@pytest.mark.asyncio
async def test_claim_sequenced_samples_skips_update_when_empty() -> None:
    mock_conn = AsyncMock()
    mock_conn.fetch.return_value = []
    with patch("app.repositories.gene_expression_repository.acquire_connection") as mock_acquire:
        mock_acquire.return_value.__aenter__.return_value = mock_conn
        repo = GeneExpressionRepository()
        claimed = await repo.claim_sequenced_samples()

    assert claimed == []
    mock_conn.execute.assert_not_awaited()
