"""
02_PostgreSQL.py

Production-oriented PostgreSQL integration for the scientific data
platform, using the modern `psycopg` (psycopg3) driver.

Configuration is entirely environment-based (DATABASE_URL). No
credentials are hard-coded, logged, or printed. If psycopg is not
installed, or DATABASE_URL is not configured, the module fails gracefully
with a clear diagnostic instead of raising an opaque ImportError or
attempting a network connection.

This module intentionally mirrors the domain used in 01_SQLite.py
(experiments / samples / measurements) but uses PostgreSQL-specific
types and features (SERIAL/IDENTITY, TIMESTAMPTZ, numeric, ON CONFLICT)
rather than SQLite syntax.
"""

from __future__ import annotations

import logging
import os
from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass

logger = logging.getLogger(__name__)

try:
    import psycopg
    from psycopg import errors as pg_errors
    from psycopg.rows import dict_row
    _PSYCOPG_AVAILABLE = True
except ImportError:  # pragma: no cover - environment dependent
    _PSYCOPG_AVAILABLE = False


class PostgresUnavailableError(RuntimeError):
    """Raised when the psycopg driver or DATABASE_URL is not available."""


class PostgresOperationError(RuntimeError):
    """Raised when a PostgreSQL operation fails."""


_SCHEMA = """
CREATE TABLE IF NOT EXISTS experiments (
    id                  BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title               TEXT NOT NULL CHECK (length(title) > 0),
    principal_investigator TEXT NOT NULL,
    started_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS samples (
    id                  BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    experiment_id       BIGINT NOT NULL REFERENCES experiments(id) ON DELETE CASCADE,
    species             TEXT NOT NULL,
    collection_location TEXT,
    UNIQUE (experiment_id, species, collection_location)
);

CREATE TABLE IF NOT EXISTS measurements (
    id                  BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    sample_id           BIGINT NOT NULL REFERENCES samples(id) ON DELETE CASCADE,
    metric_name         TEXT NOT NULL,
    metric_value        NUMERIC(12, 4) NOT NULL,
    recorded_at         TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_measurements_sample_recorded
    ON measurements (sample_id, recorded_at DESC);

CREATE INDEX IF NOT EXISTS idx_samples_experiment
    ON samples (experiment_id);
"""


@dataclass(frozen=True, slots=True)
class Sample:
    id: int
    experiment_id: int
    species: str
    collection_location: str | None


def _get_database_url() -> str:
    """
    Reads DATABASE_URL from the environment. Never hard-codes credentials
    and never logs the full connection string, since it may embed a
    password.
    """
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise PostgresUnavailableError(
            "DATABASE_URL is not set; PostgreSQL features are disabled. "
            "Set DATABASE_URL to a valid postgresql:// connection string "
            "to enable this module."
        )
    return database_url


class PostgresSampleStore:
    """
    Data-access layer for PostgreSQL, using short-lived connections
    obtained per-operation. In a real service this would typically sit
    behind the connection pool shown in 07_Connection_Pooling.py rather
    than opening a fresh connection per call.
    """

    def __init__(self, database_url: str | None = None) -> None:
        if not _PSYCOPG_AVAILABLE:
            raise PostgresUnavailableError(
                "psycopg is not installed. Install it with "
                "`pip install \"psycopg[binary]\"` to use PostgreSQL features."
            )
        self._database_url = database_url or _get_database_url()

    @contextmanager
    def _connect(self) -> Iterator["psycopg.Connection"]:
        try:
            conn = psycopg.connect(self._database_url, row_factory=dict_row)
        except psycopg.OperationalError as exc:
            # Do not leak the connection string (may contain credentials).
            raise PostgresOperationError("could not connect to PostgreSQL") from exc
        try:
            yield conn
        finally:
            conn.close()

    def initialize_schema(self) -> None:
        try:
            with self._connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(_SCHEMA)
                conn.commit()
        except psycopg.Error as exc:
            raise PostgresOperationError("failed to initialize schema") from exc

    def create_experiment(self, title: str, principal_investigator: str) -> int:
        query = (
            "INSERT INTO experiments (title, principal_investigator) "
            "VALUES (%s, %s) RETURNING id"
        )
        try:
            with self._connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (title, principal_investigator))
                    row = cur.fetchone()
                conn.commit()
                return int(row["id"])
        except psycopg.Error as exc:
            raise PostgresOperationError("failed to create experiment") from exc

    def upsert_sample(
        self, experiment_id: int, species: str, collection_location: str | None
    ) -> int:
        """
        Demonstrates a PostgreSQL-specific idiom: INSERT ... ON CONFLICT
        DO UPDATE, relying on the UNIQUE constraint defined in the schema.
        """
        query = """
            INSERT INTO samples (experiment_id, species, collection_location)
            VALUES (%s, %s, %s)
            ON CONFLICT (experiment_id, species, collection_location)
            DO UPDATE SET collection_location = EXCLUDED.collection_location
            RETURNING id
        """
        try:
            with self._connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (experiment_id, species, collection_location))
                    row = cur.fetchone()
                conn.commit()
                return int(row["id"])
        except pg_errors.ForeignKeyViolation as exc:
            raise PostgresOperationError("experiment does not exist") from exc
        except psycopg.Error as exc:
            raise PostgresOperationError("failed to upsert sample") from exc

    def list_samples_for_experiment(self, experiment_id: int, limit: int = 100) -> Sequence[Sample]:
        query = (
            "SELECT id, experiment_id, species, collection_location "
            "FROM samples WHERE experiment_id = %s ORDER BY id LIMIT %s"
        )
        try:
            with self._connect() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (experiment_id, limit))
                    rows = cur.fetchall()
        except psycopg.Error as exc:
            raise PostgresOperationError("failed to list samples") from exc
        return [
            Sample(
                id=r["id"],
                experiment_id=r["experiment_id"],
                species=r["species"],
                collection_location=r["collection_location"],
            )
            for r in rows
        ]


def _run_demo() -> None:
    logging.basicConfig(level=logging.INFO)

    if not _PSYCOPG_AVAILABLE:
        print("psycopg is not installed; skipping PostgreSQL demo. "
              "Install with: pip install \"psycopg[binary]\"")
        return

    try:
        store = PostgresSampleStore()
    except PostgresUnavailableError as exc:
        print(f"PostgreSQL demo skipped: {exc}")
        return

    try:
        store.initialize_schema()
        experiment_id = store.create_experiment(
            title="Nitrogen Uptake Trial",
            principal_investigator="Dr. S. Iyer",
        )
        sample_id = store.upsert_sample(
            experiment_id, species="Triticum aestivum", collection_location="Greenhouse 2"
        )
        logger.info("created sample id=%s in experiment id=%s", sample_id, experiment_id)
        for sample in store.list_samples_for_experiment(experiment_id):
            print(f"sample id={sample.id} species={sample.species!r}")
    except PostgresOperationError as exc:
        print(f"PostgreSQL demo failed: {exc}")


if __name__ == "__main__":
    _run_demo()
