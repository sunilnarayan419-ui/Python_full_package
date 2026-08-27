from __future__ import annotations

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import asyncpg

_POOL: asyncpg.Pool | None = None


def _dsn_from_env() -> str:
    required = ("PGHOST", "PGPORT", "PGDATABASE", "PGUSER", "PGPASSWORD")
    missing = [key for key in required if not os.environ.get(key)]
    if missing:
        raise RuntimeError(f"Missing required database environment variables: {', '.join(missing)}")
    return (
        f"postgresql://{os.environ['PGUSER']}:{os.environ['PGPASSWORD']}"
        f"@{os.environ['PGHOST']}:{os.environ['PGPORT']}/{os.environ['PGDATABASE']}"
    )


async def init_pool(min_size: int = 5, max_size: int = 20) -> asyncpg.Pool:
    global _POOL
    if _POOL is None:
        _POOL = await asyncpg.create_pool(
            dsn=_dsn_from_env(), min_size=min_size, max_size=max_size, command_timeout=30.0
        )
    return _POOL


async def close_pool() -> None:
    global _POOL
    if _POOL is not None:
        await _POOL.close()
        _POOL = None


@asynccontextmanager
async def acquire_connection() -> AsyncIterator[asyncpg.Connection]:
    if _POOL is None:
        raise RuntimeError("Pool not initialized")
    async with _POOL.acquire() as connection:
        yield connection
