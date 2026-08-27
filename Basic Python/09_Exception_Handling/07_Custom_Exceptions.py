"""Custom exceptions: domain-specific failures with useful contextual information."""

from __future__ import annotations

from dataclasses import dataclass


class InvalidSampleError(Exception):
    """Raised when a biological sample is invalid."""


class UniversitySample:
    """Minimal domain object used to demonstrate a custom exception."""

    def __init__(self, sample_id: str, weight_grams: float) -> None:
        if weight_grams <= 0:
            raise InvalidSampleError(
                f"Sample {sample_id!r} has non-positive weight: {weight_grams}g"
            )
        self.sample_id = sample_id
        self.weight_grams = weight_grams


class UniversityCustomExceptions:
    """Demonstrates defining and raising a single custom exception."""

    @staticmethod
    def run() -> None:
        print("--- UniversityCustomExceptions ---")
        for sample_id, weight in (("S001", 4.2), ("S002", -1.0)):
            try:
                sample = UniversitySample(sample_id, weight)
                print(f"Created sample: {sample.sample_id}, {sample.weight_grams}g")
            except InvalidSampleError as exc:
                print(f"Sample rejected: {exc}")


class InvalidSequenceError(Exception):
    """Raised when a biological sequence fails domain validation."""

    def __init__(self, sequence: str, reason: str) -> None:
        super().__init__(f"Invalid sequence {sequence!r}: {reason}")
        self.sequence = sequence
        self.reason = reason


class InterviewCustomExceptions:
    """Demonstrates a custom exception that carries structured contextual data."""

    VALID_AMINO_ACIDS = frozenset("ACDEFGHIKLMNPQRSTVWY")

    @staticmethod
    def validate_protein_sequence(sequence: str) -> str:
        if not sequence:
            raise InvalidSequenceError(sequence, "sequence is empty")
        invalid_residues = set(sequence.upper()) - InterviewCustomExceptions.VALID_AMINO_ACIDS
        if invalid_residues:
            raise InvalidSequenceError(
                sequence, f"contains invalid residues {sorted(invalid_residues)}"
            )
        return sequence.upper()

    @staticmethod
    def run() -> None:
        print("--- InterviewCustomExceptions ---")
        for sequence in ("MKVLAT", "MKVL@T", ""):
            try:
                validated = InterviewCustomExceptions.validate_protein_sequence(sequence)
                print(f"Valid protein sequence: {validated}")
            except InvalidSequenceError as exc:
                print(f"Rejected sequence ({exc.reason}): {exc.sequence!r}")


class LaboratoryError(Exception):
    """Base class for laboratory-pipeline domain errors."""


class ExperimentConfigurationError(LaboratoryError):
    """Raised when an experiment configuration is missing or malformed."""


class MeasurementValidationError(LaboratoryError):
    """Raised when a recorded measurement violates domain constraints."""

    def __init__(self, sample_id: str, field_name: str, value: object) -> None:
        super().__init__(
            f"Invalid {field_name} for sample {sample_id!r}: {value!r}"
        )
        self.sample_id = sample_id
        self.field_name = field_name
        self.value = value


@dataclass(frozen=True)
class ValidatedMeasurement:
    sample_id: str
    ph_value: float
    temperature_c: float


class IndustryCustomExceptions:
    """Demonstrates a small, purposeful exception hierarchy for a laboratory pipeline."""

    @staticmethod
    def _require_field(raw: dict[str, str], field_name: str) -> str:
        try:
            return raw[field_name]
        except KeyError as exc:
            raise ExperimentConfigurationError(
                f"Missing required field {field_name!r} in experiment record"
            ) from exc

    @staticmethod
    def validate_measurement(raw: dict[str, str]) -> ValidatedMeasurement:
        sample_id = IndustryCustomExceptions._require_field(raw, "sample_id")
        raw_ph = IndustryCustomExceptions._require_field(raw, "ph_value")
        raw_temp = IndustryCustomExceptions._require_field(raw, "temperature_c")

        try:
            ph_value = float(raw_ph)
        except ValueError as exc:
            raise MeasurementValidationError(sample_id, "ph_value", raw_ph) from exc

        try:
            temperature_c = float(raw_temp)
        except ValueError as exc:
            raise MeasurementValidationError(sample_id, "temperature_c", raw_temp) from exc

        if not 0.0 <= ph_value <= 14.0:
            raise MeasurementValidationError(sample_id, "ph_value", ph_value)

        return ValidatedMeasurement(sample_id, ph_value, temperature_c)

    @staticmethod
    def run() -> None:
        print("--- IndustryCustomExceptions ---")
        raw_records = [
            {"sample_id": "L001", "ph_value": "6.5", "temperature_c": "21.0"},
            {"sample_id": "L002", "ph_value": "15.9", "temperature_c": "20.0"},
            {"sample_id": "L003", "ph_value": "not_numeric", "temperature_c": "19.5"},
            {"ph_value": "6.9", "temperature_c": "22.0"},
        ]
        validated_records: list[ValidatedMeasurement] = []
        for raw in raw_records:
            try:
                measurement = IndustryCustomExceptions.validate_measurement(raw)
            except MeasurementValidationError as exc:
                print(f"Measurement rejected: {exc}")
                continue
            except ExperimentConfigurationError as exc:
                print(f"Configuration rejected: {exc}")
                continue
            validated_records.append(measurement)
        print(f"Accepted measurements: {validated_records}")


if __name__ == "__main__":
    UniversityCustomExceptions.run()
    InterviewCustomExceptions.run()
    IndustryCustomExceptions.run()
