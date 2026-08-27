from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SampleCreateRequest(BaseModel):
    """API input schema - deliberately decoupled from the persistence model."""

    subject_code: str = Field(min_length=1, max_length=64)
    collected_at: datetime


class SampleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sample_id: UUID
    subject_code: str
    status: str
    collected_at: datetime


class AnalysisJobCreateRequest(BaseModel):
    sample_id: UUID
    pipeline_name: str = Field(min_length=1, max_length=128)


class AnalysisJobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    analysis_job_id: int
    sample_id: UUID
    pipeline_name: str
    status: str
    submitted_at: datetime
