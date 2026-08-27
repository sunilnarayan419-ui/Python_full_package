from __future__ import annotations

from typing import NotRequired, TypedDict


class UniversityTypedDict:
    """Demonstrates a basic TypedDict describing the shape of a dictionary."""

    class PlantRecord(TypedDict):
        species: str
        height_cm: float

    @staticmethod
    def describe(record: "UniversityTypedDict.PlantRecord") -> str:
        return f"{record['species']} is {record['height_cm']} cm tall"

    @staticmethod
    def run() -> None:
        record: UniversityTypedDict.PlantRecord = {"species": "Ficus lyrata", "height_cm": 45.0}
        print(UniversityTypedDict.describe(record))


class InterviewTypedDict:
    """Demonstrates TypedDict with required and optional (NotRequired)
    fields, showing how static typing catches malformed dictionary-based
    data contracts before runtime."""

    class ExperimentRecord(TypedDict):
        experiment_id: str
        sample_count: int
        notes: NotRequired[str]

    @staticmethod
    def summarize(record: "InterviewTypedDict.ExperimentRecord") -> str:
        notes = record.get("notes", "no notes provided")
        return f"{record['experiment_id']}: {record['sample_count']} samples ({notes})"

    @staticmethod
    def run() -> None:
        full_record: InterviewTypedDict.ExperimentRecord = {
            "experiment_id": "EXP-014",
            "sample_count": 32,
            "notes": "second replicate batch",
        }
        minimal_record: InterviewTypedDict.ExperimentRecord = {
            "experiment_id": "EXP-015",
            "sample_count": 18,
        }
        print(InterviewTypedDict.summarize(full_record))
        print(InterviewTypedDict.summarize(minimal_record))


class IndustryTypedDict:
    """Demonstrates TypedDict as a data contract for an ingestion pipeline,
    combined with explicit runtime validation, since TypedDict itself only
    provides static-analysis guarantees and performs no runtime checks."""

    class SequencingRunPayload(TypedDict):
        run_id: str
        instrument: str
        read_count: int
        quality_score: float
        metadata: NotRequired[dict[str, str]]

    class PayloadValidationError(Exception):
        pass

    @staticmethod
    def validate_payload(payload: dict[str, object]) -> "IndustryTypedDict.SequencingRunPayload":
        required_fields: dict[str, type] = {
            "run_id": str,
            "instrument": str,
            "read_count": int,
            "quality_score": float,
        }
        errors: list[str] = []

        for field_name, expected_type in required_fields.items():
            if field_name not in payload:
                errors.append(f"missing required field: {field_name}")
            elif expected_type is float and isinstance(payload[field_name], int):
                continue  # accept ints for float fields
            elif not isinstance(payload[field_name], expected_type):
                errors.append(f"field '{field_name}' has wrong type")

        if payload.get("read_count", 0) is not None and isinstance(payload.get("read_count"), int):
            if payload["read_count"] < 0:  # type: ignore[operator]
                errors.append("read_count cannot be negative")

        if errors:
            raise IndustryTypedDict.PayloadValidationError("; ".join(errors))

        return payload  # type: ignore[return-value]

    @staticmethod
    def run() -> None:
        raw_payload: dict[str, object] = {
            "run_id": "RUN-2024-221",
            "instrument": "NovaSeq X",
            "read_count": 45_000_000,
            "quality_score": 38.2,
            "metadata": {"operator": "lab-3"},
        }
        validated = IndustryTypedDict.validate_payload(raw_payload)
        print(validated)

        bad_payload: dict[str, object] = {
            "run_id": "RUN-2024-222",
            "instrument": "NovaSeq X",
            "read_count": -10,
            "quality_score": "not-a-number",
        }
        try:
            IndustryTypedDict.validate_payload(bad_payload)
        except IndustryTypedDict.PayloadValidationError as exc:
            print(f"caught expected error: {exc}")


if __name__ == "__main__":
    UniversityTypedDict.run()
    InterviewTypedDict.run()
    IndustryTypedDict.run()
