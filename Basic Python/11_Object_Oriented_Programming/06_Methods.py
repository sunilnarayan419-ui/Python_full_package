"""
06_Methods.py

Concept: Methods
Instance methods operate on object state; class methods operate on the
class itself; static methods are utility functions grouped inside a
class for organizational reasons. This file introduces each kind
progressively.
"""

from __future__ import annotations


# --------------------------------------------------------------------------- #
# University Level
# --------------------------------------------------------------------------- #
class UniversityMethods:
    """Focuses on instance methods that read and modify object state."""

    def __init__(self, species: str, height_cm: float) -> None:
        self.species = species
        self.height_cm = height_cm

    def grow(self, amount_cm: float) -> None:
        if amount_cm < 0:
            raise ValueError("amount_cm cannot be negative")
        self.height_cm += amount_cm

    def describe(self) -> str:
        return f"{self.species}: {self.height_cm:.1f} cm"

    @staticmethod
    def run() -> None:
        print("--- UniversityMethods ---")
        plant = UniversityMethods("Helianthus annuus", 20.0)
        plant.grow(5.5)
        print(plant.describe())


# --------------------------------------------------------------------------- #
# Interview Level
# --------------------------------------------------------------------------- #
class InterviewMethods:
    """Introduces classmethod (alternate constructor) and staticmethod
    (stateless helper) alongside instance methods.
    """

    def __init__(self, sequence: str) -> None:
        self.sequence = sequence.upper()

    def gc_content(self) -> float:
        if not self.sequence:
            return 0.0
        gc_count = sum(1 for base in self.sequence if base in "GC")
        return gc_count / len(self.sequence) * 100.0

    @classmethod
    def from_fasta_line(cls, fasta_line: str) -> "InterviewMethods":
        """Alternate constructor: build directly from a raw FASTA data
        line (ignoring a leading '>' header line if present)."""
        cleaned = fasta_line.strip()
        if cleaned.startswith(">"):
            raise ValueError("expected a sequence line, not a FASTA header")
        return cls(sequence=cleaned)

    @staticmethod
    def is_valid_dna(sequence: str) -> bool:
        return set(sequence.upper()).issubset(set("ACGT"))

    @staticmethod
    def run() -> None:
        print("--- InterviewMethods ---")
        record = InterviewMethods.from_fasta_line("acgtGGCC")
        print(f"GC content: {record.gc_content():.1f}%")
        print(f"Valid DNA? {InterviewMethods.is_valid_dna('ACGTX')}")


# --------------------------------------------------------------------------- #
# Industry Level
# --------------------------------------------------------------------------- #
class IndustryMethods:
    """Demonstrates choosing between instance, class, and static methods
    based purely on responsibility, for a compound-scoring workflow.

    - Instance method: acts on this specific compound's state.
    - Class method: builds instances, tied to the class as a whole.
    - Static method: pure utility with no dependency on class or
      instance state, grouped here only for discoverability.
    """

    _scoring_version: str = "1.2"

    def __init__(self, compound_id: str, molecular_weight: float, logp: float) -> None:
        if molecular_weight < 0:
            raise ValueError("molecular_weight cannot be negative")
        self.compound_id = compound_id
        self.molecular_weight = molecular_weight
        self.logp = logp

    def drug_likeness_score(self) -> float:
        """Instance method: score depends entirely on this object's own
        molecular_weight and logp."""
        weight_score = 1.0 if self.molecular_weight <= 500.0 else 0.5
        logp_score = 1.0 if -0.4 <= self.logp <= 5.6 else 0.5
        return round((weight_score + logp_score) / 2.0, 2)

    @classmethod
    def scoring_version(cls) -> str:
        """Class method: reports metadata about the class as a whole,
        not about any single compound."""
        return cls._scoring_version

    @staticmethod
    def molar_mass_to_daltons(molar_mass_g_per_mol: float) -> float:
        """Static method: a pure unit conversion, unrelated to any
        particular class or instance state."""
        return molar_mass_g_per_mol  # g/mol and Da are numerically equal.

    @staticmethod
    def run() -> None:
        print("--- IndustryMethods ---")
        compound = IndustryMethods("CMP-77", molecular_weight=410.5, logp=3.2)

        print(f"Scoring engine version: {IndustryMethods.scoring_version()}")
        print(f"Drug-likeness score: {compound.drug_likeness_score()}")
        print(
            "410.5 g/mol equals "
            f"{IndustryMethods.molar_mass_to_daltons(410.5)} Da"
        )


if __name__ == "__main__":
    UniversityMethods.run()
    InterviewMethods.run()
    IndustryMethods.run()
