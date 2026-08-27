from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid4


class AssayType(StrEnum):
    BINDING = "binding"
    FUNCTIONAL = "functional"
    ADMET = "admet"
    CYTOTOXICITY = "cytotoxicity"


class ScreeningRunStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    VALIDATED = "validated"
    FAILED = "failed"


@dataclass(slots=True)
class DomainError(Exception):
    code: str
    message: str


class ScreeningRunNotFoundError(DomainError):
    def __init__(self, run_id: UUID) -> None:
        super().__init__(code="SCREENING_RUN_NOT_FOUND", message=f"Screening run {run_id} was not found.")


class InvalidStatusTransitionError(DomainError):
    def __init__(self, current: ScreeningRunStatus, target: ScreeningRunStatus) -> None:
        super().__init__(
            code="INVALID_STATUS_TRANSITION",
            message=f"Cannot transition screening run from {current} to {target}.",
        )


_ALLOWED_TRANSITIONS: dict[ScreeningRunStatus, set[ScreeningRunStatus]] = {
    ScreeningRunStatus.QUEUED: {ScreeningRunStatus.RUNNING, ScreeningRunStatus.FAILED},
    ScreeningRunStatus.RUNNING: {ScreeningRunStatus.VALIDATED, ScreeningRunStatus.FAILED},
    ScreeningRunStatus.VALIDATED: set(),
    ScreeningRunStatus.FAILED: set(),
}


@dataclass(slots=True)
class ScreeningRun:
    run_id: UUID
    compound_id: UUID
    assay_type: AssayType
    status: ScreeningRunStatus
    score: float | None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(cls, compound_id: UUID, assay_type: AssayType) -> "ScreeningRun":
        now = datetime.now(timezone.utc)
        return cls(
            run_id=uuid4(),
            compound_id=compound_id,
            assay_type=assay_type,
            status=ScreeningRunStatus.QUEUED,
            score=None,
            created_at=now,
            updated_at=now,
        )

    def transition_to(self, target: ScreeningRunStatus, *, score: float | None = None) -> None:
        if target not in _ALLOWED_TRANSITIONS[self.status]:
            raise InvalidStatusTransitionError(self.status, target)
        self.status = target
        if score is not None:
            self.score = score
        self.updated_at = datetime.now(timezone.utc)
