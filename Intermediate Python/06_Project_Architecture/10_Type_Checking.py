"""Demonstrates static type checking for a scientific processing API,
designed to be checked cleanly by mypy/pyright in strict mode.

Static type checking (this file) is kept distinct from runtime
validation (raising exceptions on bad data) -- types describe what a
correct caller passes; validation guards against what an incorrect
or untrusted caller might pass.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Literal, Protocol, TypeAlias, TypedDict, TypeVar

AnalyteName: TypeAlias = Literal["glucose", "cholesterol", "creatinine"]


class RawReading(TypedDict):
    """Shape of an unvalidated reading as received from an instrument feed."""

    sample_id: str
    analyte: AnalyteName
    value: float


class InvalidReadingError(ValueError):
    """Raised at runtime when a RawReading fails domain validation.

    This is a runtime concern: TypedDict guarantees the *shape* of the
    dictionary to a type checker, but not that `value` is non-negative --
    that guarantee still has to be enforced at runtime.
    """


@dataclass(frozen=True, slots=True)
class ValidatedReading:
    sample_id: str
    analyte: AnalyteName
    value: float


T = TypeVar("T")


class Repository(Protocol[T]):
    """Structural interface for any storage backend keyed by sample_id.

    Generic over the stored type T, so the same Protocol describes a
    repository of ValidatedReading, Experiment, or any other domain
    entity without duplicating the interface definition.
    """

    def save(self, key: str, item: T) -> None: ...

    def get(self, key: str) -> T | None: ...


class InMemoryRepository(Generic[T]):
    """Concrete, generic repository implementation satisfying Repository[T]."""

    def __init__(self) -> None:
        self._items: dict[str, T] = {}

    def save(self, key: str, item: T) -> None:
        self._items[key] = item

    def get(self, key: str) -> T | None:
        return self._items.get(key)


def validate_reading(raw: RawReading) -> ValidatedReading:
    """Converts a RawReading into a ValidatedReading, enforcing runtime
    invariants that the static type of RawReading cannot express.

    Raises:
        InvalidReadingError: If `value` is negative.
    """
    if raw["value"] < 0:
        raise InvalidReadingError(
            f"reading for {raw['sample_id']} has a negative value: {raw['value']}"
        )
    return ValidatedReading(
        sample_id=raw["sample_id"], analyte=raw["analyte"], value=raw["value"]
    )


def store_validated_readings(
    repository: Repository[ValidatedReading], raw_readings: list[RawReading]
) -> list[ValidatedReading]:
    """Validates and stores a batch of raw readings.

    A type checker verifies at call sites that only a
    Repository[ValidatedReading] -- not, say, a Repository[str] -- can be
    passed here; catching that class of mistake before runtime is the
    point of this file.
    """
    validated_readings: list[ValidatedReading] = []
    for raw in raw_readings:
        reading = validate_reading(raw)
        repository.save(reading.sample_id, reading)
        validated_readings.append(reading)
    return validated_readings


if __name__ == "__main__":
    repository: InMemoryRepository[ValidatedReading] = InMemoryRepository()

    raw_readings: list[RawReading] = [
        {"sample_id": "S-700", "analyte": "glucose", "value": 92.0},
        {"sample_id": "S-701", "analyte": "cholesterol", "value": 180.0},
    ]

    stored = store_validated_readings(repository, raw_readings)
    for reading in stored:
        print(f"{reading.sample_id}: {reading.analyte}={reading.value}")

    # The following would be flagged by a static type checker (not run):
    # store_validated_readings(repository, [{"sample_id": "S-702",
    #     "analyte": "vitamin_d", "value": 30.0}])  # Literal mismatch
