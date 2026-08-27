"""
05_CRUD.py

Production CRUD architecture for the scientific data platform, separating
concerns into:

    Domain models      (SQLAlchemy ORM entities)
    Repository layer    (SampleRepository -- raw data access)
    Service layer        (ExperimentService -- business rules, validation,
                          domain exceptions)

The repository never leaks raw database exceptions to callers; it
translates them into meaningful domain exceptions. The service layer
composes repository calls into coherent business operations and owns
input validation.
"""

from __future__ import annotations

import logging

from sqlalchemy import ForeignKey, String, UniqueConstraint, create_engine, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    pass


class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))

    samples: Mapped[list["Sample"]] = relationship(back_populates="experiment")


class Sample(Base):
    __tablename__ = "samples"
    __table_args__ = (
        UniqueConstraint(
            "experiment_id", "species", "collection_location", name="uq_sample_identity"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    experiment_id: Mapped[int] = mapped_column(ForeignKey("experiments.id"))
    species: Mapped[str] = mapped_column(String(120))
    collection_location: Mapped[str | None] = mapped_column(String(200), default=None)

    experiment: Mapped["Experiment"] = relationship(back_populates="samples")


# ---------------------------------------------------------------------------
# Domain-level exceptions. Callers of the service layer should only ever
# need to handle these -- never raw SQLAlchemy/DBAPI exceptions.
# ---------------------------------------------------------------------------

class SampleNotFoundError(LookupError):
    """Raised when a requested scientific sample does not exist."""


class DuplicateSampleError(ValueError):
    """Raised when a sample violates a uniqueness constraint."""


class InvalidSampleDataError(ValueError):
    """Raised when caller-supplied sample data fails validation."""


class DatabaseError(RuntimeError):
    """Raised when an underlying database operation fails unexpectedly."""


# ---------------------------------------------------------------------------
# Repository layer: thin, mechanical data access. No business rules here.
# ---------------------------------------------------------------------------

class SampleRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, experiment_id: int, species: str, collection_location: str | None) -> Sample:
        sample = Sample(
            experiment_id=experiment_id,
            species=species,
            collection_location=collection_location,
        )
        self._session.add(sample)
        try:
            self._session.flush()
        except IntegrityError as exc:
            raise DuplicateSampleError(
                f"sample with species={species!r} already exists for this experiment"
            ) from exc
        except SQLAlchemyError as exc:
            raise DatabaseError("failed to create sample") from exc
        return sample

    def get_by_id(self, sample_id: int) -> Sample:
        sample = self._session.get(Sample, sample_id)
        if sample is None:
            raise SampleNotFoundError(f"sample id={sample_id} not found")
        return sample

    def list_by_experiment(self, experiment_id: int, limit: int = 100, offset: int = 0) -> list[Sample]:
        stmt = (
            select(Sample)
            .where(Sample.experiment_id == experiment_id)
            .order_by(Sample.id)
            .limit(limit)
            .offset(offset)
        )
        try:
            return list(self._session.scalars(stmt))
        except SQLAlchemyError as exc:
            raise DatabaseError("failed to list samples") from exc

    def update_location(self, sample_id: int, collection_location: str) -> Sample:
        sample = self.get_by_id(sample_id)
        sample.collection_location = collection_location
        try:
            self._session.flush()
        except SQLAlchemyError as exc:
            raise DatabaseError("failed to update sample") from exc
        return sample

    def delete(self, sample_id: int) -> None:
        sample = self.get_by_id(sample_id)
        self._session.delete(sample)
        try:
            self._session.flush()
        except SQLAlchemyError as exc:
            raise DatabaseError("failed to delete sample") from exc


# ---------------------------------------------------------------------------
# Service layer: validation + business rules, composed on top of the
# repository. This is what application code (API handlers, CLI commands,
# background jobs) should depend on.
# ---------------------------------------------------------------------------

class ExperimentService:
    def __init__(self, session: Session) -> None:
        self._session = session
        self._samples = SampleRepository(session)

    def register_sample(
        self, experiment_id: int, species: str, collection_location: str | None
    ) -> Sample:
        if not species or not species.strip():
            raise InvalidSampleDataError("species is required")
        with self._session.begin_nested():
            return self._samples.create(experiment_id, species.strip(), collection_location)

    def get_sample(self, sample_id: int) -> Sample:
        return self._samples.get_by_id(sample_id)

    def list_samples(self, experiment_id: int, page: int = 1, page_size: int = 50) -> list[Sample]:
        if page < 1 or page_size < 1:
            raise InvalidSampleDataError("page and page_size must be positive")
        return self._samples.list_by_experiment(
            experiment_id, limit=page_size, offset=(page - 1) * page_size
        )

    def relocate_sample(self, sample_id: int, new_location: str) -> Sample:
        if not new_location or not new_location.strip():
            raise InvalidSampleDataError("new_location is required")
        return self._samples.update_location(sample_id, new_location.strip())

    def remove_sample(self, sample_id: int) -> None:
        self._samples.delete(sample_id)


def _run_demo() -> None:
    logging.basicConfig(level=logging.INFO)
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)

    try:
        with Session(engine) as session:
            with session.begin():
                experiment = Experiment(title="Salinity Stress Response")
                session.add(experiment)
                session.flush()
                service = ExperimentService(session)

                sample = service.register_sample(experiment.id, "Arabidopsis thaliana", "Growth Chamber 1")
                print(f"created sample id={sample.id}")

                try:
                    service.register_sample(experiment.id, "Arabidopsis thaliana", "Growth Chamber 1")
                except DuplicateSampleError as exc:
                    print(f"expected duplicate rejection: {exc}")

                try:
                    service.get_sample(999_999)
                except SampleNotFoundError as exc:
                    print(f"expected not-found: {exc}")

                updated = service.relocate_sample(sample.id, "Growth Chamber 2")
                print(f"relocated sample id={updated.id} -> {updated.collection_location}")

                for s in service.list_samples(experiment.id):
                    print(f"listed sample id={s.id} species={s.species!r}")

                service.remove_sample(sample.id)
                print("sample removed")
    except SQLAlchemyError as exc:
        logger.error("CRUD demo failed at the database layer: %s", exc)
    finally:
        engine.dispose()


if __name__ == "__main__":
    _run_demo()
