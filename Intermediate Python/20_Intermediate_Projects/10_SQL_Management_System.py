from __future__ import annotations

import logging
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterator

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")


class RecordValidationError(Exception):
    """Raised when a research measurement record fails validation."""


class RecordNotFoundError(Exception):
    """Raised when a requested record id does not exist."""


@dataclass(frozen=True, slots=True)
class MeasurementRecord:
    id: int | None
    plant_id: str
    species: str
    height_cm: float
    biomass_g: float
    measurement_date: date


class MeasurementValidator:
    """Validates measurement records before persistence."""

    def validate(self, record: MeasurementRecord) -> None:
        if not record.plant_id.strip():
            raise RecordValidationError("plant_id cannot be blank.")
        if not record.species.strip():
            raise RecordValidationError("species cannot be blank.")
        if record.height_cm <= 0:
            raise RecordValidationError("height_cm must be positive.")
        if record.biomass_g <= 0:
            raise RecordValidationError("biomass_g must be positive.")


class Database:
    """Manages a SQLite connection lifecycle for the research measurement system."""

    def __init__(self, path: Path | str = ":memory:") -> None:
        self._path = str(path)
        self._connection = sqlite3.connect(self._path)
        self._connection.execute("PRAGMA foreign_keys = ON")
        self._initialize_schema()

    def _initialize_schema(self) -> None:
        with self.transaction() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS measurements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    plant_id TEXT NOT NULL,
                    species TEXT NOT NULL,
                    height_cm REAL NOT NULL,
                    biomass_g REAL NOT NULL,
                    measurement_date TEXT NOT NULL
                )
                """
            )

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Cursor]:
        cursor = self._connection.cursor()
        try:
            yield cursor
            self._connection.commit()
        except sqlite3.Error:
            self._connection.rollback()
            raise

    def close(self) -> None:
        self._connection.close()


class MeasurementRepository:
    """Repository providing parameterized CRUD operations for measurement records."""

    def __init__(self, database: Database, validator: MeasurementValidator | None = None) -> None:
        self._database = database
        self._validator = validator or MeasurementValidator()

    def create(self, record: MeasurementRecord) -> MeasurementRecord:
        self._validator.validate(record)
        with self._database.transaction() as cursor:
            cursor.execute(
                """
                INSERT INTO measurements (plant_id, species, height_cm, biomass_g, measurement_date)
                VALUES (?, ?, ?, ?, ?)
                """,
                (record.plant_id, record.species, record.height_cm, record.biomass_g,
                 record.measurement_date.isoformat()),
            )
            new_id = cursor.lastrowid
        return self.get(new_id)

    def get(self, record_id: int) -> MeasurementRecord:
        with self._database.transaction() as cursor:
            cursor.execute(
                "SELECT id, plant_id, species, height_cm, biomass_g, measurement_date "
                "FROM measurements WHERE id = ?",
                (record_id,),
            )
            row = cursor.fetchone()
        if row is None:
            raise RecordNotFoundError(f"Measurement {record_id} not found.")
        return self._row_to_record(row)

    def list_by_species(self, species: str) -> list[MeasurementRecord]:
        with self._database.transaction() as cursor:
            cursor.execute(
                "SELECT id, plant_id, species, height_cm, biomass_g, measurement_date "
                "FROM measurements WHERE species = ? ORDER BY measurement_date",
                (species,),
            )
            rows = cursor.fetchall()
        return [self._row_to_record(row) for row in rows]

    def update_measurements(self, record_id: int, height_cm: float, biomass_g: float) -> MeasurementRecord:
        existing = self.get(record_id)
        updated = MeasurementRecord(
            id=existing.id, plant_id=existing.plant_id, species=existing.species,
            height_cm=height_cm, biomass_g=biomass_g, measurement_date=existing.measurement_date,
        )
        self._validator.validate(updated)
        with self._database.transaction() as cursor:
            cursor.execute(
                "UPDATE measurements SET height_cm = ?, biomass_g = ? WHERE id = ?",
                (height_cm, biomass_g, record_id),
            )
        return self.get(record_id)

    def delete(self, record_id: int) -> None:
        self.get(record_id)
        with self._database.transaction() as cursor:
            cursor.execute("DELETE FROM measurements WHERE id = ?", (record_id,))

    def average_biomass_by_species(self) -> dict[str, float]:
        with self._database.transaction() as cursor:
            cursor.execute(
                "SELECT species, AVG(biomass_g) FROM measurements GROUP BY species"
            )
            rows = cursor.fetchall()
        return {species: round(avg, 2) for species, avg in rows}

    @staticmethod
    def _row_to_record(row: tuple) -> MeasurementRecord:
        return MeasurementRecord(
            id=row[0], plant_id=row[1], species=row[2], height_cm=row[3],
            biomass_g=row[4], measurement_date=date.fromisoformat(row[5]),
        )


def run() -> dict[str, float]:
    """Runs the SQL management system against a controlled in-memory database."""
    database = Database(":memory:")
    repository = MeasurementRepository(database)

    try:
        sample_records = [
            MeasurementRecord(None, "P001", "Zea mays", 45.2, 12.8, date(2024, 5, 1)),
            MeasurementRecord(None, "P002", "Zea mays", 47.9, 13.5, date(2024, 5, 1)),
            MeasurementRecord(None, "P003", "Glycine max", 30.1, 9.2, date(2024, 5, 1)),
        ]
        for record in sample_records:
            created = repository.create(record)
            logger.info("Created measurement id=%d for %s", created.id, created.plant_id)

        repository.update_measurements(1, height_cm=46.0, biomass_g=13.0)
        logger.info("Updated measurement id=1")

        maize_records = repository.list_by_species("Zea mays")
        logger.info("Zea mays records: %d", len(maize_records))

        averages = repository.average_biomass_by_species()
        logger.info("Average biomass by species: %s", averages)

        return averages
    finally:
        database.close()


if __name__ == "__main__":
    run()
