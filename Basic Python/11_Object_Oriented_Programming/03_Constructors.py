"""
03_Constructors.py

Concept: Constructors
The `__init__` method initializes a new object's state. This file shows
how constructors move from simple assignment to establishing meaningful,
validated invariants.
"""

from __future__ import annotations


# --------------------------------------------------------------------------- #
# University Level
# --------------------------------------------------------------------------- #
class UniversityConstructors:
    """Initializes a plant sample with basic attributes."""

    def __init__(self, species: str, height_cm: float) -> None:
        self.species = species
        self.height_cm = height_cm

    @staticmethod
    def run() -> None:
        print("--- UniversityConstructors ---")
        sample = UniversityConstructors(species="Triticum aestivum", height_cm=45.0)
        print(f"Created {sample.species} at {sample.height_cm} cm")


# --------------------------------------------------------------------------- #
# Interview Level
# --------------------------------------------------------------------------- #
class InterviewConstructors:
    """Initializes a biological record with validation.

    Purpose: demonstrate that a constructor's job includes rejecting
    invalid initial state, not just assigning attributes.
    """

    def __init__(self, sample_id: str, sequence: str) -> None:
        self.sample_id = self._validate_sample_id(sample_id)
        self.sequence = self._validate_sequence(sequence)

    @staticmethod
    def _validate_sample_id(sample_id: str) -> str:
        if not sample_id.strip():
            raise ValueError("sample_id cannot be empty")
        return sample_id

    @staticmethod
    def _validate_sequence(sequence: str) -> str:
        allowed = set("ACGT")
        cleaned = sequence.upper()
        if not cleaned:
            raise ValueError("sequence cannot be empty")
        if not set(cleaned).issubset(allowed):
            raise ValueError("sequence contains unsupported symbols")
        return cleaned

    @staticmethod
    def run() -> None:
        print("--- InterviewConstructors ---")
        record = InterviewConstructors(sample_id="DNA-01", sequence="acgtACGT")
        print(f"{record.sample_id}: {record.sequence}")

        try:
            InterviewConstructors(sample_id="DNA-02", sequence="ACGX")
        except ValueError as error:
            print(f"Rejected invalid sequence: {error}")


# --------------------------------------------------------------------------- #
# Industry Level
# --------------------------------------------------------------------------- #
class IndustryConstructors:
    """A domain object whose constructor establishes meaningful invariants
    for a drug-candidate compound record, without embedding business logic
    beyond validation.

    Purpose: show that a well-designed constructor guarantees every
    instance is valid the moment it exists, which simplifies every method
    that uses the object afterward.
    """

    def __init__(
        self,
        compound_id: str,
        molecular_weight: float,
        logp: float,
    ) -> None:
        self._compound_id = self._require_non_empty(compound_id, "compound_id")
        self._molecular_weight = self._require_non_negative(
            molecular_weight, "molecular_weight"
        )
        self._logp = logp  # logP may legitimately be negative; no lower bound.

    @staticmethod
    def _require_non_empty(value: str, field_name: str) -> str:
        if not value.strip():
            raise ValueError(f"{field_name} cannot be empty")
        return value

    @staticmethod
    def _require_non_negative(value: float, field_name: str) -> float:
        if value < 0:
            raise ValueError(f"{field_name} cannot be negative")
        return value

    @property
    def compound_id(self) -> str:
        return self._compound_id

    @property
    def molecular_weight(self) -> float:
        return self._molecular_weight

    @property
    def logp(self) -> float:
        return self._logp

    def passes_lipinski_weight_rule(self) -> bool:
        """Rule of Five weight check: molecular weight <= 500 Da."""
        return self._molecular_weight <= 500.0

    @staticmethod
    def run() -> None:
        print("--- IndustryConstructors ---")
        compound = IndustryConstructors(
            compound_id="CMP-1029", molecular_weight=342.4, logp=2.1
        )
        print(
            f"{compound.compound_id}: MW={compound.molecular_weight}, "
            f"logP={compound.logp}, Lipinski-weight-ok="
            f"{compound.passes_lipinski_weight_rule()}"
        )

        try:
            IndustryConstructors(compound_id="", molecular_weight=100.0, logp=1.0)
        except ValueError as error:
            print(f"Rejected invalid compound: {error}")


if __name__ == "__main__":
    UniversityConstructors.run()
    InterviewConstructors.run()
    IndustryConstructors.run()
