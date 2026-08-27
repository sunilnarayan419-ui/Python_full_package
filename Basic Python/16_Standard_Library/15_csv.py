"""Demonstrates the csv module for structured experimental data import/export."""

import csv
import tempfile
from pathlib import Path


class UniversityCsv:
    """Introduces basic CSV reading and writing using plant sample records."""

    def write_records(self, file_path: Path, records: list[list[str]]) -> None:
        with file_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["sample_id", "species", "height_cm"])
            writer.writerows(records)

    def read_records(self, file_path: Path) -> list[list[str]]:
        with file_path.open("r", newline="", encoding="utf-8") as handle:
            reader = csv.reader(handle)
            return list(reader)

    @staticmethod
    def run() -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = Path(tmp_dir) / "samples.csv"
            demo = UniversityCsv()

            records = [["PL-001", "Arabidopsis", "24.5"], ["PL-002", "Zea mays", "88.0"]]
            demo.write_records(file_path, records)

            read_back = demo.read_records(file_path)
            print(f"Read back CSV rows: {read_back}")


class InterviewCsv:
    """Solves a structured CSV-processing problem using DictReader, with edge cases."""

    def load_valid_records(self, file_path: Path, required_fields: list[str]) -> list[dict[str, str]]:
        """Load CSV rows as dicts, skipping rows missing required data.

        Rows with a blank value for any required field are skipped rather than
        causing the entire load to fail, since a single malformed row is common
        in real laboratory data exports.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"CSV file not found: {file_path}")

        valid_records: list[dict[str, str]] = []
        with file_path.open("r", newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                if all(row.get(field) for field in required_fields):
                    valid_records.append(row)
        return valid_records

    @staticmethod
    def run() -> None:
        solver = InterviewCsv()

        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = Path(tmp_dir) / "expression.csv"
            content = (
                "sample_id,species,height_cm,leaf_count,expression_level\n"
                "PL-001,Arabidopsis,24.5,14,4.2\n"
                "PL-002,,88.0,22,3.9\n"  # missing species: should be skipped
                "PL-003,Oryza sativa,31.0,18,5.1\n"
            )
            file_path.write_text(content, encoding="utf-8")

            # Test case 1: normal load with a malformed row present
            valid_records = solver.load_valid_records(file_path, required_fields=["sample_id", "species"])
            print(f"Valid records loaded: {len(valid_records)}")
            for record in valid_records:
                print(record)

            # Test case 2: edge case, missing file
            try:
                solver.load_valid_records(Path(tmp_dir) / "missing.csv", ["sample_id"])
            except FileNotFoundError as error:
                print(f"Handled missing file: {error}")


class IndustryCsv:
    """Reusable scientific-data import/export workflow using DictReader/DictWriter."""

    FIELDNAMES = ["sample_id", "species", "height_cm", "leaf_count", "expression_level"]

    def export_records(self, file_path: Path, records: list[dict[str, str]]) -> Path:
        """Export structured experimental records to CSV with a fixed schema."""
        with file_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=self.FIELDNAMES)
            writer.writeheader()
            writer.writerows(records)
        return file_path

    def import_records(self, file_path: Path) -> list[dict[str, str]]:
        """Import structured experimental records from CSV, validating the schema."""
        if not file_path.exists():
            raise FileNotFoundError(f"CSV file not found: {file_path}")

        with file_path.open("r", newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != self.FIELDNAMES:
                raise ValueError(
                    f"Unexpected CSV schema. Expected {self.FIELDNAMES}, got {reader.fieldnames}."
                )
            return list(reader)

    @staticmethod
    def run() -> None:
        manager = IndustryCsv()

        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = Path(tmp_dir) / "experiment_export.csv"

            records = [
                {
                    "sample_id": "PL-010",
                    "species": "Arabidopsis",
                    "height_cm": "26.1",
                    "leaf_count": "15",
                    "expression_level": "4.4",
                },
                {
                    "sample_id": "PL-011",
                    "species": "Zea mays",
                    "height_cm": "90.2",
                    "leaf_count": "24",
                    "expression_level": "3.8",
                },
            ]

            manager.export_records(file_path, records)
            print(f"Exported {len(records)} records to {file_path.name}")

            imported = manager.import_records(file_path)
            print(f"Imported records: {imported}")


if __name__ == "__main__":
    UniversityCsv.run()
    InterviewCsv.run()
    IndustryCsv.run()
