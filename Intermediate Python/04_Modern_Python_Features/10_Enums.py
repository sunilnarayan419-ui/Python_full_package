from __future__ import annotations

from enum import Enum, IntEnum, StrEnum, auto


class SampleCategory(Enum):
    """Represents the biological category of a lab sample."""

    BLOOD = auto()
    TISSUE = auto()
    SALIVA = auto()
    URINE = auto()


class UniversityEnums:
    """Use an Enum to represent scientific sample categories instead of
    loose strings, giving a fixed, named set of valid values."""

    @staticmethod
    def describe(category: SampleCategory) -> str:
        """Time: O(1)."""
        return f"Sample category: {category.name}"

    @staticmethod
    def run() -> None:
        for category in SampleCategory:
            print("University:", UniversityEnums.describe(category))
        print("University: comparison ->", SampleCategory.BLOOD == SampleCategory.BLOOD)


class Priority(IntEnum):
    """IntEnum allows direct numeric comparison, useful for ordering
    urgency levels."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class InvalidPriorityError(ValueError):
    """Raised when a raw value cannot be converted to a valid Priority."""


class InterviewEnums:
    """Handle enum validation, conversion, comparisons, and practical
    branching using lab-task priority levels."""

    @staticmethod
    def parse_priority(raw_value: str | int) -> Priority:
        """Convert a raw value (name or numeric) into a Priority member.

        Time: O(1)
        Raises InvalidPriorityError for unrecognized input.
        """
        if isinstance(raw_value, int):
            try:
                return Priority(raw_value)
            except ValueError as error:
                raise InvalidPriorityError(f"invalid priority value: {raw_value}") from error
        try:
            return Priority[raw_value.upper()]
        except KeyError as error:
            raise InvalidPriorityError(f"invalid priority name: {raw_value}") from error

    @staticmethod
    def requires_immediate_attention(priority: Priority) -> bool:
        """IntEnum members compare directly with integers/each other.

        Time: O(1)
        """
        return priority >= Priority.HIGH

    @staticmethod
    def run() -> None:
        for raw in ["high", 1, "critical"]:
            priority = InterviewEnums.parse_priority(raw)
            urgent = InterviewEnums.requires_immediate_attention(priority)
            print(f"Interview: parsed {raw!r} -> {priority.name}, urgent={urgent}")

        try:
            InterviewEnums.parse_priority("urgent")
        except InvalidPriorityError as error:
            print("Interview: validation caught ->", error)


class ExperimentStatus(StrEnum):
    """String-valued enum for experiment lifecycle state, chosen because
    StrEnum values serialize cleanly to JSON/logs as plain strings while
    still constraining valid values to this fixed set."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

    @classmethod
    def from_raw(cls, raw_value: str) -> "ExperimentStatus":
        """Time: O(1). Raises ValueError via the Enum machinery for
        unrecognized raw values."""
        return cls(raw_value.lower())

    def is_terminal(self) -> bool:
        """Domain behavior attached directly to the enum member.

        Time: O(1)
        """
        return self in (ExperimentStatus.COMPLETED, ExperimentStatus.FAILED, ExperimentStatus.CANCELLED)


_ALLOWED_TRANSITIONS: dict[ExperimentStatus, frozenset[ExperimentStatus]] = {
    ExperimentStatus.PENDING: frozenset({ExperimentStatus.RUNNING, ExperimentStatus.CANCELLED}),
    ExperimentStatus.RUNNING: frozenset({ExperimentStatus.COMPLETED, ExperimentStatus.FAILED}),
    ExperimentStatus.COMPLETED: frozenset(),
    ExperimentStatus.FAILED: frozenset(),
    ExperimentStatus.CANCELLED: frozenset(),
}


class InvalidStateTransitionError(ValueError):
    """Raised when an experiment status transition is not allowed."""


class IndustryEnums:
    """A strongly typed domain-state model for experiment lifecycle
    status, using StrEnum for clean serialization and an explicit
    transition table to enforce valid state changes - replacing scattered
    string comparisons with a single source of truth for domain rules.
    """

    def __init__(self, experiment_id: str) -> None:
        self.experiment_id = experiment_id
        self.status: ExperimentStatus = ExperimentStatus.PENDING

    def transition_to(self, new_status: ExperimentStatus) -> None:
        """Time: O(1). Raises InvalidStateTransitionError for disallowed
        transitions (e.g. COMPLETED -> RUNNING)."""
        allowed = _ALLOWED_TRANSITIONS[self.status]
        if new_status not in allowed:
            raise InvalidStateTransitionError(
                f"cannot transition {self.experiment_id} from {self.status} to {new_status}"
            )
        self.status = new_status

    @staticmethod
    def run() -> None:
        experiment = IndustryEnums("EXP-2026-001")
        print("Industry: initial status ->", experiment.status, "value ->", experiment.status.value)

        experiment.transition_to(ExperimentStatus.RUNNING)
        experiment.transition_to(ExperimentStatus.COMPLETED)
        print("Industry: final status ->", experiment.status, "terminal ->", experiment.status.is_terminal())

        try:
            experiment.transition_to(ExperimentStatus.RUNNING)
        except InvalidStateTransitionError as error:
            print("Industry: invalid transition caught ->", error)


if __name__ == "__main__":
    UniversityEnums.run()
    InterviewEnums.run()
    IndustryEnums.run()
