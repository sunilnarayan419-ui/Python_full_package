from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Experiment(Base):
    __tablename__ = "experiments"

    experiment_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(256))

    analysis_jobs: Mapped[list["AnalysisJob"]] = relationship(back_populates="experiment")


class AnalysisJob(Base):
    __tablename__ = "analysis_jobs"

    analysis_job_id: Mapped[int] = mapped_column(primary_key=True)
    experiment_id: Mapped[int] = mapped_column(ForeignKey("experiments.experiment_id"))

    experiment: Mapped[Experiment] = relationship(back_populates="analysis_jobs")
