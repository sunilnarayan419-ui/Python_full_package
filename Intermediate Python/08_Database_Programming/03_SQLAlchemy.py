"""
03_SQLAlchemy.py

Modern SQLAlchemy 2.x usage for the scientific data platform: Engine,
declarative typed models, Session lifecycle, and select()/insert-via-ORM
patterns. Uses a file-less in-memory SQLite database for the runnable
demo so the example has no external dependencies, while the model layer
and query patterns are fully portable to PostgreSQL by swapping the
Engine URL (see 02_PostgreSQL.py for production connection concerns).
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from sqlalchemy import ForeignKey, String, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
)

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    """Declarative base shared by all ORM models in this module."""


class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    principal_investigator: Mapped[str] = mapped_column(String(120))

    samples: Mapped[list["PlantSample"]] = relationship(
        back_populates="experiment", cascade="all, delete-orphan"
    )


class PlantSample(Base):
    __tablename__ = "samples"

    id: Mapped[int] = mapped_column(primary_key=True)
    experiment_id: Mapped[int] = mapped_column(ForeignKey("experiments.id"))
    species: Mapped[str] = mapped_column(String(120))
    collection_location: Mapped[str | None] = mapped_column(String(200), default=None)

    experiment: Mapped["Experiment"] = relationship(back_populates="samples")
    measurements: Mapped[list["Measurement"]] = relationship(
        back_populates="sample", cascade="all, delete-orphan"
    )


class Measurement(Base):
    __tablename__ = "measurements"

    id: Mapped[int] = mapped_column(primary_key=True)
    sample_id: Mapped[int] = mapped_column(ForeignKey("samples.id"))
    metric_name: Mapped[str] = mapped_column(String(80))
    metric_value: Mapped[float]
    recorded_at: Mapped[datetime]

    sample: Mapped["PlantSample"] = relationship(back_populates="measurements")


def create_experiment(session: Session, title: str, principal_investigator: str) -> Experiment:
    """
    Uses the modern ORM insert pattern: construct the object, add() it to
    the session, and let flush/commit translate it into SQL. Transaction
    boundaries are the caller's responsibility (see 06_Transactions.py).
    """
    experiment = Experiment(title=title, principal_investigator=principal_investigator)
    session.add(experiment)
    session.flush()  # assigns experiment.id without committing yet
    return experiment


def add_sample_with_measurement(
    session: Session,
    experiment: Experiment,
    species: str,
    collection_location: str | None,
    metric_name: str,
    metric_value: float,
) -> PlantSample:
    sample = PlantSample(
        experiment=experiment,
        species=species,
        collection_location=collection_location,
    )
    sample.measurements.append(
        Measurement(
            metric_name=metric_name,
            metric_value=metric_value,
            recorded_at=datetime.now(timezone.utc),
        )
    )
    session.add(sample)
    session.flush()
    return sample


def list_samples_for_experiment(session: Session, experiment_id: int) -> list[PlantSample]:
    """
    Modern 2.x select() style, replacing the legacy Query API
    (session.query(...)). Bounded with a LIMIT to avoid loading unbounded
    result sets for large experiments.
    """
    stmt = (
        select(PlantSample)
        .where(PlantSample.experiment_id == experiment_id)
        .order_by(PlantSample.id)
        .limit(100)
    )
    return list(session.scalars(stmt))


def _run_demo() -> None:
    from sqlalchemy import create_engine

    logging.basicConfig(level=logging.INFO)

    # In-memory SQLite for a self-contained, dependency-free demo. A real
    # deployment would point this at DATABASE_URL (see 02_PostgreSQL.py)
    # and route connections through a pooled Engine (see
    # 07_Connection_Pooling.py).
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)

    try:
        with Session(engine) as session:
            with session.begin():  # explicit transaction boundary
                experiment = create_experiment(
                    session, title="Root Architecture Phenotyping", principal_investigator="Dr. N. Verma"
                )
                add_sample_with_measurement(
                    session,
                    experiment,
                    species="Solanum lycopersicum",
                    collection_location="Field Plot 7",
                    metric_name="root_depth_cm",
                    metric_value=34.2,
                )
            # session.begin() block committed on successful exit.

            samples = list_samples_for_experiment(session, experiment.id)
            for sample in samples:
                print(
                    f"sample id={sample.id} species={sample.species!r} "
                    f"measurements={len(sample.measurements)}"
                )
    except SQLAlchemyError as exc:
        logger.error("SQLAlchemy demo failed: %s", exc)
    finally:
        engine.dispose()


if __name__ == "__main__":
    _run_demo()
