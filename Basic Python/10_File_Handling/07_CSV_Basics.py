"""File-handling curriculum: Python's built-in csv module."""

from __future__ import annotations

import csv
import tempfile
from pathlib import Path


class UniversityCSVBasics:
    """Teaches basic csv.reader and csv.writer usage with a plant
    phenotyping dataset."""

    @staticmethod
    def run() -> None:
        demo_dir = Path(tempfile.mkdtemp(prefix="university_csv_"))
        csv_file = demo_dir / "plant_phenotyping.csv"

        with open(csv_file, mode="w", encoding="utf-8", newline="") as file_handle:
            writer = csv.writer(file_handle)
            writer.writerow(["sample_id", "species", "height_cm", "leaf_count"])
            writer.writerow(["P001", "Wheat", "28.5", "8"])
            writer.writerow(["P002", "Rice", "31.2", "10"])

        print("[University] Wrote CSV with csv.writer.")

        with open(csv_file, mode="r", encoding="utf-8", newline="") as file_handle:
            reader = csv.reader(file_handle)
            print("[University] Read CSV with csv.reader:")
            for row in reader:
                print(row)

        csv_file.unlink()
        demo_dir.rmdir()


class InterviewCSVBasics:
    """Uses csv.DictReader and csv.DictWriter to filter, validate, and
    aggregate crop experiment data."""

    @staticmethod
    def run() -> None:
        demo_dir = Path(tempfile.mkdtemp(prefix="interview_csv_"))
        csv_file = demo_dir / "crop_experiment.csv"

        with open(csv_file, mode="w", encoding="utf-8", newline="") as file_handle:
            writer = csv.DictWriter(
                file_handle, fieldnames=["sample_id", "species", "height_cm", "leaf_count"]
            )
            writer.writeheader()
            writer.writerow(
                {"sample_id": "P001", "species": "Wheat", "height_cm": "28.5", "leaf_count": "8"}
            )
            writer.writerow(
                {"sample_id": "P002", "species": "Rice", "height_cm": "31.2", "leaf_count": "10"}
            )
            writer.writerow(
                {"sample_id": "P003", "species": "Wheat", "height_cm": "24.1", "leaf_count": "7"}
            )

        wheat_heights: list[float] = []
        with open(csv_file, mode="r", encoding="utf-8", newline="") as file_handle:
            reader = csv.DictReader(file_handle)
            for row in reader:
                if row["species"] == "Wheat":
                    try:
                        wheat_heights.append(float(row["height_cm"]))
                    except ValueError:
                        continue

        average_wheat_height = (
            sum(wheat_heights) / len(wheat_heights) if wheat_heights else 0.0
        )
        print(f"[Interview] Wheat samples: {wheat_heights}")
        print(f"[Interview] Average wheat height: {average_wheat_height:.2f} cm")

        csv_file.unlink()
        demo_dir.rmdir()


class IndustryCSVBasics:
    """A small, maintainable CSV-processing component with typed
    interfaces, header validation, and safe file handling for
    laboratory sample data."""

    _REQUIRED_FIELDS = ("sample_id", "species", "height_cm", "leaf_count")

    def __init__(self, csv_path: Path) -> None:
        self._csv_path = csv_path

    def write_records(self, records: list[dict[str, str]]) -> None:
        with open(self._csv_path, mode="w", encoding="utf-8", newline="") as file_handle:
            writer = csv.DictWriter(file_handle, fieldnames=list(self._REQUIRED_FIELDS))
            writer.writeheader()
            writer.writerows(records)

    def read_valid_records(self) -> list[dict[str, float | str]]:
        """Read and validate records, skipping rows with missing
        fields or non-numeric measurements.

        Raises:
            FileNotFoundError: if the CSV file does not exist.
            csv.Error: if the header does not match expected fields.
        """
        if not self._csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {self._csv_path}")

        valid_records: list[dict[str, float | str]] = []
        with open(self._csv_path, mode="r", encoding="utf-8", newline="") as file_handle:
            reader = csv.DictReader(file_handle)
            if reader.fieldnames is None or set(self._REQUIRED_FIELDS) - set(reader.fieldnames):
                raise csv.Error(
                    f"CSV header missing required fields: {self._REQUIRED_FIELDS}"
                )

            for row in reader:
                try:
                    height_cm = float(row["height_cm"])
                    leaf_count = int(row["leaf_count"])
                except (ValueError, TypeError):
                    continue
                valid_records.append(
                    {
                        "sample_id": row["sample_id"],
                        "species": row["species"],
                        "height_cm": height_cm,
                        "leaf_count": leaf_count,
                    }
                )
        return valid_records

    @staticmethod
    def run() -> None:
        demo_dir = Path(tempfile.mkdtemp(prefix="industry_csv_"))
        csv_path = demo_dir / "lab_samples.csv"
        processor = IndustryCSVBasics(csv_path)

        processor.write_records(
            [
                {
                    "sample_id": "P001",
                    "species": "Wheat",
                    "height_cm": "28.5",
                    "leaf_count": "8",
                },
                {
                    "sample_id": "P002",
                    "species": "Rice",
                    "height_cm": "not_a_number",
                    "leaf_count": "10",
                },
                {
                    "sample_id": "P003",
                    "species": "Maize",
                    "height_cm": "35.7",
                    "leaf_count": "12",
                },
            ]
        )

        valid_records = processor.read_valid_records()
        print(f"[Industry] Valid records after validation: {len(valid_records)}")
        for record in valid_records:
            print(f"  {record}")

        print("[Industry] Handling a missing CSV file:")
        missing_processor = IndustryCSVBasics(demo_dir / "missing.csv")
        try:
            missing_processor.read_valid_records()
        except FileNotFoundError as error:
            print(f"Caught expected error: {error}")

        csv_path.unlink()
        demo_dir.rmdir()


if __name__ == "__main__":
    UniversityCSVBasics.run()
    InterviewCSVBasics.run()
    IndustryCSVBasics.run()
