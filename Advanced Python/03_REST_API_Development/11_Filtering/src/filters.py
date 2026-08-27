from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field, model_validator
from sqlalchemy import ColumnElement, and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import AssayType, ScreeningRun, ScreeningRunStatus

router = APIRouter(prefix="/api/v1", tags=["screening-runs"])

_SORTABLE_FIELDS = {"created_at", "score"}


class ScreeningRunFilterParams(BaseModel):
    status: ScreeningRunStatus | None = None
    assay_type: AssayType | None = None
    created_after: datetime | None = None
    created_before: datetime | None = None
    score_gte: float | None = Field(default=None, ge=0.0, le=1.0)
    score_lte: float | None = Field(default=None, ge=0.0, le=1.0)
    search: str | None = Field(default=None, max_length=255)
    sort: str = Field(default="-created_at")

    @model_validator(mode="after")
    def validate_sort_field(self) -> "ScreeningRunFilterParams":
        field_name = self.sort.lstrip("-")
        if field_name not in _SORTABLE_FIELDS:
            raise ValueError(f"Cannot sort by '{field_name}'. Allowed fields: {sorted(_SORTABLE_FIELDS)}.")
        return self

    @model_validator(mode="after")
    def validate_ranges(self) -> "ScreeningRunFilterParams":
        if self.score_gte is not None and self.score_lte is not None and self.score_gte > self.score_lte:
            raise ValueError("score_gte cannot be greater than score_lte.")
        if self.created_after is not None and self.created_before is not None and self.created_after > self.created_before:
            raise ValueError("created_after cannot be later than created_before.")
        return self


def build_filter_conditions(params: ScreeningRunFilterParams) -> list[ColumnElement[bool]]:
    conditions: list[ColumnElement[bool]] = []

    if params.status is not None:
        conditions.append(ScreeningRun.status == params.status)
    if params.assay_type is not None:
        conditions.append(ScreeningRun.assay_type == params.assay_type)
    if params.created_after is not None:
        conditions.append(ScreeningRun.created_at >= params.created_after)
    if params.created_before is not None:
        conditions.append(ScreeningRun.created_at <= params.created_before)
    if params.score_gte is not None:
        conditions.append(ScreeningRun.score >= params.score_gte)
    if params.score_lte is not None:
        conditions.append(ScreeningRun.score <= params.score_lte)
    if params.search:
        conditions.append(ScreeningRun.notes.ilike(f"%{params.search}%"))

    return conditions


def build_order_clause(sort: str) -> ColumnElement[object]:
    descending = sort.startswith("-")
    field_name = sort.lstrip("-")
    column = getattr(ScreeningRun, field_name)
    return column.desc() if descending else column.asc()


async def get_db_session() -> AsyncSession:  # pragma: no cover - wired at app startup
    raise NotImplementedError("Overridden by dependency_overrides in application startup.")


@router.get("/screening-runs")
async def search_screening_runs(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    params: Annotated[ScreeningRunFilterParams, Depends()],
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[dict[str, object]]:
    conditions = build_filter_conditions(params)
    stmt = select(ScreeningRun)
    if conditions:
        stmt = stmt.where(and_(*conditions))
    stmt = stmt.order_by(build_order_clause(params.sort)).limit(limit).offset(offset)

    result = await session.execute(stmt)
    return [
        {
            "run_id": str(row.run_id),
            "status": row.status,
            "assay_type": row.assay_type,
            "score": row.score,
            "created_at": row.created_at.isoformat(),
        }
        for row in result.scalars().all()
    ]
