"""Demonstrates clean-code practices through one cohesive component: a
drug-dose safety checker for a clinical decision-support system.

Focus: meaningful names, small functions, shallow control flow, named
constants instead of magic numbers, and explicit domain exceptions.
"""

from __future__ import annotations

from dataclasses import dataclass

# Named constants replace magic numbers scattered through the logic
# below, and double as inline documentation of clinical thresholds.
MINIMUM_SAFE_WEIGHT_KG = 2.0
MAXIMUM_ADULT_DOSE_MG = 800.0
MILLIGRAMS_PER_KILOGRAM_ADULT = 10.0
MILLIGRAMS_PER_KILOGRAM_PEDIATRIC = 4.0
PEDIATRIC_MAXIMUM_DOSE_MG = 120.0
PEDIATRIC_AGE_THRESHOLD_YEARS = 12


class UnsafeDoseError(ValueError):
    """Raised when a computed dose would exceed a safe clinical limit."""


class InvalidPatientDataError(ValueError):
    """Raised when patient data is missing or physiologically implausible."""


@dataclass(frozen=True, slots=True)
class Patient:
    patient_id: str
    weight_kg: float
    age_years: int


def is_pediatric(patient: Patient) -> bool:
    return patient.age_years < PEDIATRIC_AGE_THRESHOLD_YEARS


def ensure_weight_is_plausible(patient: Patient) -> None:
    if patient.weight_kg < MINIMUM_SAFE_WEIGHT_KG:
        raise InvalidPatientDataError(
            f"patient {patient.patient_id} weight {patient.weight_kg}kg "
            f"is below the minimum plausible weight"
        )


def calculate_recommended_dose_mg(patient: Patient) -> float:
    """Returns the recommended dose in milligrams for a patient.

    Each branch is a single, named clinical rule rather than nested
    conditionals, so the control flow stays flat and easy to follow.
    """
    ensure_weight_is_plausible(patient)

    if is_pediatric(patient):
        return _pediatric_dose_mg(patient)
    return _adult_dose_mg(patient)


def _pediatric_dose_mg(patient: Patient) -> float:
    dose = patient.weight_kg * MILLIGRAMS_PER_KILOGRAM_PEDIATRIC
    return min(dose, PEDIATRIC_MAXIMUM_DOSE_MG)


def _adult_dose_mg(patient: Patient) -> float:
    dose = patient.weight_kg * MILLIGRAMS_PER_KILOGRAM_ADULT
    return min(dose, MAXIMUM_ADULT_DOSE_MG)


def ensure_dose_is_safe(dose_mg: float, patient: Patient) -> None:
    absolute_ceiling = (
        PEDIATRIC_MAXIMUM_DOSE_MG if is_pediatric(patient) else MAXIMUM_ADULT_DOSE_MG
    )
    if dose_mg > absolute_ceiling:
        raise UnsafeDoseError(
            f"calculated dose {dose_mg}mg for patient {patient.patient_id} "
            f"exceeds safety ceiling of {absolute_ceiling}mg"
        )


def recommend_safe_dose_mg(patient: Patient) -> float:
    """Public entry point: computes a dose and verifies it against the
    safety ceiling before returning it. Small, readable, and each step
    delegates to a function whose name states its single responsibility.
    """
    dose_mg = calculate_recommended_dose_mg(patient)
    ensure_dose_is_safe(dose_mg, patient)
    return dose_mg


if __name__ == "__main__":
    patients = [
        Patient(patient_id="PT-01", weight_kg=70.0, age_years=45),
        Patient(patient_id="PT-02", weight_kg=18.0, age_years=6),
    ]

    for patient in patients:
        dose = recommend_safe_dose_mg(patient)
        print(f"{patient.patient_id}: recommended dose = {dose:.1f}mg")
