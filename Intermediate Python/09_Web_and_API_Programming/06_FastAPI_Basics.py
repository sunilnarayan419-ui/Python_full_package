"""
06_FastAPI_Basics.py

A self-contained FastAPI backend for a scientific sample/experiment
tracking service, organized in layers:

    Router (HTTP concerns)
        -> Service (business rules)
            -> Repository (persistence, in-memory here)

Run with:
    uvicorn 06_FastAPI_Basics:app --reload

No database server is required; an in-memory repository is used so this
file is runnable in isolation.
"""

from __future__ import annotations

import logging
from datetime import datetime, UTC
from typing import Protocol

from fastapi import Depends, FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Domain models
# ---------------------------------------------------------------------------

class Sample(BaseModel):
    id: str
    species: str
    tissue: str
    collected_at: datetime


class Experiment(BaseModel):
    id: str
    title: str
    sample_id: str
    created_at: datetime


# ---------------------------------------------------------------------------
# API schemas (deliberately separate from domain models where it matters)
# ---------------------------------------------------------------------------

class SampleCreate(BaseModel):
    id: str = Field(min_length=1, max_length=32)
    species: str = Field(min_length=1, max_length=128)
    tissue: str = Field(min_length=1, max_length=64)


class SampleResponse(BaseModel):
    id: str
    species: str
    tissue: str
    collected_at: datetime


class ExperimentCreate(BaseModel):
    id: str = Field(min_length=1, max_length=32)
    title: str = Field(min_length=1, max_length=256)
    sample_id: str = Field(min_length=1, max_length=32)


class ExperimentResponse(BaseModel):
    id: str
    title: str
    sample_id: str
    created_at: datetime


# ---------------------------------------------------------------------------
# Domain errors
# ---------------------------------------------------------------------------

class SampleNotFoundError(LookupError):
    """Raised when a sample cannot be found."""


class DuplicateSampleError(ValueError):
    """Raised when a sample with the same id already exists."""


class DuplicateExperimentError(ValueError):
    """Raised when an experiment with the same id already exists."""


# ---------------------------------------------------------------------------
# Repository layer
# ---------------------------------------------------------------------------

class SampleRepository(Protocol):
    def get(self, sample_id: str) -> Sample: ...
    def create(self, sample: Sample) -> Sample: ...
    def list(self, *, limit: int, offset: int) -> list[Sample]: ...
    def exists(self, sample_id: str) -> bool: ...


class ExperimentRepository(Protocol):
    def create(self, experiment: Experiment) -> Experiment: ...
    def list(self, *, limit: int, offset: int) -> list[Experiment]: ...
    def exists(self, experiment_id: str) -> bool: ...


class InMemorySampleRepository:
    def __init__(self) -> None:
        self._store: dict[str, Sample] = {}

    def get(self, sample_id: str) -> Sample:
        sample = self._store.get(sample_id)
        if sample is None:
            raise SampleNotFoundError(sample_id)
        return sample

    def create(self, sample: Sample) -> Sample:
        if sample.id in self._store:
            raise DuplicateSampleError(sample.id)
        self._store[sample.id] = sample
        return sample

    def list(self, *, limit: int, offset: int) -> list[Sample]:
        items = sorted(self._store.values(), key=lambda s: s.collected_at, reverse=True)
        return items[offset : offset + limit]

    def exists(self, sample_id: str) -> bool:
        return sample_id in self._store


class InMemoryExperimentRepository:
    def __init__(self) -> None:
        self._store: dict[str, Experiment] = {}

    def create(self, experiment: Experiment) -> Experiment:
        if experiment.id in self._store:
            raise DuplicateExperimentError(experiment.id)
        self._store[experiment.id] = experiment
        return experiment

    def list(self, *, limit: int, offset: int) -> list[Experiment]:
        items = sorted(self._store.values(), key=lambda e: e.created_at, reverse=True)
        return items[offset : offset + limit]

    def exists(self, experiment_id: str) -> bool:
        return experiment_id in self._store


