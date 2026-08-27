"""The else clause: running success-path logic only when the try block succeeds."""

from __future__ import annotations

from dataclasses import dataclass


class UniversityElse:
    """Demonstrates the basic separation try/except/else provides."""

    @staticmethod
    def process_plant_height(raw_value: str) -> None:
        try:
            height_cm = float(raw_value)
        except ValueError:
            print(f"Could not parse height value: {raw_value!r}")
        else:
            print(f"Parsed plant height successfully: {height_cm} cm")

    @staticmethod
    def run() -> None:
        print("--- UniversityElse ---")
        UniversityElse.process_plant_height("18.4")
        UniversityElse.process_plant_height("tall")


class InterviewElse:
    """Demonstrates using else to separate risky work from successful-result processing."""

    @staticmethod
    def load_and_summarize_leaf_counts(raw_counts: list[str]) -> None:
        try:
            leaf_counts = [int(value) for value in raw_counts]
        except ValueError as exc:
            print(f"Failed to parse leaf counts: {exc}")
        else:
            total = sum(leaf_counts)
            average = total / len(leaf_counts)
            print(f"Leaf counts parsed: {leaf_counts}")
            print(f"Total leaves: {total}, average per plant: {average:.2f}")

    @staticmethod
    def run() -> None:
        print("--- InterviewElse ---")
        InterviewElse.load_and_summarize_leaf_counts(["4", "7", "9", "3"])
        InterviewElse.load_and_summarize_leaf_counts(["4", "seven", "9"])


@dataclass(frozen=True)
class ExperimentRecord:
    sample_id: str
    ph_value: float
    temperature_c: float


class IndustryElse:
    """Demonstrates else as a clean boundary between validation and downstream processing."""

    @staticmethod
    def _parse_record(raw: dict[str, str]) -> ExperimentRecord:
        sample_id = raw["sample_id"]
        ph_value = float(raw["ph_value"])
        temperature_c = float(raw["temperature_c"])
        if not 0.0 <= ph_value <= 14.0:
            raise ValueError(f"pH out of range for {sample_id}: {ph_value}")
        return ExperimentRecord(sample_id, ph_value, temperature_c)

    @staticmethod
    def process_experiment_row(raw: dict[str, str]) -> ExperimentRecord | None:
        try:
            record = IndustryElse._parse_record(raw)
        except KeyError as exc:
            print(f"Rejected row, missing field {exc} in {raw}")
            return None
        except ValueError as exc:
            print(f"Rejected row: {exc}")
            return None
        else:
            print(f"Accepted experiment record: {record}")
            return record

    @staticmethod
    def run() -> None:
        print("--- IndustryElse ---")
        raw_rows = [
            {"sample_id": "R001", "ph_value": "6.8", "temperature_c": "23.0"},
            {"sample_id": "R002", "ph_value": "15.2", "temperature_c": "21.5"},
            {"sample_id": "R003", "ph_value": "not_numeric", "temperature_c": "20.0"},
        ]
        accepted = [
            record
            for raw in raw_rows
            if (record := IndustryElse.process_experiment_row(raw)) is not None
        ]
        print(f"Total accepted records: {len(accepted)}")


if __name__ == "__main__":
    UniversityElse.run()
    InterviewElse.run()
    IndustryElse.run()
