from __future__ import annotations

from datetime import date
from decimal import Decimal
from unittest.mock import AsyncMock, patch

import pytest

from app.repositories.screening_repository import (
    AssayHitRate,
    PotencyRankRow,
    ScreeningRepository,
    ScreeningResultRow,
)


@pytest.mark.asyncio
async def test_top_potency_by_target_maps_rows_to_dataclass() -> None:
    fake_rows = [
        {
            "compound_id": 101,
            "inchi_key": "ABCXYZ-UHFFFAOYSA-N",
            "gene_symbol": "EGFR",
            "potency_nm": Decimal("12.5000"),
            "potency_rank": 1,
        }
    ]
    mock_conn = AsyncMock()
    mock_conn.fetch.return_value = fake_rows

    with patch(
        "app.repositories.screening_repository.acquire_connection"
    ) as mock_acquire:
        mock_acquire.return_value.__aenter__.return_value = mock_conn
        repo = ScreeningRepository()
        result = await repo.top_potency_by_target(limit=50)

    assert result == [
        PotencyRankRow(
            compound_id=101,
            inchi_key="ABCXYZ-UHFFFAOYSA-N",
            gene_symbol="EGFR",
            potency_nm=Decimal("12.5000"),
            potency_rank=1,
        )
    ]
    mock_conn.fetch.assert_awaited_once()
    called_query, called_limit = mock_conn.fetch.call_args.args
    assert "PARTITION BY mt.target_id" in called_query
    assert called_limit == 50


@pytest.mark.asyncio
async def test_hit_rate_by_assay_filters_low_volume_assays() -> None:
    fake_rows = [
        {
            "assay_id": 7,
            "assay_name": "EGFR Binding Assay",
            "total_results": 240,
            "total_hits": 18,
            "hit_rate_pct": Decimal("7.50"),
        }
    ]
    mock_conn = AsyncMock()
    mock_conn.fetch.return_value = fake_rows

    with patch(
        "app.repositories.screening_repository.acquire_connection"
    ) as mock_acquire:
        mock_acquire.return_value.__aenter__.return_value = mock_conn
        repo = ScreeningRepository()
        result = await repo.hit_rate_by_assay(min_results=10)

    assert result == [
        AssayHitRate(
            assay_id=7,
            assay_name="EGFR Binding Assay",
            total_results=240,
            total_hits=18,
            hit_rate_pct=Decimal("7.50"),
        )
    ]


@pytest.mark.asyncio
async def test_upsert_result_raises_when_no_row_returned() -> None:
    mock_conn = AsyncMock()
    mock_conn.fetchrow.return_value = None

    with patch(
        "app.repositories.screening_repository.transaction"
    ) as mock_txn:
        mock_txn.return_value.__aenter__.return_value = mock_conn
        repo = ScreeningRepository()
        with pytest.raises(RuntimeError, match="did not return"):
            await repo.upsert_result(
                screening_run_id=1,
                compound_id=2,
                potency_nm=Decimal("45.0"),
                percent_inhibition=Decimal("87.3"),
                is_hit=True,
            )


@pytest.mark.asyncio
async def test_upsert_result_returns_result_id_on_success() -> None:
    mock_conn = AsyncMock()
    mock_conn.fetchrow.return_value = {"screening_result_id": 999}

    with patch(
        "app.repositories.screening_repository.transaction"
    ) as mock_txn:
        mock_txn.return_value.__aenter__.return_value = mock_conn
        repo = ScreeningRepository()
        result = await repo.upsert_result(
            screening_run_id=1,
            compound_id=2,
            potency_nm=Decimal("45.0"),
            percent_inhibition=Decimal("87.3"),
            is_hit=True,
        )

    assert result == ScreeningResultRow(screening_result_id=999)


@pytest.mark.asyncio
async def test_complete_project_returns_false_when_not_active() -> None:
    mock_conn = AsyncMock()
    mock_conn.fetchrow.return_value = None

    with patch(
        "app.repositories.screening_repository.transaction"
    ) as mock_txn:
        mock_txn.return_value.__aenter__.return_value = mock_conn
        repo = ScreeningRepository()
        completed = await repo.complete_project(
            project_id=5, ended_at=date(2026, 1, 1)
        )

    assert completed is False
