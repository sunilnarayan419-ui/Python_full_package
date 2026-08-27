from __future__ import annotations

from decimal import Decimal

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class AssayHitCountView(Base):
    """Read-only mapping onto mv_assay_hit_counts. Never insert/update/delete through
    this class -- the materialized view is refreshed exclusively via
    refresh_assay_hit_counts(), never through the ORM session."""

    __tablename__ = "mv_assay_hit_counts"
    __table_args__ = {"info": {"is_view": True}}

    assay_id: Mapped[int] = mapped_column(primary_key=True)
    assay_name: Mapped[str] = mapped_column(String(256))
    total_results: Mapped[int]
    hits: Mapped[int]


class ProjectHitSummaryView(Base):
    __tablename__ = "v_project_hit_summary"
    __table_args__ = {"info": {"is_view": True}}

    project_id: Mapped[int] = mapped_column(primary_key=True)
    project_code: Mapped[str] = mapped_column(String(32))
    total_results: Mapped[int]
    total_hits: Mapped[int]
