from __future__ import annotations

import sys


class UniversitySlots:
    """Simple demonstration of __slots__ restricting instance attributes
    on a plant measurement record."""

    __slots__ = ("species", "height_cm")

    def __init__(self, species: str, height_cm: float) -> None:
        self.species = species
        self.height_cm = height_cm

    @staticmethod
    def run() -> None:
        plant = UniversitySlots("Basil", 24.5)
        print("University:", plant.species, plant.height_cm)
        try:
            plant.color = "green"  # type: ignore[attr-defined]
        except AttributeError as error:
            print("University: dynamic attribute rejected ->", error)


class RegularSampleRecord:
    """A normal class (with a __dict__) for comparison purposes only."""

    def __init__(self, sample_id: str, ph_level: float) -> None:
        self.sample_id = sample_id
        self.ph_level = ph_level


class SlottedSampleRecord:
    """A slotted equivalent of RegularSampleRecord."""

    __slots__ = ("sample_id", "ph_level")

    def __init__(self, sample_id: str, ph_level: float) -> None:
        self.sample_id = sample_id
        self.ph_level = ph_level


class InterviewSlots:
    """Compare normal classes and slotted classes programmatically -
    memory footprint and dynamic attribute behavior differ; execution
    speed differences are implementation-dependent and not guaranteed."""

    @staticmethod
    def compare_memory(count: int) -> dict[str, int]:
        """Compare total approximate memory for many instances of each class.

        Time: O(n), Space: O(n) for both instance lists
        """
        regular_instances = [RegularSampleRecord(f"S{i}", 7.0) for i in range(count)]
        slotted_instances = [SlottedSampleRecord(f"S{i}", 7.0) for i in range(count)]

        regular_size = sum(sys.getsizeof(instance) + sys.getsizeof(instance.__dict__) for instance in regular_instances)
        slotted_size = sum(sys.getsizeof(instance) for instance in slotted_instances)

        return {"regular_bytes": regular_size, "slotted_bytes": slotted_size}

    @staticmethod
    def has_dict_attribute(instance: object) -> bool:
        """Time: O(1)."""
        return hasattr(instance, "__dict__")

    @staticmethod
    def run() -> None:
        sizes = InterviewSlots.compare_memory(1000)
        print("Interview: approximate memory (1000 instances each) ->", sizes)
        print(
            "Interview: regular instance has __dict__ ->",
            InterviewSlots.has_dict_attribute(RegularSampleRecord("S1", 7.0)),
        )
        print(
            "Interview: slotted instance has __dict__ ->",
            InterviewSlots.has_dict_attribute(SlottedSampleRecord("S1", 7.0)),
        )


class GenomicReadBase:
    """Base class in a slotted inheritance chain. Subclasses must also
    declare __slots__ (including an empty tuple if adding no new
    attributes) or they silently regain a __dict__, negating the
    memory benefit.
    """

    __slots__ = ("read_id", "sequence")

    def __init__(self, read_id: str, sequence: str) -> None:
        self.read_id = read_id
        self.sequence = sequence


class QualityScoredRead(GenomicReadBase):
    """Adds quality scores while preserving the slotted memory benefit
    by declaring its own __slots__ for its additional attribute."""

    __slots__ = ("quality_scores",)

    def __init__(self, read_id: str, sequence: str, quality_scores: list[int]) -> None:
        super().__init__(read_id, sequence)
        self.quality_scores = quality_scores

    def mean_quality(self) -> float:
        """Time: O(n)."""
        if not self.quality_scores:
            return 0.0
        return sum(self.quality_scores) / len(self.quality_scores)


class IndustrySlots:
    """Uses __slots__ for a high-volume genomic sequencing-read object,
    where millions of read objects may exist simultaneously and the
    per-instance memory saving from omitting a __dict__ becomes
    materially significant. __slots__ is not applied blindly elsewhere -
    it is a deliberate choice justified by this object's volume.
    """

    @staticmethod
    def process_reads(reads: list[QualityScoredRead]) -> dict[str, float]:
        """Time: O(n * m) where m is average quality-score list length."""
        if not reads:
            return {"read_count": 0, "average_quality": 0.0}
        mean_qualities = [read.mean_quality() for read in reads]
        return {
            "read_count": len(reads),
            "average_quality": sum(mean_qualities) / len(mean_qualities),
        }

    @staticmethod
    def run() -> None:
        reads = [
            QualityScoredRead("READ-1", "ACGTACGT", [35, 38, 40, 37]),
            QualityScoredRead("READ-2", "TTGGCCAA", [30, 32, 29, 33]),
        ]
        summary = IndustrySlots.process_reads(reads)
        print("Industry: read batch summary ->", summary)

        try:
            reads[0].new_field = "not allowed"  # type: ignore[attr-defined]
        except AttributeError as error:
            print("Industry: dynamic attribute rejected on high-volume object ->", error)


if __name__ == "__main__":
    UniversitySlots.run()
    InterviewSlots.run()
    IndustrySlots.run()
