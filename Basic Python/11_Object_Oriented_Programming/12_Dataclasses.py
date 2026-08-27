"""
12_Dataclasses.py

Concept: Dataclasses
`@dataclass` generates boilerplate (init, repr, equality) for classes
that primarily hold structured data. This file progresses from a plain
dataclass to defaults/validation to an immutable, carefully controlled
scientific data model.
"""

from __future__ import annotations

from dataclasses import dataclass, field


# --------------------------------------------------------------------------- #
# University Level
# --------------------------------------------------------------------------- #
@dataclass
class UniversityPlantSample:
    """A simple dataclass: __init__, __repr__, and __eq__ are generated
    automatically from the type-annotated fields."""

    species: str
    height_cm: float


class UniversityDataclasses:
    @staticmethod
    def run() -> None:
        print("--- UniversityDataclasses ---")
        sample_a = UniversityPlantSample(species="Oryza sativa", height_cm=30.0)
        sample_b = UniversityPlantSample(species="Oryza sativa", height_cm=30.0)

        print(sample_a)
        print(f"Equal by value? {sample_a == sample_b}")


# --------------------------------------------------------------------------- #
# Interview Level
# --------------------------------------------------------------------------- #
@dataclass
class InterviewExperimentMeasurement:
    """Uses defaults, default_factory, and __post_init__ validation for a
    single experimental measurement record."""

    sample_id: str
    value: float
    unit: str = "ng/uL"
    tags: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.sample_id.strip():
            raise ValueError("sample_id cannot be empty")
        if self.value < 0:
            raise ValueError("value cannot be negative")


class InterviewDataclasses:
    @staticmethod
    def run() -> None:
        print("--- InterviewDataclasses ---")
        measurement = InterviewExperimentMeasurement(sample_id="S-11", value=45.2)
        measurement.tags.append("qc-passed")
        print(measurement)

        try:
            InterviewExperimentMeasurement(sample_id="S-12", value=-3.0)
        except ValueError as error:
            print(f"Rejected invalid measurement: {error}")


# --------------------------------------------------------------------------- #
# Industry Level
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class IndustryCompoundRecord:
    """An immutable, carefully controlled scientific data model: once a
    compound record is created and validated, it cannot be mutated,
    which makes it safe to share across a pipeline without defensive
    copying.
    """

    compound_id: str
    molecular_weight: float
    logp: float
    descriptors: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.compound_id.strip():
            raise ValueError("compound_id cannot be empty")
        if self.molecular_weight < 0:
            raise ValueError("molecular_weight cannot be negative")

    def with_additional_descriptor(self, descriptor: str) -> "IndustryCompoundRecord":
        """Since the dataclass is frozen, 'changing' it means returning a
        new instance rather than mutating the existing one."""
        return IndustryCompoundRecord(
            compound_id=self.compound_id,
            molecular_weight=self.molecular_weight,
            logp=self.logp,
            descriptors=self.descriptors + (descriptor,),
        )


class IndustryDataclasses:
    @staticmethod
    def run() -> None:
        print("--- IndustryDataclasses ---")
        record = IndustryCompoundRecord(
            compound_id="CMP-900", molecular_weight=298.4, logp=1.9
        )
        updated_record = record.with_additional_descriptor("passes-lipinski")

        print(record)
        print(updated_record)

        try:
            record.molecular_weight = 500.0  # type: ignore[misc]
        except Exception as error:  # dataclasses.FrozenInstanceError
            print(f"Mutation rejected on frozen record: {type(error).__name__}: {error}")


if __name__ == "__main__":
    UniversityDataclasses.run()
    InterviewDataclasses.run()
    IndustryDataclasses.run()
