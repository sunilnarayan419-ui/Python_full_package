from __future__ import annotations

import os

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine


def _database_url() -> str:
    required = ("PGHOST", "PGPORT", "PGDATABASE", "PGUSER", "PGPASSWORD")
    missing = [key for key in required if not os.environ.get(key)]
    if missing:
        raise RuntimeError(f"Missing required database environment variables: {', '.join(missing)}")
    return (
        f"postgresql+asyncpg://{os.environ['PGUSER']}:{os.environ['PGPASSWORD']}"
        f"@{os.environ['PGHOST']}:{os.environ['PGPORT']}/{os.environ['PGDATABASE']}"
    )


def build_engine() -> AsyncEngine:
    """
    Pool sizing rationale for a FastAPI deployment running N Uvicorn workers:

    - pool_size: steady-state connections held open per worker process. Set so that
      (pool_size * worker_count) stays comfortably under PostgreSQL's max_connections
      (default 100), leaving headroom for migrations, admin tools, and other services.
    - max_overflow: extra connections allowed under burst load beyond pool_size, closed
      once load subsides. Keeps burst capacity without permanently reserving DB slots.
    - pool_timeout: how long a request waits for a free connection before failing fast
      with a clear error, instead of queuing indefinitely and cascading into timeouts.
    - pool_recycle: forces reconnection before a cloud load balancer or PgBouncer
      silently drops long-idle TCP connections (typically 300-1800s).
    - pool_pre_ping: issues a cheap SELECT 1 before handing out a pooled connection,
      converting "connection was closed by the server" into a transparent reconnect
      instead of a query-time failure.
    """
    return create_async_engine(
        _database_url(),
        pool_size=10,
        max_overflow=10,
        pool_timeout=5.0,
        pool_recycle=1800,
        pool_pre_ping=True,
        echo=False,
    )


# Created once per process at import time -- never per-request. Creating a new engine
# (and therefore a new pool) inside a request handler defeats pooling entirely and will
# exhaust PostgreSQL's max_connections under any real load.
engine: AsyncEngine = build_engine()
session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine, expire_on_commit=False
)
