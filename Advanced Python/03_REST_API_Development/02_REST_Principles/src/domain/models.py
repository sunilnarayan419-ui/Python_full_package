from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid4


class ExperimentStatus(StrEnum):
    PLANNED = "planned"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(slots=True)
class Compound:
    compound_id: UUID
    name: str
    molecular_formula: str
    created_at: datetime
    updated_at: datetime
    version: int = 1

    def etag(self) -> str:
        payload = f"{self.compound_id}:{self.version}:{self.updated_at.isoformat()}"
        return hashlib.sha256(payload.encode()).hexdigest()[:16]

    def rename(self, new_name: str) -> None:
        self.name = new_name
        self.version += 1
        self.updated_at = datetime.now(timezone.utc)


@dataclass(slots=True)
class Experiment:
    experiment_id: UUID
    compound_id: UUID
    title: str
    status: ExperimentStatus
    created_at: datetime

    @classmethod
    def schedule(cls, compound_id: UUID, title: str) -> "Experiment":
        return cls(
            experiment_id=uuid4(),
            compound_id=compound_id,
            title=title,
            status=ExperimentStatus.PLANNED,
            created_at=datetime.now(timezone.utc),
        )


@dataclass(slots=True)
class InMemoryCompoundStore:
    _compounds: dict[UUID, Compound] = field(default_factory=dict)
    _experiments: dict[UUID, list[Experiment]] = field(default_factory=dict)

    def add(self, compound: Compound) -> None:
        self._compounds[compound.compound_id] = compound
        self._experiments.setdefault(compound.compound_id, [])

    def get(self, compound_id: UUID) -> Compound | None:
        return self._compounds.get(compound_id)

    def list_experiments(self, compound_id: UUID) -> list[Experiment]:
        return self._experiments.get(compound_id, [])

    def add_experiment(self, experiment: Experiment) -> None:
        self._experiments.setdefault(experiment.compound_id, []).append(experiment)
