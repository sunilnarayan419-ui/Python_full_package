from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from ..domain.entities import AssayType, ScreeningRunStatus


class ScreeningRunCreateRequest(BaseModel):
    compound_id: UUID
    assay_type: AssayType


class ScreeningRunTransitionRequest(BaseModel):
    target_status: ScreeningRunStatus
    score: float | None = Field(default=None, ge=0.0, le=1.0)


class ScreeningRunResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    run_id: UUID
    compound_id: UUID
    assay_type: AssayType
    status: ScreeningRunStatus
    score: float | None
    created_at: datetime
    updated_at: datetime


class PageMeta(BaseModel):
    limit: int
    offset: int
    count: int


class ScreeningRunPage(BaseModel):
    items: list[ScreeningRunResponse]
    meta: PageMeta


class ErrorDetail(BaseModel):
    code: str
    message: str
    request_id: str


class ErrorResponse(BaseModel):
    error: ErrorDetail
