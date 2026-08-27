"""
07_Connection_Pooling.py

Production connection-pool configuration and lifecycle management using
SQLAlchemy's Engine-level pooling. Demonstrates how pool_size,
max_overflow, pool_timeout, pool_recycle, and pool_pre_ping interact, and
how to check connections out and back in safely without leaking them.

Pool sizing is deliberately NOT hard-coded to fixed "good" numbers in
business logic. It is externalized to configuration because the correct
values depend on:

  - the target database's max_connections and available resources
  - how many application processes/workers will each hold their own pool
  - the application's expected concurrency and query latency
  - the deployment environment (a laptop, CI, or a multi-node cluster)

A single Engine (and therefore a single pool) should be created once per
process and reused -- not recreated per request, which defeats pooling
entirely and can exhaust the database's connection limit under load.
"""

from __future__ import annotations

import logging
import os
from contextlib import contextmanager
from dataclasses import dataclass

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class PoolConfig:
    """
    Externalized pool configuration. Defaults here are conservative
    starting points for a small service, not universal recommendations --
    they must be tuned against real database capacity and measured
    application concurrency before being trusted in production.
    """

    database_url: str
    pool_size: int = 5
    max_overflow: int = 5
    pool_timeout_seconds: int = 30
    # Recycle connections periodically so the app doesn't hold connections
    # that a middlebox, load balancer, or the database itself may have
    # silently dropped after a period of inactivity.
    pool_recycle_seconds: int = 1800
    # Issue a lightweight "SELECT 1"-style check before handing a pooled
    # connection back to application code, so a connection that died
    # while idle in the pool doesn't surface as a confusing query error.
    pool_pre_ping: bool = True
    echo: bool = False

    @classmethod
    def from_environment(cls) -> "PoolConfig":
        database_url = os.environ.get("DATABASE_URL")
        if not database_url:
            # Falls back to an in-memory SQLite engine so this module is
            # runnable without external configuration. SQLite's pooling
            # semantics differ substantially from a networked database
            # (see the caveat printed in the demo below).
            database_url = "sqlite+pysqlite:///:memory:"
        return cls(
            database_url=database_url,
            pool_size=int(os.environ.get("DB_POOL_SIZE", "5")),
            max_overflow=int(os.environ.get("DB_MAX_OVERFLOW", "5")),
            pool_timeout_seconds=int(os.environ.get("DB_POOL_TIMEOUT", "30")),
            pool_recycle_seconds=int(os.environ.get("DB_POOL_RECYCLE", "1800")),
            pool_pre_ping=os.environ.get("DB_POOL_PRE_PING", "true").lower() == "true",
            echo=os.environ.get("DB_ECHO", "false").lower() == "true",
        )


def build_engine(config: PoolConfig) -> Engine:
    kwargs = dict(
        pool_pre_ping=config.pool_pre_ping,
        pool_recycle=config.pool_recycle_seconds,
        echo=config.echo,
    )
    # SQLite's default pool (SingletonThreadPool / NullPool depending on
    # URL) does not accept pool_size/max_overflow/pool_timeout the way a
    # networked-database dialect (e.g. PostgreSQL via QueuePool) does.
    # Only pass those knobs for dialects that support QueuePool-style
    # sizing.
    if not config.database_url.startswith("sqlite"):
        kwargs.update(
            pool_size=config.pool_size,
            max_overflow=config.max_overflow,
            pool_timeout=config.pool_timeout_seconds,
        )
    return create_engine(config.database_url, **kwargs)


class DatabaseGateway:
    """
    Owns exactly one Engine (and therefore one pool) for the lifetime of
    the process. Application code obtains short-lived Sessions from this
    gateway rather than constructing Engines itself.
    """

    def __init__(self, config: PoolConfig) -> None:
        self._config = config
        self._engine = build_engine(config)

    @contextmanager
    def session(self):
        """
        Checks a pooled connection out for the duration of the `with`
        block and guarantees it is returned to the pool afterward, even
        on error -- the Session close() releases its underlying
        connection back to the pool rather than closing the physical
        socket.
        """
        session = Session(self._engine)
        try:
            yield session
        finally:
            session.close()  # returns the connection to the pool

    def healthcheck(self) -> bool:
        try:
            with self._engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except SQLAlchemyError as exc:
            logger.error("database healthcheck failed: %s", exc)
            return False

    def pool_status(self) -> str:
        # Engine.pool.status() gives a human-readable snapshot of
        # checked-out vs. available connections -- useful for dashboards
        # and incident diagnostics, without exposing the connection URL.
        return self._engine.pool.status()

    def dispose(self) -> None:
        """
        Closes every pooled connection. Call this once at process
        shutdown, not per request.
        """
        self._engine.dispose()


def _run_demo() -> None:
    logging.basicConfig(level=logging.INFO)

    config = PoolConfig.from_environment()
    gateway = DatabaseGateway(config)

    try:
        print(f"healthcheck ok={gateway.healthcheck()}")
        print(f"pool status: {gateway.pool_status()}")

        # Simulate several short-lived units of work reusing the same
        # pool instead of opening a new physical connection each time.
        for i in range(3):
            with gateway.session() as session:
                session.execute(text("SELECT :n AS n"), {"n": i}).one()

        print(f"pool status after workload: {gateway.pool_status()}")

        if config.database_url.startswith("sqlite"):
            print(
                "note: SQLite does not use QueuePool-style pool_size/"
                "max_overflow; those settings only take effect for "
                "networked dialects such as PostgreSQL."
            )
    finally:
        gateway.dispose()


if __name__ == "__main__":
    _run_demo()
