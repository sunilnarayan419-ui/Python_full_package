from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Organization(Base):
    __tablename__ = "organizations"

    organization_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256), unique=True)

    projects: Mapped[list["ResearchProject"]] = relationship(back_populates="organization")


class Researcher(Base):
    __tablename__ = "researchers"

    researcher_id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(256))
    email: Mapped[str] = mapped_column(String(320), unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)


class ResearchProject(Base):
    __tablename__ = "research_projects"

    project_id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.organization_id"))
    project_code: Mapped[str] = mapped_column(String(32), unique=True)
    title: Mapped[str] = mapped_column(String(256))
    owner_researcher_id: Mapped[int] = mapped_column(ForeignKey("researchers.researcher_id"))
    status: Mapped[str] = mapped_column(String(16))
    started_at: Mapped[date]
    ended_at: Mapped[date | None]
    deleted_at: Mapped[datetime | None]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    organization: Mapped[Organization] = relationship(back_populates="projects")
    experiments: Mapped[list["Experiment"]] = relationship(back_populates="project")
    compounds: Mapped[list["Compound"]] = relationship(back_populates="project")

    __table_args__ = (
        CheckConstraint(
            "status IN ('planning','active','on_hold','completed','cancelled')",
            name="chk_project_status",
        ),
    )


class Experiment(Base):
    __tablename__ = "experiments"

    experiment_id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("research_projects.project_id"))
    title: Mapped[str] = mapped_column(String(256))
    hypothesis: Mapped[str] = mapped_column(String(4000))
    started_at: Mapped[date]

    project: Mapped[ResearchProject] = relationship(back_populates="experiments")
    assays: Mapped[list["Assay"]] = relationship(back_populates="experiment")


class MolecularTarget(Base):
    __tablename__ = "molecular_targets"

    target_id: Mapped[int] = mapped_column(primary_key=True)
    gene_symbol: Mapped[str] = mapped_column(String(64))
    uniprot_accession: Mapped[str] = mapped_column(String(16), unique=True)
    target_class: Mapped[str] = mapped_column(String(64))


class Assay(Base):
    __tablename__ = "assays"

    assay_id: Mapped[int] = mapped_column(primary_key=True)
    experiment_id: Mapped[int] = mapped_column(ForeignKey("experiments.experiment_id"))
    target_id: Mapped[int] = mapped_column(ForeignKey("molecular_targets.target_id"))
    assay_name: Mapped[str] = mapped_column(String(256))
    assay_type: Mapped[str] = mapped_column(String(16))
    readout_unit: Mapped[str] = mapped_column(String(16))

    experiment: Mapped[Experiment] = relationship(back_populates="assays")

    __table_args__ = (
        CheckConstraint(
            "assay_type IN ('binding','functional','adme','toxicity')", name="chk_assay_type"
        ),
    )


class Compound(Base):
    __tablename__ = "compounds"

    compound_id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("research_projects.project_id"))
    parent_compound_id: Mapped[int | None] = mapped_column(ForeignKey("compounds.compound_id"))
    inchi_key: Mapped[str] = mapped_column(String(27), unique=True)
    molecular_weight: Mapped[Decimal] = mapped_column(Numeric(10, 4))
    synthesized_at: Mapped[date]

    project: Mapped[ResearchProject] = relationship(back_populates="compounds")


class ScreeningRun(Base):
    __tablename__ = "screening_runs"

    screening_run_id: Mapped[int] = mapped_column(primary_key=True)
    assay_id: Mapped[int] = mapped_column(ForeignKey("assays.assay_id"))
    operator_id: Mapped[int] = mapped_column(ForeignKey("researchers.researcher_id"))
    run_date: Mapped[date]
    plate_count: Mapped[int]


class ScreeningResult(Base):
    __tablename__ = "screening_results"

    screening_result_id: Mapped[int] = mapped_column(primary_key=True)
    screening_run_id: Mapped[int] = mapped_column(ForeignKey("screening_runs.screening_run_id"))
    compound_id: Mapped[int] = mapped_column(ForeignKey("compounds.compound_id"))
    potency_nm: Mapped[Decimal | None] = mapped_column(Numeric(12, 4))
    is_hit: Mapped[bool] = mapped_column(default=False)

    __table_args__ = (
        UniqueConstraint("screening_run_id", "compound_id", name="uq_result_run_compound"),
    )
