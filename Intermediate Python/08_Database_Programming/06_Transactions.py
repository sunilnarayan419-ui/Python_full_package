"""
06_Transactions.py

Focused demonstration of transaction management for a multi-step
scientific workflow: creating an experiment together with its samples
and initial measurements must be atomic -- either the entire operation
succeeds, or none of it is persisted.

Important: Python code does not itself provide transactional guarantees.
The underlying database engine (here, SQLite via SQLAlchemy) provides
atomicity, consistency, isolation, and durability (ACID); this module's
job is only to define correct transaction *boundaries* and to ensure
exceptions trigger a rollback rather than a partial commit.

    Atomicity   - the experiment/samples/measurements batch either fully
                  commits or fully rolls back.
    Consistency - foreign key and NOT NULL constraints in the schema keep
                  the database in a valid state before and after the
                  transaction.
    Isolation   - the database engine controls what concurrent
                  transactions can see of each other's uncommitted work.
    Durability  - once COMMIT returns, the database engine guarantees the
                  change survives a crash (subject to its own fsync/WAL
                  configuration).
"""

from __future__ import annotations

import logging

from sqlalchemy import ForeignKey, String, create_engine, select
from sqlalchemy.exc import SQLAlchemyError
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

    id: Mapped[int] = mapped_column(primary_key=True)
    experiment_id: Mapped[int] = mapped_column(ForeignKey("experiments.id"))
    species: Mapped[str] = mapped_column(String(120))

    experiment: Mapped["Experiment"] = relationship(back_populates="samples")
    measurements: Mapped[list["Measurement"]] = relationship(back_populates="sample")


class Measurement(Base):
    __tablename__ = "measurements"

    id: Mapped[int] = mapped_column(primary_key=True)
    sample_id: Mapped[int] = mapped_column(ForeignKey("samples.id"))
    metric_name: Mapped[str] = mapped_column(String(80))
    metric_value: Mapped[float]

    sample: Mapped["Sample"] = relationship(back_populates="measurements")


class WorkflowError(RuntimeError):
    """Raised when the atomic experiment-creation workflow fails."""


def create_experiment_batch(
    session: Session,
    title: str,
    sample_specs: list[dict],
    *,
    fail_after_samples: bool = False,
) -> int:
    """
    Creates an experiment together with its samples and measurements as a
    single atomic unit of work.

    `fail_after_samples` exists only to deterministically demonstrate the
    rollback path in the demo below -- it simulates a failure (e.g. a
    downstream validation error) after some rows have already been
    flushed to the database but before the transaction commits.

    session.begin() defines the transaction boundary: on normal exit from
    the `with` block SQLAlchemy issues COMMIT; on an exception it issues
    ROLLBACK before the exception propagates. No partial state from a
    failed call is ever visible to other transactions.
    """
    try:
        with session.begin():
            experiment = Experiment(title=title)
            session.add(experiment)
            session.flush()  # experiment.id now populated, not yet committed

            for spec in sample_specs:
                sample = Sample(experiment_id=experiment.id, species=spec["species"])
                session.add(sample)
                session.flush()

                for metric_name, metric_value in spec.get("measurements", {}).items():
                    session.add(
                        Measurement(
                            sample_id=sample.id,
                            metric_name=metric_name,
                            metric_value=metric_value,
                        )
                    )

            if fail_after_samples:
                # Simulates a late failure (e.g. an external validation
                # service rejecting the batch) after rows are already
                # staged in this transaction.
                raise WorkflowError("simulated downstream validation failure")

            session.flush()
            return experiment.id
    except SQLAlchemyError as exc:
        # session.begin()'s context manager has already rolled back by
        # the time this runs; we translate to a domain-level error rather
        # than leaking the raw DBAPI/SQLAlchemy exception.
        raise WorkflowError("failed to create experiment batch") from exc
    # Note: WorkflowError raised intentionally above propagates as-is;
    # session.begin() still rolls back before it reaches the caller.


def _count_experiments(session: Session) -> int:
    return len(list(session.scalars(select(Experiment))))


def _run_demo() -> None:
    logging.basicConfig(level=logging.INFO)
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)

    try:
        with Session(engine) as session:
            # --- Successful atomic batch ---
            experiment_id = create_experiment_batch(
                session,
                title="Photosynthetic Efficiency Panel",
                sample_specs=[
                    {"species": "Zea mays", "measurements": {"chlorophyll_content": 42.1}},
                    {"species": "Sorghum bicolor", "measurements": {"chlorophyll_content": 39.8}},
                ],
            )
            print(f"committed experiment id={experiment_id}, "
                  f"total experiments now={_count_experiments(session)}")

            # --- Failing atomic batch: nothing should be persisted ---
            before = _count_experiments(session)
            try:
                create_experiment_batch(
                    session,
                    title="Should Not Persist",
                    sample_specs=[{"species": "Oryza sativa", "measurements": {}}],
                    fail_after_samples=True,
                )
            except WorkflowError as exc:
                print(f"expected rollback after failure: {exc}")
            after = _count_experiments(session)
            assert before == after, "rollback failed: partial write detected"
            print(f"experiment count unchanged after rollback: {after}")
    finally:
        engine.dispose()


if __name__ == "__main__":
    _run_demo()
