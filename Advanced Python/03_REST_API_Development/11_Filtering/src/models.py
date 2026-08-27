from __future__ import annotations

import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum as SAEnum, Float, ForeignKey, Index, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class AssayType(str, enum.Enum):
    BINDING = "binding"
    FUNCTIONAL = "functional"
    ADMET = "admet"
    CYTOTOXICITY = "cytotoxicity"


class ScreeningRunStatus(str, enum.Enum):
    QUEUED = "queued"
    RUNNING = "running"
    VALIDATED = "validated"
    FAILED = "failed"


class ScreeningRun(Base):
    __tablename__ = "screening_runs"
    __table_args__ = (
        Index("ix_screening_runs_status_created_at", "status", "created_at"),
        Index("ix_screening_runs_assay_type", "assay_type"),
    )

    run_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    compound_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("compounds.compound_id"), nullable=False)
    assay_type: Mapped[AssayType] = mapped_column(SAEnum(AssayType, name="assay_type_enum"), nullable=False)
    status: Mapped[ScreeningRunStatus] = mapped_column(
        SAEnum(ScreeningRunStatus, name="screening_run_status_enum"), nullable=False, default=ScreeningRunStatus.QUEUED
    )
    score: Mapped[float | None] = mapped_column(Float, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
