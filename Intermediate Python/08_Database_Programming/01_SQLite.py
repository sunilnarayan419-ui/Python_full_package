"""
01_SQLite.py

Production-oriented SQLite data-access layer for a small scientific data
platform. Demonstrates connection lifecycle, parameterized SQL, schema
constraints, indexing, and transaction-safe CRUD operations against a
'samples' / 'experiments' / 'measurements' schema.

SQLite is used here as a lightweight, embedded engine suitable for local
tooling, tests, and single-node deployments. It is NOT a substitute for a
networked, multi-writer production database such as PostgreSQL (see
02_PostgreSQL.py) -- SQLite serializes writers at the file/database level
and has no native concept of connection pooling or role-based access
control.
"""

from __future__ import annotations

import contextlib
import logging
import sqlite3
import tempfile
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

_SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS experiments (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    title           TEXT NOT NULL,
    principal_investigator TEXT NOT NULL,
    started_at      TEXT NOT NULL,
    CHECK (length(title) > 0)
);

CREATE TABLE IF NOT EXISTS samples (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    experiment_id   INTEGER NOT NULL REFERENCES experiments(id) ON DELETE CASCADE,
    species         TEXT NOT NULL,
    collection_location TEXT,
    UNIQUE (experiment_id, species, collection_location)
);

CREATE TABLE IF NOT EXISTS measurements (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id       INTEGER NOT NULL REFERENCES samples(id) ON DELETE CASCADE,
    metric_name     TEXT NOT NULL,
    metric_value    REAL NOT NULL,
    recorded_at     TEXT NOT NULL
);

-- Supports the common access pattern: "all measurements for a sample,
-- most recent first". Without this index, that query degrades to a full
-- table scan as measurements grow.
CREATE INDEX IF NOT EXISTS idx_measurements_sample_recorded
    ON measurements (sample_id, recorded_at DESC);

-- Supports listing samples that belong to a given experiment.
CREATE INDEX IF NOT EXISTS idx_samples_experiment
    ON samples (experiment_id);
