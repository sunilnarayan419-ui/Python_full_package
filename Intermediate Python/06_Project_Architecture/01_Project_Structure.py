"""Demonstrates professional project structure for a scientific software
platform through clearly separated architectural layers.

Recommended physical project layout this module conceptually represents:

    scientific_platform/
    ├── app/
    │   ├── api/            # HTTP/CLI entry points, request/response shaping
    │   ├── domain/          # Sample, Experiment, Measurement models + rules
    │   ├── services/        # Use-case orchestration (application services)
    │   ├── repositories/    # Persistence boundaries (interfaces + impls)
    │   └── config/          # Typed configuration objects
    ├── tests/
    │   ├── unit/
    │   └── integration/
    ├── scripts/             # One-off operational scripts
    └── pyproject.toml

Each section below is separated with a header comment matching the
directory it would live in, so the boundaries are visible even though
everything is collapsed into one file for this learning example.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


# ---------------------------------------------------------------------------
# app/domain/ -- core domain models and rules, no I/O, no framework code
# ---------------------------------------------------------------------------


class InvalidMeasurementError(ValueError):
    """Raised when a scientific measurement violates a domain invariant."""


@dataclass(frozen=True, slots=True)
class Measurement:
    sample_id: str
    value: float
    unit: str

    def __post_init__(self) -> None:
        if self.value < 0:
            raise InvalidMeasurementError(
                f"measurement for {self.sample_id} cannot be negative"
            )


@dataclass(frozen=True, slots=True)
class Experiment:
    experiment_id: str
    measurements: tuple[Measurement, ...]

    def mean_value(self) -> float:
        if not self.measurements:
            raise InvalidMeasurementError("cannot average an empty measurement set")
        return sum(m.value for m in self.measurements) / len(self.measurements)


# ---------------------------------------------------------------------------
# app/repositories/ -- persistence boundary, defined as an interface here;
# a real project would put the interface in repositories/interfaces.py and
# concrete adapters (Postgres, S3, etc.) in repositories/impl/.
# ---------------------------------------------------------------------------


class ExperimentRepository(Protocol):
    """Structural interface for experiment persistence."""

    def save(self, experiment: Experiment) -> None: ...

    def get(self, experiment_id: str) -> Experiment | None: ...


class InMemoryExperimentRepository:
    """A concrete adapter suitable for tests and local development.

    Production code would instead provide e.g. a PostgresExperimentRepository
    living under app/repositories/impl/, implementing the same Protocol.
    """

    def __init__(self) -> None:
        self._storage: dict[str, Experiment] = {}

    def save(self, experiment: Experiment) -> None:
        self._storage[experiment.experiment_id] = experiment

    def get(self, experiment_id: str) -> Experiment | None:
        return self._storage.get(experiment_id)


# ---------------------------------------------------------------------------
# app/services/ -- application/use-case layer: orchestrates domain objects
# and repositories, contains no domain rules of its own.
# ---------------------------------------------------------------------------


class ExperimentAnalysisService:
    """Use case: record an experiment and report its summary statistics.

    Depends only on the repository interface (dependency inversion), so
    it can be tested with InMemoryExperimentRepository and deployed with
    a real database-backed implementation without any code changes here.
    """

    def __init__(self, repository: ExperimentRepository) -> None:
        self._repository = repository

    def record_experiment(self, experiment: Experiment) -> None:
        self._repository.save(experiment)

    def summarize(self, experiment_id: str) -> float:
        experiment = self._repository.get(experiment_id)
        if experiment is None:
            raise LookupError(f"experiment {experiment_id} not found")
        return experiment.mean_value()


# ---------------------------------------------------------------------------
# app/api/ -- thin entry-point layer; translates external calls into
# service invocations and formats output. Contains no business logic.
# ---------------------------------------------------------------------------


def handle_record_and_summarize_request(
    service: ExperimentAnalysisService, experiment: Experiment
) -> str:
    """Represents what a CLI command or HTTP handler would do: delegate
    to the service layer and format the result for the caller.
    """
    service.record_experiment(experiment)
    mean_value = service.summarize(experiment.experiment_id)
    return f"experiment {experiment.experiment_id}: mean={mean_value:.3f}"


if __name__ == "__main__":
    repository = InMemoryExperimentRepository()
    service = ExperimentAnalysisService(repository)

    experiment = Experiment(
        experiment_id="EXP-900",
        measurements=(
            Measurement(sample_id="S-1", value=12.5, unit="ng/uL"),
            Measurement(sample_id="S-2", value=15.0, unit="ng/uL"),
        ),
    )

    print(handle_record_and_summarize_request(service, experiment))
