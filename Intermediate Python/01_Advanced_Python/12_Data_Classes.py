from __future__ import annotations

from dataclasses import dataclass, field


class UniversityDataClasses:
    """Demonstrates a basic @dataclass acting as a simple data record."""

    @dataclass
    class PlantSample:
        species: str
        height_cm: float
        leaf_count: int

    @staticmethod
    def run() -> None:
        sample = UniversityDataClasses.PlantSample(species="Arabidopsis thaliana", height_cm=12.4, leaf_count=8)
        print(sample)


class InterviewDataClasses:
    """Demonstrates dataclass defaults, default_factory, and __post_init__
    validation, showing awareness of common dataclass pitfalls such as
    mutable default arguments."""

    @dataclass
    class ExperimentTrial:
        trial_id: str
        replicate_values: list[float] = field(default_factory=list)
        notes: str = ""

        def __post_init__(self) -> None:
            if any(v < 0 for v in self.replicate_values):
                raise ValueError("replicate_values must be non-negative")

        @property
        def mean_value(self) -> float:
            return sum(self.replicate_values) / len(self.replicate_values) if self.replicate_values else 0.0

    @staticmethod
    def run() -> None:
        trial = InterviewDataClasses.ExperimentTrial(trial_id="T-001", replicate_values=[4.2, 4.5, 4.1])
        print(trial)
        print(f"mean_value={trial.mean_value:.3f}")

        try:
            InterviewDataClasses.ExperimentTrial(trial_id="T-002", replicate_values=[-1.0])
        except ValueError as exc:
            print(f"caught expected error: {exc}")


class IndustryDataClasses:
    """Demonstrates production-grade dataclass usage: frozen (immutable)
    records for hashable, thread-safe value objects, field-level metadata,
    computed properties, and composition of nested dataclasses."""

    @dataclass(frozen=True, slots=True)
    class Coordinates:
        latitude: float
        longitude: float

        def __post_init__(self) -> None:
            if not (-90.0 <= self.latitude <= 90.0):
                raise ValueError("latitude out of range")
            if not (-180.0 <= self.longitude <= 180.0):
                raise ValueError("longitude out of range")

    @dataclass(frozen=True, slots=True)
    class FieldTrialRecord:
        trial_id: str
        crop_species: str
        location: "IndustryDataClasses.Coordinates"
        yield_kg_per_hectare: float = field(metadata={"unit": "kg/ha"})
        tags: tuple[str, ...] = field(default_factory=tuple)

        def __post_init__(self) -> None:
            if self.yield_kg_per_hectare < 0:
                raise ValueError("yield_kg_per_hectare cannot be negative")

        def with_tag(self, tag: str) -> "IndustryDataClasses.FieldTrialRecord":
            """Returns a new immutable record with an added tag, since the
            instance itself is frozen and cannot be mutated in place."""
            return IndustryDataClasses.FieldTrialRecord(
                trial_id=self.trial_id,
                crop_species=self.crop_species,
                location=self.location,
                yield_kg_per_hectare=self.yield_kg_per_hectare,
                tags=(*self.tags, tag),
            )

    @staticmethod
    def run() -> None:
        location = IndustryDataClasses.Coordinates(latitude=17.385, longitude=78.4867)
        record = IndustryDataClasses.FieldTrialRecord(
            trial_id="FT-2024-09",
            crop_species="Oryza sativa",
            location=location,
            yield_kg_per_hectare=4200.5,
        )
        print(record)

        tagged_record = record.with_tag("drought-tolerant")
        print(tagged_record)
        print(f"original tags unchanged: {record.tags}")

        try:
            record.yield_kg_per_hectare = -50.0  # type: ignore[misc]
        except AttributeError as exc:
            print(f"caught expected error mutating frozen record: {exc}")

        try:
            IndustryDataClasses.FieldTrialRecord(
                trial_id="FT-2024-10",
                crop_species="Zea mays",
                location=location,
                yield_kg_per_hectare=-100.0,
            )
        except ValueError as exc:
            print(f"caught expected error: {exc}")


if __name__ == "__main__":
    UniversityDataClasses.run()
    InterviewDataClasses.run()
    IndustryDataClasses.run()
