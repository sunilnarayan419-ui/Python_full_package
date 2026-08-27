from __future__ import annotations

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

# Many-to-many association table: researchers <-> research_projects
project_researchers = Table(
    "project_researchers",
    Base.metadata,
    Column("project_id", ForeignKey("research_projects.project_id"), primary_key=True),
    Column("researcher_id", ForeignKey("researchers.researcher_id"), primary_key=True),
    Column("role", String(32), nullable=False, server_default="contributor"),
)


class Researcher(Base):
    __tablename__ = "researchers"

    researcher_id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(256))

    projects: Mapped[list["ResearchProject"]] = relationship(
        secondary=project_researchers, back_populates="researchers", lazy="selectin"
    )


class ResearchProject(Base):
    __tablename__ = "research_projects"

    project_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(256))

    researchers: Mapped[list[Researcher]] = relationship(
        secondary=project_researchers, back_populates="projects", lazy="selectin"
    )

    # One-to-many with explicit orphan cleanup: deleting a project deletes its notebooks,
    # but a notebook is never silently reassigned without going through the domain layer.
    notebooks: Mapped[list["LabNotebook"]] = relationship(
        back_populates="project", cascade="all, delete-orphan", lazy="selectin"
    )


class LabNotebook(Base):
    __tablename__ = "lab_notebooks"

    notebook_id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("research_projects.project_id"))
    title: Mapped[str] = mapped_column(String(256))

    project: Mapped[ResearchProject] = relationship(back_populates="notebooks")

    # Composite child collection deliberately kept lazy='raise' — the domain layer must
    # ask for entries explicitly (paginated) rather than ever loading an unbounded set.
    entries: Mapped[list["NotebookEntry"]] = relationship(back_populates="notebook", lazy="raise")


class NotebookEntry(Base):
    __tablename__ = "notebook_entries"

    entry_id: Mapped[int] = mapped_column(primary_key=True)
    notebook_id: Mapped[int] = mapped_column(ForeignKey("lab_notebooks.notebook_id"))
    body: Mapped[str] = mapped_column(String(4000))

    notebook: Mapped[LabNotebook] = relationship(back_populates="entries")
