"""
09_Encapsulation.py

Concept: Encapsulation
Encapsulation protects an object's internal state so that it cannot
easily become invalid. This file progresses from public attributes, to
protected/name-mangled attributes, to properties that enforce
invariants on every write.
"""

from __future__ import annotations


# --------------------------------------------------------------------------- #
# University Level
# --------------------------------------------------------------------------- #
class UniversityEncapsulation:
    """Demonstrates the basic vocabulary of encapsulation:
    public, protected-by-convention, and name-mangled attributes.
    """

    def __init__(self, species: str, internal_note: str, secret_code: str) -> None:
        self.species = species              # public: freely accessible
        self._internal_note = internal_note  # protected by convention only
        self.__secret_code = secret_code     # name-mangled, harder to access

    def reveal_secret_code(self) -> str:
        return self.__secret_code

    @staticmethod
    def run() -> None:
        print("--- UniversityEncapsulation ---")
        sample = UniversityEncapsulation("Vitis vinifera", "handle with care", "X-42")

        print(f"Public: {sample.species}")
        print(f"Protected (by convention): {sample._internal_note}")
        print(f"Name-mangled access via method: {sample.reveal_secret_code()}")
        # Direct external access still possible via the mangled name,
        # but it signals clear intent that this is not part of the API:
        print(f"Name-mangled raw attribute: {sample._UniversityEncapsulation__secret_code}")


# --------------------------------------------------------------------------- #
# Interview Level
# --------------------------------------------------------------------------- #
class InterviewEncapsulation:
    """Uses a property to validate a biological measurement on every
    assignment, not just at construction time."""

    def __init__(self, height_cm: float) -> None:
        self.height_cm = height_cm  # goes through the property setter

    @property
    def height_cm(self) -> float:
        return self._height_cm

    @height_cm.setter
    def height_cm(self, value: float) -> None:
        if value < 0:
            raise ValueError("height_cm cannot be negative")
        self._height_cm = value

    @staticmethod
    def run() -> None:
        print("--- InterviewEncapsulation ---")
        plant = InterviewEncapsulation(height_cm=18.5)
        print(f"Initial height: {plant.height_cm} cm")

        plant.height_cm = 24.0
        print(f"Updated height: {plant.height_cm} cm")

        try:
            plant.height_cm = -3.0
        except ValueError as error:
            print(f"Rejected invalid update: {error}")


# --------------------------------------------------------------------------- #
# Industry Level
# --------------------------------------------------------------------------- #
class IndustryEncapsulation:
    """A domain object whose internal state cannot easily become invalid:
    a titration/concentration record where volume and concentration must
    always stay non-negative, and total mass is derived rather than
    stored redundantly.

    Only properties that need validation or derivation get a `@property`;
    trivial fields remain plain attributes to avoid pointless boilerplate.
    """

    def __init__(self, sample_id: str, volume_ml: float, concentration_ng_ul: float) -> None:
        self.sample_id = sample_id  # plain attribute: no invariant to protect
        self._volume_ml = self._require_non_negative(volume_ml, "volume_ml")
        self._concentration_ng_ul = self._require_non_negative(
            concentration_ng_ul, "concentration_ng_ul"
        )

    @staticmethod
    def _require_non_negative(value: float, field_name: str) -> float:
        if value < 0:
            raise ValueError(f"{field_name} cannot be negative")
        return value

    @property
    def volume_ml(self) -> float:
        return self._volume_ml

    @volume_ml.setter
    def volume_ml(self, value: float) -> None:
        self._volume_ml = self._require_non_negative(value, "volume_ml")

    @property
    def concentration_ng_ul(self) -> float:
        return self._concentration_ng_ul

    @concentration_ng_ul.setter
    def concentration_ng_ul(self, value: float) -> None:
        self._concentration_ng_ul = self._require_non_negative(value, "concentration_ng_ul")

    @property
    def total_mass_ng(self) -> float:
        """Derived value: never stored, so it can never drift out of sync."""
        return self._volume_ml * 1000.0 * self._concentration_ng_ul / 1000.0

    @staticmethod
    def run() -> None:
        print("--- IndustryEncapsulation ---")
        record = IndustryEncapsulation(
            sample_id="S-501", volume_ml=0.05, concentration_ng_ul=120.0
        )
        print(f"Total mass: {record.total_mass_ng:.2f} ng")

        record.concentration_ng_ul = 90.0
        print(f"Recomputed total mass: {record.total_mass_ng:.2f} ng")

        try:
            record.volume_ml = -0.01
        except ValueError as error:
            print(f"Rejected invalid update: {error}")


if __name__ == "__main__":
    UniversityEncapsulation.run()
    InterviewEncapsulation.run()
    IndustryEncapsulation.run()
