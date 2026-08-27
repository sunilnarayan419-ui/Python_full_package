"""File-handling curriculum: appending to files without destroying
existing data."""

from __future__ import annotations

import tempfile
from pathlib import Path


class UniversityAppendingFiles:
    """Teaches append mode ('a') using a simple laboratory observation
    log."""

    @staticmethod
    def run() -> None:
        demo_dir = Path(tempfile.mkdtemp(prefix="university_appending_"))
        log_file = demo_dir / "observation_log.txt"

        with open(log_file, mode="w", encoding="utf-8") as file_handle:
            file_handle.write("Day 1: Germination observed.\n")

        with open(log_file, mode="a", encoding="utf-8") as file_handle:
            file_handle.write("Day 2: First leaves appeared.\n")

        with open(log_file, mode="a", encoding="utf-8") as file_handle:
            file_handle.write("Day 3: Stem height 4.5 cm.\n")

        print("[University] Appended observation log contents:")
        print(log_file.read_text(encoding="utf-8"))

        log_file.unlink()
        demo_dir.rmdir()


class InterviewAppendingFiles:
    """Demonstrates incremental plant growth measurement logging,
    distinguishing append from overwrite."""

    @staticmethod
    def _format_growth_record(day: int, height_cm: float) -> str:
        return f"day={day},height_cm={height_cm:.1f}\n"

    @staticmethod
    def run() -> None:
        demo_dir = Path(tempfile.mkdtemp(prefix="interview_appending_"))
        growth_file = demo_dir / "plant_growth.txt"

        daily_measurements = [(1, 2.0), (2, 4.5), (3, 7.1), (4, 9.8)]
        for day, height_cm in daily_measurements:
            with open(growth_file, mode="a", encoding="utf-8") as file_handle:
                file_handle.write(
                    InterviewAppendingFiles._format_growth_record(day, height_cm)
                )

        print("[Interview] Incrementally logged growth measurements:")
        print(growth_file.read_text(encoding="utf-8"))

        print("[Interview] Overwrite mode clears prior data (contrast):")
        with open(growth_file, mode="w", encoding="utf-8") as file_handle:
            file_handle.write("day=1,height_cm=2.0\n")
        print(growth_file.read_text(encoding="utf-8"))

        growth_file.unlink()
        demo_dir.rmdir()


class IndustryAppendingFiles:
    """Validates and appends structured observations to a pipeline
    processing log, distinguishing append behavior from overwrite and
    rejecting malformed records before they reach disk."""

    def __init__(self, log_path: Path) -> None:
        self._log_path = log_path
        if not self._log_path.exists():
            self._log_path.touch()

    @staticmethod
    def _validate_record(sample_id: str, status: str) -> None:
        if not sample_id.strip():
            raise ValueError("sample_id must not be empty.")
        allowed_statuses = {"PENDING", "PROCESSED", "FAILED"}
        if status not in allowed_statuses:
            raise ValueError(
                f"Invalid status {status!r}; expected one of {allowed_statuses}."
            )

    def append_record(self, sample_id: str, status: str) -> None:
        self._validate_record(sample_id, status)
        with open(self._log_path, mode="a", encoding="utf-8") as file_handle:
            file_handle.write(f"{sample_id},{status}\n")

    @staticmethod
    def run() -> None:
        demo_dir = Path(tempfile.mkdtemp(prefix="industry_appending_"))
        log_path = demo_dir / "pipeline_status.log"
        logger = IndustryAppendingFiles(log_path)

        logger.append_record("P001", "PROCESSED")
        logger.append_record("P002", "PENDING")
        logger.append_record("P003", "FAILED")

        print("[Industry] Appended validated pipeline status records:")
        print(log_path.read_text(encoding="utf-8"))

        print("[Industry] Rejecting an invalid status:")
        try:
            logger.append_record("P004", "UNKNOWN")
        except ValueError as error:
            print(f"Caught expected error: {error}")

        print("[Industry] Log unchanged after rejected record:")
        print(log_path.read_text(encoding="utf-8"))

        log_path.unlink()
        demo_dir.rmdir()


if __name__ == "__main__":
    UniversityAppendingFiles.run()
    InterviewAppendingFiles.run()
    IndustryAppendingFiles.run()
