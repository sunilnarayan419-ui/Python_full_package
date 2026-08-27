from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator

DB_PATH = Path(":memory:")


class SampleCreateRequest(BaseModel):
    """Request payload for creating a laboratory sample."""

    species: str = Field(min_length=1, max_length=100)
    treatment: str = Field(min_length=1, max_length=100)
    collected_by: str = Field(min_length=1, max_length=100)
    weight_g: float = Field(gt=0.0, le=10_000.0)

    @field_validator("species", "treatment", "collected_by")
    @classmethod
    def strip_whitespace(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("Field cannot be blank.")
        return stripped


class SampleUpdateRequest(BaseModel):
    """Request payload for updating an existing laboratory sample."""

    species: str | None = Field(default=None, min_length=1, max_length=100)
    treatment: str | None = Field(default=None, min_length=1, max_length=100)
    weight_g: float | None = Field(default=None, gt=0.0, le=10_000.0)


class SampleResponse(BaseModel):
    """Response payload representing a laboratory sample."""

    id: int
    species: str
    treatment: str
    collected_by: str
    weight_g: float
    created_at: str


class HealthResponse(BaseModel):
    status: str
    timestamp: str


class SampleNotFoundError(Exception):
    """Raised when a requested sample id does not exist."""


class SampleRepository:
    """SQLite-backed repository for laboratory samples."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection
        self._initialize_schema()

    def _initialize_schema(self) -> None:
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS samples (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                species TEXT NOT NULL,
                treatment TEXT NOT NULL,
                collected_by TEXT NOT NULL,
                weight_g REAL NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        self._connection.commit()

    def create(self, payload: SampleCreateRequest) -> SampleResponse:
        created_at = datetime.now(timezone.utc).isoformat()
        cursor = self._connection.execute(
            """
            INSERT INTO samples (species, treatment, collected_by, weight_g, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (payload.species, payload.treatment, payload.collected_by, payload.weight_g, created_at),
        )
        self._connection.commit()
        return self.get(cursor.lastrowid)

    def get(self, sample_id: int) -> SampleResponse:
        row = self._connection.execute(
            "SELECT id, species, treatment, collected_by, weight_g, created_at FROM samples WHERE id = ?",
            (sample_id,),
        ).fetchone()
        if row is None:
            raise SampleNotFoundError(f"Sample {sample_id} not found.")
        return SampleResponse(
            id=row[0], species=row[1], treatment=row[2], collected_by=row[3],
            weight_g=row[4], created_at=row[5],
        )

    def list_all(self) -> list[SampleResponse]:
        rows = self._connection.execute(
            "SELECT id, species, treatment, collected_by, weight_g, created_at FROM samples ORDER BY id"
        ).fetchall()
        return [
            SampleResponse(
                id=r[0], species=r[1], treatment=r[2], collected_by=r[3], weight_g=r[4], created_at=r[5]
            )
            for r in rows
        ]

    def update(self, sample_id: int, payload: SampleUpdateRequest) -> SampleResponse:
        existing = self.get(sample_id)
        species = payload.species if payload.species is not None else existing.species
        treatment = payload.treatment if payload.treatment is not None else existing.treatment
        weight_g = payload.weight_g if payload.weight_g is not None else existing.weight_g

        self._connection.execute(
            "UPDATE samples SET species = ?, treatment = ?, weight_g = ? WHERE id = ?",
            (species, treatment, weight_g, sample_id),
        )
        self._connection.commit()
        return self.get(sample_id)

    def delete(self, sample_id: int) -> None:
        self.get(sample_id)
        self._connection.execute("DELETE FROM samples WHERE id = ?", (sample_id,))
        self._connection.commit()


class SampleService:
    """Business-logic layer coordinating repository operations."""

    def __init__(self, repository: SampleRepository) -> None:
        self._repository = repository

    def create_sample(self, payload: SampleCreateRequest) -> SampleResponse:
        return self._repository.create(payload)

    def get_sample(self, sample_id: int) -> SampleResponse:
        return self._repository.get(sample_id)

    def list_samples(self) -> list[SampleResponse]:
        return self._repository.list_all()

    def update_sample(self, sample_id: int, payload: SampleUpdateRequest) -> SampleResponse:
        return self._repository.update(sample_id, payload)

    def delete_sample(self, sample_id: int) -> None:
        self._repository.delete(sample_id)


_connection = sqlite3.connect(":memory:", check_same_thread=False)
_repository = SampleRepository(_connection)
_service = SampleService(_repository)


def get_sample_service() -> SampleService:
    """Dependency provider for the sample service."""
    return _service


app = FastAPI(title="Laboratory Sample Registry", version="1.0.0")


@app.get("/health", response_model=HealthResponse, tags=["system"])
def health_check() -> HealthResponse:
    return HealthResponse(status="ok", timestamp=datetime.now(timezone.utc).isoformat())


@app.get("/items", response_model=list[SampleResponse], tags=["samples"])
def list_items(service: SampleService = Depends(get_sample_service)) -> list[SampleResponse]:
    return service.list_samples()


@app.get("/items/{item_id}", response_model=SampleResponse, tags=["samples"])
def get_item(item_id: int, service: SampleService = Depends(get_sample_service)) -> SampleResponse:
    try:
        return service.get_sample(item_id)
    except SampleNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@app.post("/items", response_model=SampleResponse, status_code=status.HTTP_201_CREATED, tags=["samples"])
def create_item(
    payload: SampleCreateRequest, service: SampleService = Depends(get_sample_service)
) -> SampleResponse:
    return service.create_sample(payload)


@app.put("/items/{item_id}", response_model=SampleResponse, tags=["samples"])
def update_item(
    item_id: int,
    payload: SampleUpdateRequest,
    service: SampleService = Depends(get_sample_service),
) -> SampleResponse:
    try:
        return service.update_sample(item_id, payload)
    except SampleNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["samples"])
def delete_item(item_id: int, service: SampleService = Depends(get_sample_service)) -> None:
    try:
        service.delete_sample(item_id)
    except SampleNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


def run() -> FastAPI:
    """Returns the configured FastAPI application.

    Start the server externally with:
        uvicorn 04_FastAPI_Backend:app --reload
    """
    return app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
