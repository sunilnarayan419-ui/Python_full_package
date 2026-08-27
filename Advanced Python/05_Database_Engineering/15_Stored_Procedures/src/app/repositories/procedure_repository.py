from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

import asyncpg


@dataclass(frozen=True, slots=True)
class PotencyPercentileRow:
    compound_id: int
    potency_nm: Decimal
    percentile: Decimal


class ProcedureRepository:
    """Every invocation below uses parameterized calls -- never string-formatted SQL --
    even though the callee is a trusted, statically-named database function."""

    def __init__(self, pool: asyncpg.Pool) -> None:
        self._pool = pool

    async def compound_potency_percentiles(self, target_id: int) -> list[PotencyPercentileRow]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM fn_compound_potency_percentile($1)", target_id
            )
        return [PotencyPercentileRow(**dict(row)) for row in rows]

    async def lipinski_violations(
        self, *, molecular_weight: Decimal, logp: Decimal, hbd: int, hba: int
    ) -> int:
        async with self._pool.acquire() as conn:
            return await conn.fetchval(
                "SELECT fn_lipinski_violations($1, $2, $3, $4)",
                molecular_weight,
                logp,
                hbd,
                hba,
            )

    async def archive_completed_project(self, project_id: int) -> None:
        async with self._pool.acquire() as conn:
            try:
                await conn.execute("CALL sp_archive_completed_project($1)", project_id)
            except asyncpg.RaiseError as exc:
                # Surface the database's specific, human-readable error rather than
                # letting a generic asyncpg exception propagate uninterpreted.
                raise ValueError(str(exc)) from exc
