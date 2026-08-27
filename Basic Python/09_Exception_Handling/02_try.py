"""The try statement: protecting risky operations with the smallest reasonable scope."""

from __future__ import annotations

from dataclasses import dataclass


class UniversityTry:
    """Demonstrates the basic syntax and purpose of a try block."""

    @staticmethod
    def convert_measurement(raw_value: str) -> float | None:
        try:
            return float(raw_value)
        except ValueError:
            return None

    @staticmethod
    def run() -> None:
        print("--- UniversityTry ---")
        raw_leaf_lengths = ["4.2", "5.8", "not_measured", "3.1"]
        converted: list[float] = []
        for raw_value in raw_leaf_lengths:
            result = UniversityTry.convert_measurement(raw_value)
            if result is not None:
                converted.append(result)
        print(f"Converted leaf lengths: {converted}")


class InterviewTry:
    """Demonstrates keeping try blocks small around realistic parsing tasks."""

    @staticmethod
    def parse_sample_record(raw_record: str) -> dict[str, str]:
        fields = raw_record.split(",")
        try:
            sample_id, plant_height_raw = fields[0], fields[1]
        except IndexError:
            return {}
        return {"sample_id": sample_id.strip(), "plant_height_raw": plant_height_raw.strip()}

    @staticmethod
    def compute_derived_growth_rate(height_cm: float, days_elapsed: int) -> float | None:
        try:
            growth_rate = height_cm / days_elapsed
        except ZeroDivisionError:
            return None
        return round(growth_rate, 3)

    @staticmethod
    def run() -> None:
        print("--- InterviewTry ---")
        raw_records = ["S001, 14.5", "S002", "S003, 22.0"]
        parsed_records = [InterviewTry.parse_sample_record(r) for r in raw_records]
        print(f"Parsed sample records: {parsed_records}")

        growth_rate = InterviewTry.compute_derived_growth_rate(14.5, 0)
        print(f"Growth rate with zero elapsed days: {growth_rate}")

        growth_rate_valid = InterviewTry.compute_derived_growth_rate(14.5, 10)
        print(f"Valid growth rate: {growth_rate_valid}")


@dataclass(frozen=True)
class EnzymeReading:
    sample_id: str
    activity_units: float


class IndustryTry:
    """Demonstrates narrow, purposeful try blocks around a small parsing pipeline."""

    @staticmethod
    def _parse_activity_value(raw_value: str) -> float:
        try:
            activity = float(raw_value)
        except ValueError as exc:
            raise ValueError(f"Invalid enzyme activity value: {raw_value!r}") from exc
        if activity < 0:
            raise ValueError(f"Enzyme activity cannot be negative: {activity}")
        return activity

    @staticmethod
    def load_enzyme_readings(raw_rows: list[tuple[str, str]]) -> list[EnzymeReading]:
        readings: list[EnzymeReading] = []
        for sample_id, raw_activity in raw_rows:
            try:
                activity = IndustryTry._parse_activity_value(raw_activity)
            except ValueError as exc:
                print(f"Skipping row for {sample_id!r}: {exc}")
                continue
            readings.append(EnzymeReading(sample_id=sample_id, activity_units=activity))
        return readings

    @staticmethod
    def run() -> None:
        print("--- IndustryTry ---")
        raw_rows = [
            ("E001", "12.4"),
            ("E002", "not_measured"),
            ("E003", "-3.5"),
            ("E004", "8.9"),
        ]
        readings = IndustryTry.load_enzyme_readings(raw_rows)
        print(f"Accepted enzyme readings: {readings}")


if __name__ == "__main__":
    UniversityTry.run()
    InterviewTry.run()
    IndustryTry.run()
