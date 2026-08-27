from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class ResearchProject(TimestampMixin, Base):
    __tablename__ = "research_projects"

    project_id: Mapped[int] = mapped_column(primary_key=True)
    project_code: Mapped[str] = mapped_column(String(32), unique=True)
    title: Mapped[str] = mapped_column(String(256))
    status: Mapped[str] = mapped_column(String(16))
    started_at: Mapped[date]

    compounds: Mapped[list["Compound"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('planning','active','on_hold','completed','cancelled')",
            name="chk_project_status",
        ),
    )


class Compound(TimestampMixin, Base):
    __tablename__ = "compounds"

    compound_id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("research_projects.project_id"))
    inchi_key: Mapped[str] = mapped_column(String(27), unique=True)
    molecular_weight: Mapped[Decimal] = mapped_column(Numeric(10, 4))

    project: Mapped[ResearchProject] = relationship(back_populates="compounds")
    screening_results: Mapped[list["ScreeningResult"]] = relationship(
        back_populates="compound", lazy="raise"
    )


class ScreeningResult(Base):
    __tablename__ = "screening_results"

    screening_result_id: Mapped[int] = mapped_column(primary_key=True)
    compound_id: Mapped[int] = mapped_column(ForeignKey("compounds.compound_id"))
    screening_run_id: Mapped[int] = mapped_column(ForeignKey("screening_runs.screening_run_id"))
    potency_nm: Mapped[Decimal | None] = mapped_column(Numeric(12, 4))
    is_hit: Mapped[bool] = mapped_column(default=False)

    compound: Mapped[Compound] = relationship(back_populates="screening_results")

    __table_args__ = (
        UniqueConstraint("screening_run_id", "compound_id", name="uq_result_run_compound"),
    )
