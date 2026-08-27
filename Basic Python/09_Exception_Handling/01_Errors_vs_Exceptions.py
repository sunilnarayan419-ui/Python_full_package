"""Errors vs Exceptions: syntax errors, runtime errors, logical errors, and exceptions."""

from __future__ import annotations

import ast
from dataclasses import dataclass


class UniversityErrorsVsExceptions:
    """Demonstrates the fundamental distinction between error categories."""

    @staticmethod
    def check_syntax(source_code: str) -> bool:
        try:
            ast.parse(source_code)
        except SyntaxError as exc:
            print(f"Syntax error detected: {exc.msg} (line {exc.lineno})")
            return False
        return True

    @staticmethod
    def demonstrate_runtime_error() -> None:
        plant_heights_cm: list[float] = [12.5, 15.0, 9.8]
        index = 5
        try:
            value = plant_heights_cm[index]
            print(f"Height at index {index}: {value}")
        except IndexError as exc:
            print(f"Runtime error caught: {exc}")

    @staticmethod
    def demonstrate_logical_error() -> None:
        leaf_counts: list[int] = [4, 7, 2, 9]
        total = sum(leaf_counts)
        incorrect_average = total / (len(leaf_counts) + 1)
        correct_average = total / len(leaf_counts)
        print(f"Incorrect average (logical error): {incorrect_average:.2f}")
        print(f"Correct average: {correct_average:.2f}")

    @staticmethod
    def demonstrate_exception() -> None:
        raw_measurement = "not_a_number"
        try:
            float(raw_measurement)
        except ValueError as exc:
            print(f"Exception caught during conversion: {exc}")

    @staticmethod
    def run() -> None:
        print("--- UniversityErrorsVsExceptions ---")
        valid_source = "plant_height = 12.5"
        invalid_source = "plant_height = = 12.5"
        UniversityErrorsVsExceptions.check_syntax(valid_source)
        UniversityErrorsVsExceptions.check_syntax(invalid_source)
        UniversityErrorsVsExceptions.demonstrate_runtime_error()
        UniversityErrorsVsExceptions.demonstrate_logical_error()
        UniversityErrorsVsExceptions.demonstrate_exception()


class InterviewErrorsVsExceptions:
    """Distinguishes error categories through realistic biological data handling."""

    @staticmethod
    def parse_gene_expression_row(row: dict[str, str]) -> tuple[str, float] | None:
        try:
            gene_id = row["gene_id"]
            expression_level = float(row["expression_level"])
        except KeyError as exc:
            print(f"Malformed record, missing field: {exc}")
            return None
        except ValueError as exc:
            print(f"Malformed record, invalid numeric value: {exc}")
            return None
        return gene_id, expression_level

    @staticmethod
    def detect_logical_error_in_normalization(values: list[float]) -> list[float]:
        maximum = max(values)
        if maximum == 0:
            return [0.0 for _ in values]
        return [round(v / maximum, 4) for v in values]

    @staticmethod
    def run() -> None:
        print("--- InterviewErrorsVsExceptions ---")
        records = [
            {"gene_id": "GAPDH", "expression_level": "8.2"},
            {"gene_id": "ACTB", "expression_level": "not_available"},
            {"expression_level": "5.1"},
        ]
        parsed: list[tuple[str, float]] = []
        for row in records:
            result = InterviewErrorsVsExceptions.parse_gene_expression_row(row)
            if result is not None:
                parsed.append(result)
        print(f"Successfully parsed records: {parsed}")

        normalized = InterviewErrorsVsExceptions.detect_logical_error_in_normalization(
            [2.0, 4.0, 8.0]
        )
        print(f"Normalized expression levels: {normalized}")


@dataclass(frozen=True)
class SampleValidationOutcome:
    is_valid: bool
    reason: str | None = None


class DefectDetectedError(RuntimeError):
    """Raised when internal program state violates an invariant (a programmer defect)."""


class IndustryErrorsVsExceptions:
    """Separates invalid input, expected operational failure, and programmer defects."""

    @staticmethod
    def validate_sample_ph(ph_value: float) -> SampleValidationOutcome:
        if not isinstance(ph_value, (int, float)):
            return SampleValidationOutcome(False, "pH value must be numeric")
        if not 0.0 <= ph_value <= 14.0:
            return SampleValidationOutcome(False, "pH value out of chemical range")
        return SampleValidationOutcome(True)

    @staticmethod
    def read_sample_measurement(source: dict[str, float], key: str) -> float:
        try:
            return source[key]
        except KeyError as exc:
            raise LookupError(f"Expected operational failure: '{key}' not recorded") from exc

    @staticmethod
    def compute_buffer_ratio(numerator: float, denominator: float) -> float:
        if denominator == 0:
            raise DefectDetectedError(
                "Programmer defect: buffer ratio requested with zero denominator"
            )
        return numerator / denominator

    @staticmethod
    def run() -> None:
        print("--- IndustryErrorsVsExceptions ---")

        invalid_input_outcome = IndustryErrorsVsExceptions.validate_sample_ph(15.2)
        print(f"Invalid input case: {invalid_input_outcome}")

        readings = {"ph": 6.8, "temperature_c": 22.5}
        try:
            IndustryErrorsVsExceptions.read_sample_measurement(readings, "conductivity")
        except LookupError as exc:
            print(f"Expected operational failure handled: {exc}")

        try:
            IndustryErrorsVsExceptions.compute_buffer_ratio(10.0, 0.0)
        except DefectDetectedError as exc:
            print(f"Programmer defect surfaced clearly: {exc}")

        valid_outcome = IndustryErrorsVsExceptions.validate_sample_ph(readings["ph"])
        print(f"Valid input case: {valid_outcome}")


if __name__ == "__main__":
    UniversityErrorsVsExceptions.run()
    InterviewErrorsVsExceptions.run()
    IndustryErrorsVsExceptions.run()
