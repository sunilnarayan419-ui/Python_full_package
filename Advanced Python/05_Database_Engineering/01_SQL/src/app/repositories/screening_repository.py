from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal

import asyncpg

from app.database.connection import acquire_connection, transaction


@dataclass(frozen=True, slots=True)
class PotencyRankRow:
    compound_id: int
    inchi_key: str
    gene_symbol: str
    potency_nm: Decimal
    potency_rank: int


@dataclass(frozen=True, slots=True)
class AssayHitRate:
    assay_id: int
    assay_name: str
    total_results: int
    total_hits: int
    hit_rate_pct: Decimal | None


@dataclass(frozen=True, slots=True)
class ScreeningResultRow:
    screening_result_id: int


class ScreeningRepository:
    """Read/write access to screening data using only parameterized SQL."""

    async def top_potency_by_target(self, limit: int = 100) -> list[PotencyRankRow]:
        query = """
            SELECT compound_id, inchi_key, gene_symbol, potency_nm, potency_rank
            FROM (
                SELECT
                    c.compound_id,
                    c.inchi_key,
                    mt.gene_symbol,
                    sr.potency_nm,
                    RANK() OVER (
                        PARTITION BY mt.target_id
                        ORDER BY sr.potency_nm ASC NULLS LAST
                    ) AS potency_rank
                FROM screening_results sr
                JOIN compounds c ON c.compound_id = sr.compound_id
                JOIN screening_runs run ON run.screening_run_id = sr.screening_run_id
                JOIN assays a ON a.assay_id = run.assay_id
                JOIN molecular_targets mt ON mt.target_id = a.target_id
                WHERE sr.potency_nm IS NOT NULL
            ) ranked
            WHERE potency_rank <= 5
            ORDER BY gene_symbol, potency_rank
            LIMIT $1
        """
        async with acquire_connection() as conn:
            rows = await conn.fetch(query, limit)
        return [PotencyRankRow(**dict(row)) for row in rows]

    async def hit_rate_by_assay(self, min_results: int = 10) -> list[AssayHitRate]:
        query = """
            SELECT
                a.assay_id,
                a.assay_name,
                COUNT(*) AS total_results,
                COUNT(*) FILTER (WHERE sr.is_hit) AS total_hits,
                ROUND(
                    COUNT(*) FILTER (WHERE sr.is_hit)::NUMERIC
                    / NULLIF(COUNT(*), 0) * 100, 2
                ) AS hit_rate_pct
            FROM screening_results sr
            JOIN screening_runs run ON run.screening_run_id = sr.screening_run_id
            JOIN assays a ON a.assay_id = run.assay_id
            GROUP BY a.assay_id, a.assay_name
            HAVING COUNT(*) >= $1
            ORDER BY hit_rate_pct DESC
        """
        async with acquire_connection() as conn:
            rows = await conn.fetch(query, min_results)
        return [AssayHitRate(**dict(row)) for row in rows]

    async def upsert_result(
        self,
        *,
        screening_run_id: int,
        compound_id: int,
        potency_nm: Decimal | None,
        percent_inhibition: Decimal | None,
        is_hit: bool,
    ) -> ScreeningResultRow:
        query = """
            INSERT INTO screening_results (
                screening_run_id, compound_id, potency_nm, percent_inhibition, is_hit
            )
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (screening_run_id, compound_id)
            DO UPDATE SET
                potency_nm = EXCLUDED.potency_nm,
                percent_inhibition = EXCLUDED.percent_inhibition,
                is_hit = EXCLUDED.is_hit,
                measured_at = now()
            RETURNING screening_result_id
        """
        async with transaction() as conn:
            row = await conn.fetchrow(
                query,
                screening_run_id,
                compound_id,
                potency_nm,
                percent_inhibition,
                is_hit,
            )
        if row is None:
            raise RuntimeError("Upsert did not return a screening_result_id")
        return ScreeningResultRow(screening_result_id=row["screening_result_id"])

    async def compound_lineage(self, compound_id: int) -> list[dict]:
        query = """
            WITH RECURSIVE compound_lineage AS (
                SELECT compound_id, parent_compound_id, inchi_key, 0 AS depth
                FROM compounds
                WHERE compound_id = $1

                UNION ALL

                SELECT c.compound_id, c.parent_compound_id, c.inchi_key, cl.depth + 1
                FROM compounds c
                JOIN compound_lineage cl ON c.parent_compound_id = cl.compound_id
            )
            SELECT * FROM compound_lineage ORDER BY depth
        """
        async with acquire_connection() as conn:
            rows = await conn.fetch(query, compound_id)
        return [dict(row) for row in rows]

    async def complete_project(
        self, *, project_id: int, ended_at: date
    ) -> bool:
        query = """
            UPDATE research_projects
            SET status = 'completed', ended_at = $2
            WHERE project_id = $1 AND status = 'active'
            RETURNING project_id
        """
        async with transaction() as conn:
            row = await conn.fetchrow(query, project_id, ended_at)
        return row is not None
