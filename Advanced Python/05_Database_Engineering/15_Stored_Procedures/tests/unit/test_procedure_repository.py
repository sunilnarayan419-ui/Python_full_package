from __future__ import annotations

from decimal import Decimal
from unittest.mock import AsyncMock

import asyncpg
import pytest

from app.repositories.procedure_repository import PotencyPercentileRow, ProcedureRepository


@pytest.mark.asyncio
async def test_compound_potency_percentiles_maps_rows() -> None:
    fake_conn = AsyncMock()
    fake_conn.fetch.return_value = [
        {"compound_id": 1, "potency_nm": Decimal("10.0"), "percentile": Decimal("0.9500")}
    ]
    pool = AsyncMock()
    pool.acquire.return_value.__aenter__.return_value = fake_conn

    repo = ProcedureRepository(pool)
    result = await repo.compound_potency_percentiles(target_id=7)

    assert result == [
        PotencyPercentileRow(compound_id=1, potency_nm=Decimal("10.0"), percentile=Decimal("0.9500"))
    ]
    fake_conn.fetch.assert_awaited_once_with(
        "SELECT * FROM fn_compound_potency_percentile($1)", 7
    )


@pytest.mark.asyncio
async def test_archive_completed_project_wraps_raise_error() -> None:
    fake_conn = AsyncMock()
    fake_conn.execute.side_effect = asyncpg.RaiseError("project 5 is not completed (status=active)")
    pool = AsyncMock()
    pool.acquire.return_value.__aenter__.return_value = fake_conn

    repo = ProcedureRepository(pool)
    with pytest.raises(ValueError, match="not completed"):
        await repo.archive_completed_project(5)


@pytest.mark.asyncio
async def test_lipinski_violations_uses_parameterized_call() -> None:
    fake_conn = AsyncMock()
    fake_conn.fetchval.return_value = 2
    pool = AsyncMock()
    pool.acquire.return_value.__aenter__.return_value = fake_conn

    repo = ProcedureRepository(pool)
    result = await repo.lipinski_violations(
        molecular_weight=Decimal("520"), logp=Decimal("6.1"), hbd=2, hba=4
    )

    assert result == 2
    query_arg = fake_conn.fetchval.call_args.args[0]
    assert "fn_lipinski_violations($1, $2, $3, $4)" in query_arg
