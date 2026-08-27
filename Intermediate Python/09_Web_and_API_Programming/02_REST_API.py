"""
02_REST_API.py

Resource-oriented REST API design for a scientific data platform, expressed
as a framework-agnostic in-process API layer (no web server required to run
this file). The same request/response contracts shown here are what a real
FastAPI or Flask layer would sit in front of.

Resources:
    /api/v1/samples
    /api/v1/experiments
    /api/v1/measurements

Design choices demonstrated:
    - resource-oriented URLs, not RPC-style verbs in the path
    - pagination via limit/offset with bounds enforcement
    - filtering and sorting on list endpoints
    - consistent, minimal response envelopes (no forced success/data wrapper)
    - explicit API versioning under /api/v1
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Any, Literal

logger = logging.getLogger(__name__)

API_PREFIX = "/api/v1"

MAX_PAGE_SIZE = 100
DEFAULT_PAGE_SIZE = 20


class SampleNotFoundError(LookupError):
    """Raised when a sample resource cannot be found."""


class DuplicateSampleError(ValueError):
    """Raised when a sample with the same accession already exists."""


class InvalidQueryError(ValueError):
    """Raised when query parameters are malformed or out of bounds."""


@dataclass(slots=True)
class Sample:
    id: str
    species: str
    tissue: str
    collected_at: datetime
    project_id: str


@dataclass(slots=True)
class PageResult:
    items: list[Any]
    total: int
    limit: int
    offset: int

    def to_dict(self, key: str) -> dict[str, Any]:
        return {
            key: self.items,
            "pagination": {
                "total": self.total,
                "limit": self.limit,
                "offset": self.offset,
                "has_more": self.offset + len(self.items) < self.total,
            },
        }


class SampleRepository:
    """In-memory repository standing in for a database-backed one. Real
    implementations would issue SQL/ORM queries with equivalent semantics."""

    def __init__(self) -> None:
        self._samples: dict[str, Sample] = {}

    def seed(self, samples: list[Sample]) -> None:
        for s in samples:
            self._samples[s.id] = s

    def get(self, sample_id: str) -> Sample:
        sample = self._samples.get(sample_id)
        if sample is None:
            raise SampleNotFoundError(sample_id)
        return sample

    def create(self, sample: Sample) -> Sample:
        if sample.id in self._samples:
            raise DuplicateSampleError(sample.id)
        self._samples[sample.id] = sample
        return sample

    def delete(self, sample_id: str) -> None:
        self._samples.pop(sample_id, None)

    def list(
        self,
        *,
        species: str | None = None,
        project_id: str | None = None,
        sort_by: Literal["collected_at", "id"] = "collected_at",
        descending: bool = True,
        limit: int = DEFAULT_PAGE_SIZE,
        offset: int = 0,
    ) -> PageResult:
        results = list(self._samples.values())

        if species is not None:
            results = [s for s in results if s.species == species]
        if project_id is not None:
            results = [s for s in results if s.project_id == project_id]

        results.sort(key=lambda s: getattr(s, sort_by), reverse=descending)

        total = len(results)
        page = results[offset : offset + limit]
        return PageResult(items=page, total=total, limit=limit, offset=offset)


def _validate_pagination(limit: int, offset: int) -> tuple[int, int]:
    """Enforce sane pagination bounds so clients cannot request unbounded
    scientific datasets in a single call."""
    if offset < 0:
        raise InvalidQueryError("offset must be >= 0")
    if limit <= 0:
        raise InvalidQueryError("limit must be > 0")
    if limit > MAX_PAGE_SIZE:
        raise InvalidQueryError(f"limit must be <= {MAX_PAGE_SIZE}")
    return limit, offset


def _sample_to_response(sample: Sample) -> dict[str, Any]:
    """API response shape, intentionally decoupled from the domain model
    field-for-field so internal fields are never accidentally exposed."""
    return {
        "id": sample.id,
        "species": sample.species,
        "tissue": sample.tissue,
        "collected_at": sample.collected_at.isoformat(),
        "project_id": sample.project_id,
        "self": f"{API_PREFIX}/samples/{sample.id}",
    }


@dataclass(slots=True)
class ApiResult:
    status_code: int
    body: dict[str, Any] | None
    headers: dict[str, str] = field(default_factory=dict)


class SampleResource:
    """Route handlers for the /api/v1/samples resource. In a real service
    these would be bound to FastAPI/Flask routes; the signatures here map
    1:1 onto that binding."""

    def __init__(self, repo: SampleRepository) -> None:
        self._repo = repo

    def list_samples(
        self,
        *,
        species: str | None = None,
        project_id: str | None = None,
        sort_by: str = "collected_at",
        order: str = "desc",
        limit: int = DEFAULT_PAGE_SIZE,
        offset: int = 0,
    ) -> ApiResult:
        # GET /api/v1/samples?species=...&project_id=...&sort=...&limit=...&offset=...
        try:
            limit, offset = _validate_pagination(limit, offset)
            if sort_by not in {"collected_at", "id"}:
                raise InvalidQueryError("sort_by must be one of: collected_at, id")
            if order not in {"asc", "desc"}:
                raise InvalidQueryError("order must be one of: asc, desc")
        except InvalidQueryError as exc:
            return ApiResult(status_code=422, body={"error": "invalid_query", "detail": str(exc)})

        page = self._repo.list(
            species=species,
            project_id=project_id,
            sort_by=sort_by,  # type: ignore[arg-type]
            descending=(order == "desc"),
            limit=limit,
            offset=offset,
        )
        body = page.to_dict("samples")
        body["samples"] = [_sample_to_response(s) for s in page.items]
        return ApiResult(status_code=200, body=body)

    def get_sample(self, sample_id: str) -> ApiResult:
        # GET /api/v1/samples/{sample_id}
        try:
            sample = self._repo.get(sample_id)
        except SampleNotFoundError:
            return ApiResult(status_code=404, body={"error": "sample_not_found", "id": sample_id})
        return ApiResult(status_code=200, body=_sample_to_response(sample))

    def create_sample(self, payload: dict[str, Any]) -> ApiResult:
        # POST /api/v1/samples
        required = {"id", "species", "tissue", "project_id"}
        missing = required - payload.keys()
        if missing:
            return ApiResult(
                status_code=422,
                body={"error": "validation_error", "missing_fields": sorted(missing)},
            )

        sample = Sample(
            id=str(payload["id"]),
            species=str(payload["species"]),
            tissue=str(payload["tissue"]),
            project_id=str(payload["project_id"]),
            collected_at=datetime.now(UTC),
        )
        try:
            self._repo.create(sample)
        except DuplicateSampleError:
            return ApiResult(
                status_code=409,
                body={"error": "sample_already_exists", "id": sample.id},
            )

        logger.info("sample created id=%s", sample.id)
        return ApiResult(
            status_code=201,
            headers={"Location": f"{API_PREFIX}/samples/{sample.id}"},
            body=_sample_to_response(sample),
        )

    def delete_sample(self, sample_id: str) -> ApiResult:
        # DELETE /api/v1/samples/{sample_id} -- idempotent
        try:
            self._repo.get(sample_id)
        except SampleNotFoundError:
            return ApiResult(status_code=404, body={"error": "sample_not_found", "id": sample_id})
        self._repo.delete(sample_id)
        return ApiResult(status_code=204, body=None)


def _demo() -> None:
    logging.basicConfig(level=logging.INFO)

    repo = SampleRepository()
    repo.seed(
        [
            Sample("SMP-001", "Arabidopsis thaliana", "leaf", datetime.now(UTC), "PRJ-1"),
            Sample("SMP-002", "Oryza sativa", "root", datetime.now(UTC), "PRJ-1"),
        ]
    )
    resource = SampleResource(repo)

    listed = resource.list_samples(limit=10, offset=0)
    assert listed.status_code == 200
    assert listed.body is not None
    assert len(listed.body["samples"]) == 2

    too_big = resource.list_samples(limit=10_000)
    assert too_big.status_code == 422

    created = resource.create_sample(
        {"id": "SMP-003", "species": "Zea mays", "tissue": "kernel", "project_id": "PRJ-2"}
    )
    assert created.status_code == 201

    dup = resource.create_sample(
        {"id": "SMP-003", "species": "Zea mays", "tissue": "kernel", "project_id": "PRJ-2"}
    )
    assert dup.status_code == 409

    not_found = resource.get_sample("SMP-999")
    assert not_found.status_code == 404

    logger.info("REST API resource demo completed successfully")


if __name__ == "__main__":
    _demo()