# ---------------------------------------------------------------------------
# Service layer
# ---------------------------------------------------------------------------

class SampleService:
    def __init__(self, repo: SampleRepository) -> None:
        self._repo = repo

    def get_sample(self, sample_id: str) -> Sample:
        return self._repo.get(sample_id)

    def list_samples(self, *, limit: int, offset: int) -> list[Sample]:
        return self._repo.list(limit=limit, offset=offset)

    def create_sample(self, payload: SampleCreate) -> Sample:
        sample = Sample(
            id=payload.id,
            species=payload.species,
            tissue=payload.tissue,
            collected_at=datetime.now(UTC),
        )
        return self._repo.create(sample)


class ExperimentService:
    def __init__(self, experiments: ExperimentRepository, samples: SampleRepository) -> None:
        self._experiments = experiments
        self._samples = samples

    def list_experiments(self, *, limit: int, offset: int) -> list[Experiment]:
        return self._experiments.list(limit=limit, offset=offset)

    def create_experiment(self, payload: ExperimentCreate) -> Experiment:
        if not self._samples.exists(payload.sample_id):
            raise SampleNotFoundError(payload.sample_id)
        experiment = Experiment(
            id=payload.id,
            title=payload.title,
            sample_id=payload.sample_id,
            created_at=datetime.now(UTC),
        )
        return self._experiments.create(experiment)


# ---------------------------------------------------------------------------
# Dependency injection wiring
# ---------------------------------------------------------------------------

_sample_repo = InMemorySampleRepository()
_experiment_repo = InMemoryExperimentRepository()


def get_sample_repository() -> SampleRepository:
    return _sample_repo


def get_experiment_repository() -> ExperimentRepository:
    return _experiment_repo


def get_sample_service(
    repo: SampleRepository = Depends(get_sample_repository),
) -> SampleService:
    return SampleService(repo)


def get_experiment_service(
    experiments: ExperimentRepository = Depends(get_experiment_repository),
    samples: SampleRepository = Depends(get_sample_repository),
) -> ExperimentService:
    return ExperimentService(experiments, samples)


# ---------------------------------------------------------------------------
# Application & routes
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Scientific Sample Tracking API",
    version="1.0.0",
    description="Backend service for tracking laboratory samples and experiments.",
)


@app.get("/health", tags=["ops"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/samples/{sample_id}", response_model=SampleResponse, tags=["samples"])
def get_sample(
    sample_id: str,
    service: SampleService = Depends(get_sample_service),
) -> Sample:
    try:
        return service.get_sample(sample_id)
    except SampleNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="sample not found")


@app.get("/samples", response_model=list[SampleResponse], tags=["samples"])
def list_samples(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: SampleService = Depends(get_sample_service),
) -> list[Sample]:
    return service.list_samples(limit=limit, offset=offset)


@app.post(
    "/samples",
    response_model=SampleResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["samples"],
)
def create_sample(
    payload: SampleCreate,
    service: SampleService = Depends(get_sample_service),
) -> Sample:
    try:
        return service.create_sample(payload)
    except DuplicateSampleError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"sample '{payload.id}' already exists",
        )


@app.get("/experiments", response_model=list[ExperimentResponse], tags=["experiments"])
def list_experiments(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    service: ExperimentService = Depends(get_experiment_service),
) -> list[Experiment]:
    return service.list_experiments(limit=limit, offset=offset)


@app.post(
    "/experiments",
    response_model=ExperimentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["experiments"],
)
def create_experiment(
    payload: ExperimentCreate,
    service: ExperimentService = Depends(get_experiment_service),
) -> Experiment:
    try:
        return service.create_experiment(payload)
    except SampleNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"sample '{payload.sample_id}' does not exist",
        )
    except DuplicateExperimentError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"experiment '{payload.id}' already exists",
        )
