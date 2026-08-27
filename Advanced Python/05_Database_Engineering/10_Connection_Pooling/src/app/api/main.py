from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.engine import engine, session_factory


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Warm the pool at startup so the first request doesn't pay a cold-start
    # connection cost, and dispose it cleanly at shutdown.
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with session_factory() as session:
        yield session


@app.get("/health/db")
async def db_health() -> dict[str, str]:
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    return {"status": "ok"}


@app.get("/health/pool")
async def pool_metrics() -> dict[str, int]:
    pool = engine.pool
    return {
        "checked_out": pool.checkedout(),
        "checked_in": pool.checkedin(),
        "overflow": pool.overflow(),
        "size": pool.size(),
    }
