"""
04_ORM.py

Focused demonstration of Object-Relational Mapping concepts: how Python
objects and their relationships map onto relational tables, why that
mapping is useful, and where it is *not* a substitute for understanding
SQL.

Domain: Gene -> Protein (one-to-many: a gene may encode multiple protein
isoforms) and MolecularTarget <- Compound interactions represented via an
association table, since that relationship is naturally many-to-many.
"""

from __future__ import annotations

import logging

from sqlalchemy import ForeignKey, Table, Column, String, create_engine, select, text
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, selectinload

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    pass


class Gene(Base):
    __tablename__ = "genes"

    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(String(40), unique=True)

    # One-to-many: one gene -> many protein isoforms.
    proteins: Mapped[list["Protein"]] = relationship(back_populates="gene")


class Protein(Base):
    __tablename__ = "proteins"

    id: Mapped[int] = mapped_column(primary_key=True)
    gene_id: Mapped[int] = mapped_column(ForeignKey("genes.id"))
    uniprot_accession: Mapped[str] = mapped_column(String(20), unique=True)

    # Many-to-one: many protein isoforms -> one gene.
    gene: Mapped["Gene"] = relationship(back_populates="proteins")

    targets: Mapped[list["MolecularTarget"]] = relationship(
        secondary="protein_targets", back_populates="proteins"
    )


class MolecularTarget(Base):
    __tablename__ = "molecular_targets"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))

    proteins: Mapped[list["Protein"]] = relationship(
        secondary="protein_targets", back_populates="targets"
    )
    compounds: Mapped[list["Compound"]] = relationship(
        secondary="target_compounds", back_populates="targets"
    )


class Compound(Base):
    __tablename__ = "compounds"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))

    targets: Mapped[list["MolecularTarget"]] = relationship(
        secondary="target_compounds", back_populates="compounds"
    )


# Pure association tables (no meaningful attributes of their own) are
# modeled as plain Table objects rather than full entity classes -- this
# keeps the ORM layer proportional to the actual domain complexity.
protein_targets = Table(
    "protein_targets",
    Base.metadata,
    Column("protein_id", ForeignKey("proteins.id"), primary_key=True),
    Column("target_id", ForeignKey("molecular_targets.id"), primary_key=True),
)

target_compounds = Table(
    "target_compounds",
    Base.metadata,
    Column("target_id", ForeignKey("molecular_targets.id"), primary_key=True),
    Column("compound_id", ForeignKey("compounds.id"), primary_key=True),
)


def _seed(session: Session) -> Gene:
    gene = Gene(symbol="EGFR")
    protein = Protein(uniprot_accession="P00533", gene=gene)
    target = MolecularTarget(name="EGFR kinase domain")
    compound = Compound(name="Erlotinib")
    protein.targets.append(target)
    target.compounds.append(compound)
    session.add(gene)
    session.flush()
    return gene


def demo_orm_navigation(session: Session, gene_id: int) -> None:
    """
    Shows the core value of ORM: once objects are loaded, relationships
    are navigated as plain Python attributes instead of hand-written
    JOINs. `selectinload` is used deliberately here to avoid the N+1
    query problem that naive lazy-loading would cause when iterating
    over many genes and their proteins.
    """
    stmt = (
        select(Gene)
        .where(Gene.id == gene_id)
        .options(selectinload(Gene.proteins).selectinload(Protein.targets))
    )
    gene = session.scalars(stmt).one()
    for protein in gene.proteins:
        target_names = [t.name for t in protein.targets]
        print(f"gene={gene.symbol} protein={protein.uniprot_accession} targets={target_names}")


def demo_raw_sql_still_useful(session: Session) -> None:
    """
    ORM mapping does not remove the need to understand SQL. Aggregate
    reporting queries, bulk analytics, and database-specific features are
    often clearer and more efficient expressed directly, using the same
    parameterized, injection-safe execution path as the ORM.
    """
    result = session.execute(
        text("SELECT COUNT(*) AS protein_count FROM proteins WHERE gene_id = :gene_id"),
        {"gene_id": 1},
    ).one()
    print(f"raw SQL aggregate: protein_count={result.protein_count}")


def _run_demo() -> None:
    logging.basicConfig(level=logging.INFO)
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)

    try:
        with Session(engine) as session:
            with session.begin():
                gene = _seed(session)
            demo_orm_navigation(session, gene.id)
            demo_raw_sql_still_useful(session)
    finally:
        engine.dispose()


if __name__ == "__main__":
    _run_demo()
