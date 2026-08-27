"""
05_Class_Variables.py

Concept: Class Variables
Class variables hold state shared by every instance of a class, as
opposed to instance variables which belong to one object. This file
shows correct use of class-level state and how to avoid accidental
shared mutability.
"""

from __future__ import annotations


# --------------------------------------------------------------------------- #
# University Level
# --------------------------------------------------------------------------- #
class UniversityClassVariables:
    """A simple shared class variable: the taxonomic kingdom for every
    plant sample created through this class."""

    kingdom: str = "Plantae"

    def __init__(self, species: str) -> None:
        self.species = species

    @staticmethod
    def run() -> None:
        print("--- UniversityClassVariables ---")
        plant_a = UniversityClassVariables("Rosa")
        plant_b = UniversityClassVariables("Tulipa")

        print(f"{plant_a.species} kingdom: {plant_a.kingdom}")
        print(f"{plant_b.species} kingdom: {plant_b.kingdom}")
        print(f"Shared reference? {plant_a.kingdom is plant_b.kingdom}")


# --------------------------------------------------------------------------- #
# Interview Level
# --------------------------------------------------------------------------- #
class InterviewClassVariables:
    """Demonstrates the distinction between class-level and instance-level
    state using a running count of created samples.

    Purpose: a class variable tracks how many objects have been created
    in total, while each object still keeps its own sample_id.
    """

    total_samples_created: int = 0

    def __init__(self, sample_id: str) -> None:
        if not sample_id.strip():
            raise ValueError("sample_id cannot be empty")
        self.sample_id = sample_id
        InterviewClassVariables.total_samples_created += 1

    @classmethod
    def reset_counter(cls) -> None:
        cls.total_samples_created = 0

    @staticmethod
    def run() -> None:
        print("--- InterviewClassVariables ---")
        InterviewClassVariables.reset_counter()

        InterviewClassVariables("S-01")
        InterviewClassVariables("S-02")
        InterviewClassVariables("S-03")

        print(f"Total samples created: {InterviewClassVariables.total_samples_created}")


# --------------------------------------------------------------------------- #
# Industry Level
# --------------------------------------------------------------------------- #
class IndustryClassVariables:
    """Uses class variables only where shared state is genuinely
    appropriate: a fixed reference-genome build shared by every record,
    while explicitly avoiding accidental shared mutable state (e.g. a
    shared list) by keeping per-instance collections in the instance
    namespace instead.
    """

    # Immutable shared configuration: safe to share across all instances.
    REFERENCE_GENOME_BUILD: str = "GRCh38"

    def __init__(self, sample_id: str) -> None:
        if not sample_id.strip():
            raise ValueError("sample_id cannot be empty")
        self.sample_id = sample_id
        # Deliberately an instance variable, not a class variable: each
        # record must own its own mutable list of variant calls.
        self._variant_calls: list[str] = []

    def add_variant_call(self, variant: str) -> None:
        if not variant.strip():
            raise ValueError("variant cannot be empty")
        self._variant_calls.append(variant)

    @property
    def variant_calls(self) -> tuple[str, ...]:
        return tuple(self._variant_calls)

    @classmethod
    def genome_build(cls) -> str:
        return cls.REFERENCE_GENOME_BUILD

    @staticmethod
    def run() -> None:
        print("--- IndustryClassVariables ---")
        record_a = IndustryClassVariables("S-301")
        record_b = IndustryClassVariables("S-302")

        record_a.add_variant_call("chr17:g.43094692G>A")
        record_b.add_variant_call("chr13:g.32398489del")

        print(f"Genome build (shared): {IndustryClassVariables.genome_build()}")
        print(f"record_a variants: {record_a.variant_calls}")
        print(f"record_b variants: {record_b.variant_calls}")


if __name__ == "__main__":
    UniversityClassVariables.run()
    InterviewClassVariables.run()
    IndustryClassVariables.run()
