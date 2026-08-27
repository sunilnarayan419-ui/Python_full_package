"""File-handling curriculum: writing files with write() and structured
output generation."""

from __future__ import annotations

import tempfile
from pathlib import Path


class UniversityWritingFiles:
    """Teaches basic write() usage by generating a plant experiment
    report."""

    @staticmethod
    def run() -> None:
        demo_dir = Path(tempfile.mkdtemp(prefix="university_writing_"))
        report_file = demo_dir / "plant_report.txt"

        with open(report_file, mode="w", encoding="utf-8") as file_handle:
            file_handle.write("Plant Experiment Report\n")
            file_handle.write("Sample P001: Wheat, height 28.5 cm\n")
            file_handle.write("Sample P002: Rice, height 31.2 cm\n")

        print("[University] Wrote plant_report.txt, contents:")
        print(report_file.read_text(encoding="utf-8"))

        report_file.unlink()
        demo_dir.rmdir()


class InterviewWritingFiles:
    """Writes sequence-processing results to a file, demonstrating
    multiple records and overwrite behavior."""

    @staticmethod
    def _compute_gc_content(sequence: str) -> float:
        if not sequence:
            return 0.0
        gc_count = sequence.upper().count("G") + sequence.upper().count("C")
        return round((gc_count / len(sequence)) * 100, 2)

    @staticmethod
    def run() -> None:
        demo_dir = Path(tempfile.mkdtemp(prefix="interview_writing_"))
        sequences = {
            "SEQ001": "ATGCGTACGTAGCTAG",
            "SEQ002": "GGCTATTCGATCGATT",
            "SEQ003": "TTAGGCATCGGATCGA",
        }
        results_file = demo_dir / "gc_content_results.txt"

        with open(results_file, mode="w", encoding="utf-8") as file_handle:
            for sequence_id, sequence in sequences.items():
                gc_content = InterviewWritingFiles._compute_gc_content(sequence)
                file_handle.write(f"{sequence_id},{gc_content}\n")

        print("[Interview] Wrote GC-content results:")
        print(results_file.read_text(encoding="utf-8"))

        print("[Interview] Overwriting the same file with fresh results:")
        with open(results_file, mode="w", encoding="utf-8") as file_handle:
            file_handle.write("SEQ004,55.0\n")
        print(results_file.read_text(encoding="utf-8"))

        results_file.unlink()
        demo_dir.rmdir()


class IndustryWritingFiles:
    """Writes calculated biological measurements to structured output,
    ensuring output directories exist and avoiding accidental
    overwrites of existing results."""

    def __init__(self, output_dir: Path) -> None:
        self._output_dir = output_dir
        self._output_dir.mkdir(parents=True, exist_ok=True)

    def write_measurement_report(
        self,
        filename: str,
        records: list[tuple[str, float]],
        allow_overwrite: bool = False,
    ) -> Path:
        """Write measurement records to a report file.

        Raises:
            FileExistsError: if the target exists and overwriting is
                not explicitly allowed.
        """
        target_path = self._output_dir / filename
        if target_path.exists() and not allow_overwrite:
            raise FileExistsError(
                f"Refusing to overwrite existing report: {target_path}"
            )

        with open(target_path, mode="w", encoding="utf-8") as file_handle:
            file_handle.write("sample_id,measurement_cm\n")
            for sample_id, measurement in records:
                file_handle.write(f"{sample_id},{measurement:.2f}\n")

        return target_path

    @staticmethod
    def run() -> None:
        demo_dir = Path(tempfile.mkdtemp(prefix="industry_writing_"))
        writer = IndustryWritingFiles(demo_dir / "reports")

        records = [("P001", 28.5), ("P002", 31.234), ("P003", 26.87)]
        report_path = writer.write_measurement_report("crop_report.csv", records)
        print(f"[Industry] Wrote report to {report_path}")
        print(report_path.read_text(encoding="utf-8"))

        print("[Industry] Attempting accidental overwrite:")
        try:
            writer.write_measurement_report("crop_report.csv", records)
        except FileExistsError as error:
            print(f"Caught expected error: {error}")

        print("[Industry] Explicit overwrite when intended:")
        writer.write_measurement_report(
            "crop_report.csv", [("P004", 29.1)], allow_overwrite=True
        )
        print(report_path.read_text(encoding="utf-8"))

        report_path.unlink()
        (demo_dir / "reports").rmdir()
        demo_dir.rmdir()


if __name__ == "__main__":
    UniversityWritingFiles.run()
    InterviewWritingFiles.run()
    IndustryWritingFiles.run()
