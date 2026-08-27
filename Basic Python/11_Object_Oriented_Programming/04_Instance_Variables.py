"""
04_Instance_Variables.py

Concept: Instance Variables
Instance variables hold state that belongs to one specific object. Two
objects of the same class can carry completely different instance
variable values at the same time.
"""

from __future__ import annotations


# --------------------------------------------------------------------------- #
# University Level
# --------------------------------------------------------------------------- #
class UniversityInstanceVariables:
    """Simple per-object attributes: each plant tracks its own height."""

    def __init__(self, species: str, height_cm: float) -> None:
        self.species = species
        self.height_cm = height_cm

    @staticmethod
    def run() -> None:
        print("--- UniversityInstanceVariables ---")
        plant_a = UniversityInstanceVariables("Cucumis sativus", 15.0)
        plant_b = UniversityInstanceVariables("Cucumis sativus", 22.0)

        print(f"plant_a height: {plant_a.height_cm} cm")
        print(f"plant_b height: {plant_b.height_cm} cm")


# --------------------------------------------------------------------------- #
# Interview Level
# --------------------------------------------------------------------------- #
class InterviewInstanceVariables:
    """Multiple objects with independent gene-expression state.

    Purpose: demonstrate that mutating one object's instance variables
    never affects another object's instance variables.
    """

    def __init__(self, gene_symbol: str, expression_level: float) -> None:
        if expression_level < 0:
            raise ValueError("expression_level cannot be negative")
        self.gene_symbol = gene_symbol
        self.expression_level = expression_level

    def apply_fold_change(self, fold_change: float) -> None:
        if fold_change < 0:
            raise ValueError("fold_change cannot be negative")
        self.expression_level *= fold_change

    @staticmethod
    def run() -> None:
        print("--- InterviewInstanceVariables ---")
        gene_a = InterviewInstanceVariables("GAPDH", 10.0)
        gene_b = InterviewInstanceVariables("GAPDH", 10.0)

        gene_a.apply_fold_change(2.5)

        print(f"gene_a expression: {gene_a.expression_level}")
        print(f"gene_b expression: {gene_b.expression_level}")


# --------------------------------------------------------------------------- #
# Industry Level
# --------------------------------------------------------------------------- #
class IndustryInstanceVariables:
    """Controlled state changes through appropriate methods rather than
    direct external mutation, for a molecular descriptor record.

    Purpose: show that instance variables in production code are usually
    changed through methods that preserve validity, not by external code
    reaching in and assigning directly.
    """

    def __init__(self, compound_id: str, concentration_ng_ul: float) -> None:
        self._compound_id = compound_id
        self._concentration_ng_ul = self._validate(concentration_ng_ul)
        self._dilution_events = 0

    @staticmethod
    def _validate(concentration_ng_ul: float) -> float:
        if concentration_ng_ul < 0:
            raise ValueError("concentration_ng_ul cannot be negative")
        return concentration_ng_ul

    @property
    def concentration_ng_ul(self) -> float:
        return self._concentration_ng_ul

    @property
    def dilution_events(self) -> int:
        return self._dilution_events

    def dilute(self, factor: float) -> None:
        if factor <= 0:
            raise ValueError("dilution factor must be positive")
        self._concentration_ng_ul /= factor
        self._dilution_events += 1

    @staticmethod
    def run() -> None:
        print("--- IndustryInstanceVariables ---")
        sample_a = IndustryInstanceVariables("S-201", 120.0)
        sample_b = IndustryInstanceVariables("S-202", 120.0)

        sample_a.dilute(2.0)
        sample_a.dilute(2.0)

        print(
            f"sample_a: {sample_a.concentration_ng_ul} ng/uL "
            f"after {sample_a.dilution_events} dilution(s)"
        )
        print(
            f"sample_b: {sample_b.concentration_ng_ul} ng/uL "
            f"after {sample_b.dilution_events} dilution(s)"
        )


if __name__ == "__main__":
    UniversityInstanceVariables.run()
    InterviewInstanceVariables.run()
    IndustryInstanceVariables.run()
