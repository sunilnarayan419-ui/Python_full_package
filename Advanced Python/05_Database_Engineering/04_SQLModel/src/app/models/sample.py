from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel


class Sample(SQLModel, table=True):
    __tablename__ = "samples"

    sample_id: UUID = Field(default_factory=uuid4, primary_key=True)
    subject_code: str = Field(index=True, max_length=64)
    status: str = Field(default="collected", max_length=16)
    collected_at: datetime

    analysis_jobs: list["AnalysisJob"] = Relationship(back_populates="sample")


class AnalysisJob(SQLModel, table=True):
    __tablename__ = "analysis_jobs"

    analysis_job_id: int | None = Field(default=None, primary_key=True)
    sample_id: UUID = Field(foreign_key="samples.sample_id")
    pipeline_name: str = Field(max_length=128)
    status: str = Field(default="queued", max_length=16)
    submitted_at: datetime = Field(default_factory=datetime.utcnow)

    sample: Sample = Relationship(back_populates="analysis_jobs")
