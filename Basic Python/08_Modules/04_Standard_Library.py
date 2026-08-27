"""
04_Standard_Library.py

Topic: Practical use of Python's standard library.

Demonstrates math, statistics, collections, pathlib, json, csv, datetime,
and re working together to support scientific and bioinformatics workflows.
"""

import csv
import io
import json
import math
import re
import statistics
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


class UniversityStandardLibrary:
    """Introduces several standard-library modules through direct examples."""

    @staticmethod
    def run() -> None:
        dna_sequence = "ATGCGTACGTTAGC"
        base_counts = Counter(dna_sequence)

        gc_content = (base_counts["G"] + base_counts["C"]) / len(dna_sequence) * 100
        rounded_gc = math.floor(gc_content * 100) / 100

        print("University: standard library modules")
        print(f"  Sequence: {dna_sequence}")
        print(f"  Base counts: {dict(base_counts)}")
        print(f"  GC content: {rounded_gc:.2f}%")


class InterviewStandardLibrary:
    """Combines standard-library modules to solve a realistic parsing task."""

    @staticmethod
    def _parse_sample_ids(raw_labels: list[str]) -> list[str]:
        pattern = re.compile(r"^SAMPLE-(\d{3})$")
        valid_ids = []
        for label in raw_labels:
            if pattern.match(label):
                valid_ids.append(label)
        return valid_ids

    @staticmethod
    def run() -> None:
        raw_labels = ["SAMPLE-001", "SAMPLE-2", "SAMPLE-045", "control", "SAMPLE-100"]
        valid_ids = InterviewStandardLibrary._parse_sample_ids(raw_labels)

        readings_by_id: dict[str, list[float]] = defaultdict(list)
        readings_by_id["SAMPLE-001"].extend([0.44, 0.47, 0.45])
        readings_by_id["SAMPLE-045"].extend([0.61, 0.58])

        summary = {
            sample_id: round(statistics.mean(values), 3)
            for sample_id, values in readings_by_id.items()
        }

        print("Interview: standard library modules")
        print(f"  Valid sample IDs: {valid_ids}")
        print(f"  Mean readings: {summary}")


class IndustryStandardLibrary:
    """Demonstrates a small realistic workflow using multiple stdlib tools."""

    def __init__(self, output_directory: Path) -> None:
        self._output_directory = output_directory
        self._output_directory.mkdir(parents=True, exist_ok=True)

    def ingest_csv_readings(self, csv_text: str) -> list[dict[str, str]]:
        reader = csv.DictReader(io.StringIO(csv_text))
        return list(reader)

    def compute_statistics(self, rows: list[dict[str, str]], field: str) -> dict[str, float]:
        values = [float(row[field]) for row in rows if row.get(field)]
        if not values:
            raise ValueError(f"No numeric values found for field '{field}'.")

        return {
            "mean": statistics.mean(values),
            "stdev": statistics.stdev(values) if len(values) > 1 else 0.0,
            "min": min(values),
            "max": max(values),
        }

    def write_report(self, summary: dict[str, float], report_name: str) -> Path:
        report_path = self._output_directory / f"{report_name}.json"
        payload = {
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "summary": summary,
        }
        report_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return report_path

    @staticmethod
    def run() -> None:
        csv_text = (
            "sample_id,absorbance\n"
            "S1,0.412\n"
            "S2,0.398\n"
            "S3,0.421\n"
            "S4,0.405\n"
        )

        workflow = IndustryStandardLibrary(Path("./lab_reports"))
        rows = workflow.ingest_csv_readings(csv_text)
        summary = workflow.compute_statistics(rows, "absorbance")
        report_path = workflow.write_report(summary, "absorbance_summary")

        print("Industry: standard library modules")
        print(f"  Parsed rows: {len(rows)}")
        print(f"  Summary: {summary}")
        print(f"  Report written to: {report_path}")


if __name__ == "__main__":
    UniversityStandardLibrary.run()
    InterviewStandardLibrary.run()
    IndustryStandardLibrary.run()