"""


class SampleDatabaseError(RuntimeError):
    """Raised when a SQLite operation fails in an unrecoverable way."""


@dataclass(frozen=True, slots=True)
class Sample:
    id: int
    experiment_id: int
    species: str
    collection_location: str | None


class SqliteSampleStore:
    """
    Thin data-access layer around a SQLite database file.

    Each public method opens (or reuses, via context manager) a connection
    with an explicit lifecycle -- no connection is held open longer than
    the operation that needs it, and every connection is closed
    deterministically.
    """

    def __init__(self, db_path: str | Path) -> None:
        self._db_path = str(db_path)

    @contextlib.contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        try:
            conn.execute("PRAGMA foreign_keys = ON;")
            yield conn
        finally:
            conn.close()

    def initialize_schema(self) -> None:
        try:
            with self._connect() as conn, conn:
                conn.executescript(_SCHEMA)
        except sqlite3.Error as exc:
            raise SampleDatabaseError("failed to initialize schema") from exc

    def create_experiment(self, title: str, principal_investigator: str, started_at: str) -> int:
        query = (
            "INSERT INTO experiments (title, principal_investigator, started_at) "
            "VALUES (?, ?, ?)"
        )
        try:
            with self._connect() as conn, conn:
                cursor = conn.execute(query, (title, principal_investigator, started_at))
                return int(cursor.lastrowid)
        except sqlite3.Error as exc:
            raise SampleDatabaseError("failed to create experiment") from exc

    def create_sample(
        self, experiment_id: int, species: str, collection_location: str | None
    ) -> int:
        query = (
            "INSERT INTO samples (experiment_id, species, collection_location) "
            "VALUES (?, ?, ?)"
        )
        try:
            with self._connect() as conn, conn:
                cursor = conn.execute(query, (experiment_id, species, collection_location))
                return int(cursor.lastrowid)
        except sqlite3.IntegrityError as exc:
            raise SampleDatabaseError("sample violates a database constraint") from exc
        except sqlite3.Error as exc:
            raise SampleDatabaseError("failed to create sample") from exc

    def record_measurement(
        self, sample_id: int, metric_name: str, metric_value: float, recorded_at: str
    ) -> int:
        query = (
            "INSERT INTO measurements (sample_id, metric_name, metric_value, recorded_at) "
            "VALUES (?, ?, ?, ?)"
        )
        try:
            with self._connect() as conn, conn:
                cursor = conn.execute(query, (sample_id, metric_name, metric_value, recorded_at))
                return int(cursor.lastrowid)
        except sqlite3.Error as exc:
            raise SampleDatabaseError("failed to record measurement") from exc

    def get_sample(self, sample_id: int) -> Sample | None:
        query = (
            "SELECT id, experiment_id, species, collection_location "
            "FROM samples WHERE id = ?"
        )
        try:
            with self._connect() as conn:
                row = conn.execute(query, (sample_id,)).fetchone()
        except sqlite3.Error as exc:
            raise SampleDatabaseError("failed to fetch sample") from exc
        if row is None:
            return None
        return Sample(
            id=row["id"],
            experiment_id=row["experiment_id"],
            species=row["species"],
            collection_location=row["collection_location"],
        )

    def list_samples_for_experiment(self, experiment_id: int, limit: int = 100) -> Sequence[Sample]:
        query = (
            "SELECT id, experiment_id, species, collection_location "
            "FROM samples WHERE experiment_id = ? ORDER BY id LIMIT ?"
        )
        try:
            with self._connect() as conn:
                rows = conn.execute(query, (experiment_id, limit)).fetchall()
        except sqlite3.Error as exc:
            raise SampleDatabaseError("failed to list samples") from exc
        return [
            Sample(
                id=row["id"],
                experiment_id=row["experiment_id"],
                species=row["species"],
                collection_location=row["collection_location"],
            )
            for row in rows
        ]

    def update_sample_location(self, sample_id: int, collection_location: str) -> bool:
        query = "UPDATE samples SET collection_location = ? WHERE id = ?"
        try:
            with self._connect() as conn, conn:
                cursor = conn.execute(query, (collection_location, sample_id))
                return cursor.rowcount > 0
        except sqlite3.Error as exc:
            raise SampleDatabaseError("failed to update sample") from exc

    def delete_sample(self, sample_id: int) -> bool:
        query = "DELETE FROM samples WHERE id = ?"
        try:
            with self._connect() as conn, conn:
                cursor = conn.execute(query, (sample_id,))
                return cursor.rowcount > 0
        except sqlite3.Error as exc:
            raise SampleDatabaseError("failed to delete sample") from exc

    def record_experiment_with_samples(
        self,
        title: str,
        principal_investigator: str,
        started_at: str,
        species_list: Sequence[str],
    ) -> int:
        """
        Demonstrates a single multi-statement transaction: the experiment
        and all of its initial samples are created atomically. If any
        insert fails, the whole operation rolls back and no partial state
        is left behind.
        """
        try:
            with self._connect() as conn:
                with conn:  # conn used as a context manager => implicit
                             # BEGIN ... COMMIT/ROLLBACK around this block
                    cursor = conn.execute(
                        "INSERT INTO experiments (title, principal_investigator, started_at) "
                        "VALUES (?, ?, ?)",
                        (title, principal_investigator, started_at),
                    )
                    experiment_id = int(cursor.lastrowid)
                    for species in species_list:
                        conn.execute(
                            "INSERT INTO samples (experiment_id, species, collection_location) "
                            "VALUES (?, ?, NULL)",
                            (experiment_id, species),
                        )
                return experiment_id
        except sqlite3.Error as exc:
            raise SampleDatabaseError("failed to record experiment with samples") from exc


def _run_demo() -> None:
    logging.basicConfig(level=logging.INFO)

    # Avoid depending on a permanent local database file: use a temporary
    # directory that is cleaned up automatically.
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = Path(tmp_dir) / "scientific_platform.db"
        store = SqliteSampleStore(db_path)
        store.initialize_schema()

        experiment_id = store.record_experiment_with_samples(
            title="Drought Tolerance Screen - Batch 12",
            principal_investigator="Dr. A. Rao",
            started_at="2026-08-01",
            species_list=["Oryza sativa", "Zea mays"],
        )
        logger.info("created experiment id=%s", experiment_id)

        samples = store.list_samples_for_experiment(experiment_id)
        for sample in samples:
            store.record_measurement(
                sample_id=sample.id,
                metric_name="leaf_water_potential_mpa",
                metric_value=-1.2,
                recorded_at="2026-08-05T09:00:00",
            )

        updated = store.update_sample_location(samples[0].id, "Field Site 4")
        logger.info("updated first sample location: %s", updated)

        for sample in store.list_samples_for_experiment(experiment_id):
            print(f"sample id={sample.id} species={sample.species!r} "
                  f"location={sample.collection_location!r}")

        deleted = store.delete_sample(samples[-1].id)
        logger.info("deleted last sample: %s", deleted)


if __name__ == "__main__":
    _run_demo()
