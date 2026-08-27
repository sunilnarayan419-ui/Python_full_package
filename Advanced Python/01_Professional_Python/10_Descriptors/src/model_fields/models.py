"""Domain model composed from validated and cached descriptor fields."""
from __future__ import annotations

from .descriptors import BoundedFloat, CachedProperty, ValidatedString


class PatientRecord:
    medical_record_number = ValidatedString(pattern=r"MRN-\d{6}")
    systolic_bp_mmhg = BoundedFloat(minimum=40.0, maximum=300.0)
    diastolic_bp_mmhg = BoundedFloat(minimum=20.0, maximum=200.0)

    def __init__(self, medical_record_number: str, systolic_bp_mmhg: float, diastolic_bp_mmhg: float) -> None:
        self.medical_record_number = medical_record_number
        self.systolic_bp_mmhg = systolic_bp_mmhg
        self.diastolic_bp_mmhg = diastolic_bp_mmhg

    @CachedProperty
    def pulse_pressure(self) -> float:
        """Expensive-in-spirit derived metric, computed once and cached."""
        return self.systolic_bp_mmhg - self.diastolic_bp_mmhg
