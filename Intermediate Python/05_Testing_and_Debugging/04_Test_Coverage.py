"""Demonstrates meaningful test coverage for a dosage-calculation service.

Coverage is treated as a signal (which branches/paths ran) rather than
proof of correctness. Run with:

    coverage run -m unittest 04_Test_Coverage.py
    coverage report -m
"""

from __future__ import annotations

import unittest
from dataclasses import dataclass


class DosageCalculationError(ValueError):
    """Raised when a drug dosage cannot be safely calculated."""


@dataclass(frozen=True, slots=True)
class Patient:
    patient_id: str
    weight_kg: float
    is_pediatric: bool


class DosageCalculator:
    """Computes weight-based drug dosage with age-specific safety limits.

    Every branch below corresponds to a distinct clinical rule; each
    must be covered independently because branch coverage (not just
    line coverage) is what reveals whether the pediatric cap, the
    weight floor, and the failure paths were actually exercised.
    """

    ADULT_MG_PER_KG = 5.0
    PEDIATRIC_MG_PER_KG = 2.0
    PEDIATRIC_MAX_DOSE_MG = 40.0
    MIN_WEIGHT_KG = 2.0

    def calculate_dose_mg(self, patient: Patient) -> float:
        if patient.weight_kg < self.MIN_WEIGHT_KG:
            raise DosageCalculationError(
                f"weight {patient.weight_kg}kg below safe calculation threshold"
            )

        if patient.is_pediatric:
            dose = patient.weight_kg * self.PEDIATRIC_MG_PER_KG
            if dose > self.PEDIATRIC_MAX_DOSE_MG:
                # Branch: pediatric dose capped for safety.
                return self.PEDIATRIC_MAX_DOSE_MG
            # Branch: pediatric dose under the cap.
            return dose

        # Branch: adult dosing path.
        return patient.weight_kg * self.ADULT_MG_PER_KG


class TestDosageCalculatorCoverage(unittest.TestCase):
    """Covers each distinct branch of DosageCalculator.calculate_dose_mg.

    Intentionally left uncovered for this demonstration: the exact
    boundary where pediatric dose equals PEDIATRIC_MAX_DOSE_MG exactly
    (== vs >). A coverage report against this suite will show that
    boundary as untested, which is the point -- coverage tooling
    surfaces the gap; it does not close it automatically.
    """

    def setUp(self) -> None:
        self.calculator = DosageCalculator()

    def test_weight_below_threshold_raises(self) -> None:
        patient = Patient(patient_id="P-001", weight_kg=1.5, is_pediatric=False)
        with self.assertRaises(DosageCalculationError):
            self.calculator.calculate_dose_mg(patient)

    def test_adult_dose_uses_adult_rate(self) -> None:
        patient = Patient(patient_id="P-002", weight_kg=70.0, is_pediatric=False)
        dose = self.calculator.calculate_dose_mg(patient)
        self.assertAlmostEqual(dose, 350.0, places=6)

    def test_pediatric_dose_under_cap(self) -> None:
        patient = Patient(patient_id="P-003", weight_kg=10.0, is_pediatric=True)
        dose = self.calculator.calculate_dose_mg(patient)
        self.assertAlmostEqual(dose, 20.0, places=6)

    def test_pediatric_dose_exceeding_cap_is_clamped(self) -> None:
        patient = Patient(patient_id="P-004", weight_kg=30.0, is_pediatric=True)
        dose = self.calculator.calculate_dose_mg(patient)
        self.assertAlmostEqual(dose, DosageCalculator.PEDIATRIC_MAX_DOSE_MG, places=6)


if __name__ == "__main__":
    unittest.main()
