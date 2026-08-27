from __future__ import annotations

from datetime import date
from decimal import Decimal

import asyncpg
import pytest

from app.repositories.screening_repository import ScreeningRepository

pytestmark = pytest.mark.integration


@pytest.fixture
async def seeded_conn(db_pool: asyncpg.Pool) -> asyncpg.Connection:
    async with db_pool.acquire() as conn:
        async with conn.transaction():
            researcher_id = await conn.fetchval(
                """
                INSERT INTO researchers (full_name, email, department)
                VALUES ($1, $2, $3) RETURNING researcher_id
                """,
                "Dr. Elena Voss",
                "e.voss@example-pharma.test",
                "Medicinal Chemistry",
            )
            project_id = await conn.fetchval(
                """
                INSERT INTO research_projects
                    (project_code, title, lead_researcher_id, status, started_at)
                VALUES ($1, $2, $3, 'active', $4) RETURNING project_id
                """,
                "PRJ-EGFR-01",
                "EGFR Inhibitor Discovery",
                researcher_id,
                date(2025, 1, 1),
            )
            compound_id = await conn.fetchval(
                """
                INSERT INTO compounds
                    (project_id, smiles, molecular_weight, inchi_key, synthesized_at)
                VALUES ($1, $2, $3, $4, $5) RETURNING compound_id
                """,
                project_id,
                "CC(=O)OC1=CC=CC=C1C(=O)O",
                180.16,
                "BSYNRYMUTXBXSQ-UHFFFAOYSA-N",
                date(2025, 2, 1),
            )
            target_id = await conn.fetchval(
                """
                INSERT INTO molecular_targets (gene_symbol, uniprot_accession, target_class)
                VALUES ($1, $2, $3) RETURNING target_id
                """,
                "EGFR",
                "P00533",
                "kinase",
            )
            assay_id = await conn.fetchval(
                """
                INSERT INTO assays (target_id, assay_name, assay_type, readout_unit)
                VALUES ($1, $2, 'binding', 'nM') RETURNING assay_id
                """,
                target_id,
                "EGFR Binding Assay",
            )
            run_id = await conn.fetchval(
                """
                INSERT INTO screening_runs (assay_id, operator_id, run_date, plate_count)
                VALUES ($1, $2, $3, 4) RETURNING screening_run_id
                """,
                assay_id,
                researcher_id,
                date(2025, 3, 1),
            )
        yield conn, {"compound_id": compound_id, "run_id": run_id, "project_id": project_id}


@pytest.mark.asyncio
async def test_upsert_then_potency_rank_reflects_seeded_data(
    seeded_conn: tuple[asyncpg.Connection, dict],
) -> None:
    conn, ids = seeded_conn
    repo = ScreeningRepository()
    result = await repo.upsert_result(
        screening_run_id=ids["run_id"],
        compound_id=ids["compound_id"],
        potency_nm=Decimal("8.2000"),
        percent_inhibition=Decimal("95.10"),
        is_hit=True,
    )
    assert result.screening_result_id > 0

    ranked = await repo.top_potency_by_target(limit=10)
    assert any(row.compound_id == ids["compound_id"] for row in ranked)


@pytest.mark.asyncio
async def test_upsert_is_idempotent_on_conflict(
    seeded_conn: tuple[asyncpg.Connection, dict],
) -> None:
    conn, ids = seeded_conn
    repo = ScreeningRepository()
    first = await repo.upsert_result(
        screening_run_id=ids["run_id"],
        compound_id=ids["compound_id"],
        potency_nm=Decimal("50.0"),
        percent_inhibition=Decimal("60.0"),
        is_hit=False,
    )
    second = await repo.upsert_result(
        screening_run_id=ids["run_id"],
        compound_id=ids["compound_id"],
        potency_nm=Decimal("5.0"),
        percent_inhibition=Decimal("99.0"),
        is_hit=True,
    )
    assert first.screening_result_id == second.screening_result_id

    row = await conn.fetchrow(
        "SELECT potency_nm, is_hit FROM screening_results WHERE screening_result_id = $1",
        second.screening_result_id,
    )
    assert row["potency_nm"] == Decimal("5.0000")
    assert row["is_hit"] is True


@pytest.mark.asyncio
async def test_complete_project_is_a_no_op_when_already_completed(
    seeded_conn: tuple[asyncpg.Connection, dict],
) -> None:
    conn, ids = seeded_conn
    repo = ScreeningRepository()
    first = await repo.complete_project(
        project_id=ids["project_id"], ended_at=date(2025, 6, 1)
    )
    second = await repo.complete_project(
        project_id=ids["project_id"], ended_at=date(2025, 6, 2)
    )
    assert first is True
    assert second is False
