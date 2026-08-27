from __future__ import annotations

import os
from pathlib import Path

import asyncpg
import pytest

SCHEMA_PATH = Path(__file__).resolve().parents[2] / "sql" / "schema.sql"


def _test_dsn() -> str:
    return (
        f"postgresql://{os.environ['PGUSER']}:{os.environ['PGPASSWORD']}"
        f"@{os.environ['PGHOST']}:{os.environ['PGPORT']}/{os.environ['PGDATABASE_TEST']}"
    )


@pytest.fixture(scope="session")
async def db_pool() -> asyncpg.Pool:
    pool = await asyncpg.create_pool(dsn=_test_dsn(), min_size=1, max_size=5)
    async with pool.acquire() as conn:
        await conn.execute(SCHEMA_PATH.read_text())
    yield pool
    await pool.close()


@pytest.fixture(autouse=True)
async def _clean_tables(db_pool: asyncpg.Pool) -> None:
    yield
    async with db_pool.acquire() as conn:
        await conn.execute(
            """
            TRUNCATE TABLE
                screening_results, screening_runs, assays, molecular_targets,
                compounds, research_projects, researchers
            RESTART IDENTITY CASCADE
            """
        )
