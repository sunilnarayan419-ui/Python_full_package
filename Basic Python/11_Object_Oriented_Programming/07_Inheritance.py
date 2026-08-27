"""
07_Inheritance.py

Concept: Inheritance
Inheritance models a genuine IS-A relationship: a derived class reuses
and specializes the behavior of a base class. This file shows single
inheritance, overriding with super(), and a judgment call about when
inheritance is (and is not) the right tool.
"""

from __future__ import annotations


# --------------------------------------------------------------------------- #
# University Level
# --------------------------------------------------------------------------- #
class UniversityInheritance:
    """Base class: a generic biological sample."""

    def __init__(self, sample_id: str) -> None:
        self.sample_id = sample_id

    def describe(self) -> str:
        return f"Sample {self.sample_id}"

    @staticmethod
    def run() -> None:
        print("--- UniversityInheritance ---")

        class PlantSample(UniversityInheritance):
            """PlantSample IS-A biological sample, specialized for plants."""

            def __init__(self, sample_id: str, species: str) -> None:
                super().__init__(sample_id)
                self.species = species

        plant = PlantSample(sample_id="P-01", species="Solanum lycopersicum")
        print(plant.describe())
        print(f"Species: {plant.species}")


# --------------------------------------------------------------------------- #
# Interview Level
# --------------------------------------------------------------------------- #
class InterviewInheritance:
    """Base class with a method designed to be overridden by subclasses."""

    def __init__(self, sample_id: str) -> None:
        self.sample_id = sample_id

    def describe(self) -> str:
        return f"Generic sample {self.sample_id}"

    @staticmethod
    def run() -> None:
        print("--- InterviewInheritance ---")

        class MicrobialSample(InterviewInheritance):
            """MicrobialSample overrides describe() to add microbe-specific
            detail, while reusing the base constructor via super()."""

            def __init__(self, sample_id: str, organism: str, colony_count: int) -> None:
                super().__init__(sample_id)
                if colony_count < 0:
                    raise ValueError("colony_count cannot be negative")
                self.organism = organism
                self.colony_count = colony_count

            def describe(self) -> str:
                base_description = super().describe()
                return f"{base_description} -> {self.organism}, {self.colony_count} CFU"

        culture = MicrobialSample(sample_id="M-07", organism="E. coli", colony_count=1523)
        print(culture.describe())


# --------------------------------------------------------------------------- #
# Industry Level
# --------------------------------------------------------------------------- #
class BiologicalSample:
    """Genuine shared abstraction: every sample in the lab has an ID and
    a collection date, regardless of what kind of sample it is."""

    def __init__(self, sample_id: str, collection_date: str) -> None:
        if not sample_id.strip():
            raise ValueError("sample_id cannot be empty")
        self.sample_id = sample_id
        self.collection_date = collection_date

    def describe(self) -> str:
        return f"Sample {self.sample_id} collected {self.collection_date}"


class PlantSample(BiologicalSample):
    """PlantSample IS-A BiologicalSample: a real specialization, not an
    artificial one, since every plant sample is also a biological sample."""

    def __init__(self, sample_id: str, collection_date: str, species: str) -> None:
        super().__init__(sample_id, collection_date)
        self.species = species

    def describe(self) -> str:
        return f"{super().describe()} ({self.species})"


class MicrobialSample(BiologicalSample):
    """A second, independent specialization of the same base class."""

    def __init__(
        self, sample_id: str, collection_date: str, organism: str, colony_count: int
    ) -> None:
        super().__init__(sample_id, collection_date)
        if colony_count < 0:
            raise ValueError("colony_count cannot be negative")
        self.organism = organism
        self.colony_count = colony_count

    def describe(self) -> str:
        return f"{super().describe()} ({self.organism}, {self.colony_count} CFU)"


class IndustryInheritance:
    """Demonstrates inheritance used only where a genuine polymorphic
    hierarchy exists (BiologicalSample -> PlantSample / MicrobialSample),
    kept intentionally shallow rather than deep.
    """

    @staticmethod
    def run() -> None:
        print("--- IndustryInheritance ---")
        samples: list[BiologicalSample] = [
            PlantSample("P-11", "2026-02-01", "Glycine max"),
            MicrobialSample("M-11", "2026-02-02", "B. subtilis", 842),
        ]
        for sample in samples:
            print(sample.describe())


if __name__ == "__main__":
    UniversityInheritance.run()
    InterviewInheritance.run()
    IndustryInheritance.run()
