"""The except clause: specific exception types, ordering, and safe recovery."""

from __future__ import annotations

from dataclasses import dataclass


class UniversityExcept:
    """Demonstrates matching except clauses to specific exception types."""

    @staticmethod
    def divide_dosage(total_mg: float, num_doses: int) -> float | None:
        try:
            return total_mg / num_doses
        except ZeroDivisionError:
            print("Cannot split dosage into zero doses.")
            return None
        except TypeError:
            print("Dosage values must be numeric.")
            return None

    @staticmethod
    def run() -> None:
        print("--- UniversityExcept ---")
        print(UniversityExcept.divide_dosage(500.0, 5))
        print(UniversityExcept.divide_dosage(500.0, 0))


class InterviewExcept:
    """Demonstrates multiple except blocks and exception ordering with realistic data."""

    VALID_BASES = frozenset("ACGT")

    @staticmethod
    def validate_dna_sequence(sequence: str) -> str:
        try:
            if not sequence:
                raise ValueError("Sequence cannot be empty")
            invalid_bases = set(sequence.upper()) - InterviewExcept.VALID_BASES
            if invalid_bases:
                raise ValueError(f"Invalid bases found: {sorted(invalid_bases)}")
        except ValueError as exc:
            print(f"Sequence rejected: {exc}")
            return ""
        return sequence.upper()

    @staticmethod
    def extract_experiment_field(record: dict[str, object], key: str) -> object:
        try:
            return record[key]
        except KeyError:
            print(f"Missing expected field: {key!r}")
            return None
        except TypeError:
            print("Record must be a dictionary-like structure.")
            return None

    @staticmethod
    def run() -> None:
        print("--- InterviewExcept ---")
        print(InterviewExcept.validate_dna_sequence("ACGTACGT"))
        print(InterviewExcept.validate_dna_sequence("ACGXACGT"))
        print(InterviewExcept.validate_dna_sequence(""))

        record: dict[str, object] = {"sample_id": "S010", "temperature_c": 24.5}
        print(InterviewExcept.extract_experiment_field(record, "sample_id"))
        print(InterviewExcept.extract_experiment_field(record, "humidity"))


@dataclass(frozen=True)
class CompoundRecord:
    compound_id: str
    molecular_weight: float


class InvalidCompoundDataError(ValueError):
    """Raised when compound data fails domain-specific validation."""


class IndustryExcept:
    """Demonstrates why blanket 'except Exception' handling is avoided in production code."""

    @staticmethod
    def parse_compound_record(raw: dict[str, str]) -> CompoundRecord:
        try:
            compound_id = raw["compound_id"]
        except KeyError as exc:
            raise InvalidCompoundDataError("Missing compound_id in record") from exc

        try:
            molecular_weight = float(raw["molecular_weight"])
        except KeyError as exc:
            raise InvalidCompoundDataError(
                f"Missing molecular_weight for {compound_id}"
            ) from exc
        except ValueError as exc:
            raise InvalidCompoundDataError(
                f"Non-numeric molecular_weight for {compound_id}"
            ) from exc

        if molecular_weight <= 0:
            raise InvalidCompoundDataError(
                f"Molecular weight must be positive for {compound_id}"
            )

        return CompoundRecord(compound_id=compound_id, molecular_weight=molecular_weight)

    @staticmethod
    def load_compounds(raw_records: list[dict[str, str]]) -> list[CompoundRecord]:
        compounds: list[CompoundRecord] = []
        for raw in raw_records:
            try:
                compound = IndustryExcept.parse_compound_record(raw)
            except InvalidCompoundDataError as exc:
                print(f"Rejected compound record: {exc}")
                continue
            compounds.append(compound)
        return compounds

    @staticmethod
    def run() -> None:
        print("--- IndustryExcept ---")
        raw_records = [
            {"compound_id": "C001", "molecular_weight": "180.16"},
            {"compound_id": "C002", "molecular_weight": "not_a_number"},
            {"compound_id": "C003", "molecular_weight": "-12.0"},
            {"molecular_weight": "58.44"},
        ]
        compounds = IndustryExcept.load_compounds(raw_records)
        print(f"Accepted compounds: {compounds}")


if __name__ == "__main__":
    UniversityExcept.run()
    InterviewExcept.run()
    IndustryExcept.run()
