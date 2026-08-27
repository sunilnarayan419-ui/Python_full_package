"""File-handling curriculum: reading files with read(), readline(),
readlines(), and iteration."""

from __future__ import annotations

import tempfile
from pathlib import Path


class UniversityReadingFiles:
    """Teaches read(), readline(), and readlines() using DNA sequence
    records."""

    @staticmethod
    def run() -> None:
        demo_dir = Path(tempfile.mkdtemp(prefix="university_reading_"))
        dna_file = demo_dir / "dna_sequences.txt"
        dna_file.write_text(
            "ATGCGTACGTAGCTAG\nGGCTATTCGATCGATT\nTTAGGCATCGGATCGA\n",
            encoding="utf-8",
        )

        with open(dna_file, mode="r", encoding="utf-8") as file_handle:
            full_contents = file_handle.read()
        print("[University] read() full contents:")
        print(full_contents)

        with open(dna_file, mode="r", encoding="utf-8") as file_handle:
            first_sequence = file_handle.readline()
        print("[University] readline() first sequence:")
        print(first_sequence.strip())

        with open(dna_file, mode="r", encoding="utf-8") as file_handle:
            all_sequences = file_handle.readlines()
        print("[University] readlines() list of sequences:")
        print(all_sequences)

        dna_file.unlink()
        demo_dir.rmdir()


class InterviewReadingFiles:
    """Processes plant measurement records line-by-line, demonstrating
    iteration and simple aggregation."""

    @staticmethod
    def _parse_height_line(line: str) -> tuple[str, float] | None:
        parts = line.strip().split(",")
        if len(parts) != 2:
            return None
        sample_id, raw_height = parts
        try:
            return sample_id, float(raw_height)
        except ValueError:
            return None

    @staticmethod
    def run() -> None:
        demo_dir = Path(tempfile.mkdtemp(prefix="interview_reading_"))
        measurements_file = demo_dir / "plant_heights.txt"
        measurements_file.write_text(
            "P001,28.5\nP002,31.2\nP003,invalid\nP004,26.9\n", encoding="utf-8"
        )

        valid_heights: list[float] = []
        skipped_lines = 0

        with open(measurements_file, mode="r", encoding="utf-8") as file_handle:
            for line in file_handle:
                parsed = InterviewReadingFiles._parse_height_line(line)
                if parsed is None:
                    skipped_lines += 1
                    continue
                _, height = parsed
                valid_heights.append(height)

        average_height = sum(valid_heights) / len(valid_heights) if valid_heights else 0.0
        print(f"[Interview] Valid heights: {valid_heights}")
        print(f"[Interview] Skipped malformed lines: {skipped_lines}")
        print(f"[Interview] Average plant height: {average_height:.2f} cm")

        measurements_file.unlink()
        demo_dir.rmdir()


class IndustryReadingFiles:
    """Streams large experiment logs line-by-line to avoid unnecessary
    memory usage, a pattern essential for scientific file processing."""

    def __init__(self, encoding: str = "utf-8") -> None:
        self._encoding = encoding

    def stream_gene_expression_records(self, path: Path) -> list[tuple[str, float]]:
        """Read gene expression records without loading the entire file
        into memory at once."""
        if not path.exists():
            raise FileNotFoundError(f"Expression file not found: {path}")

        records: list[tuple[str, float]] = []
        with open(path, mode="r", encoding=self._encoding) as file_handle:
            for line_number, line in enumerate(file_handle, start=1):
                stripped = line.strip()
                if not stripped:
                    continue
                gene_id, _, raw_value = stripped.partition(",")
                try:
                    expression_level = float(raw_value)
                except ValueError as error:
                    raise ValueError(
                        f"Malformed expression value on line {line_number}: {stripped!r}"
                    ) from error
                records.append((gene_id, expression_level))
        return records

    @staticmethod
    def run() -> None:
        demo_dir = Path(tempfile.mkdtemp(prefix="industry_reading_"))
        expression_file = demo_dir / "gene_expression_large.txt"
        expression_file.write_text(
            "BRCA1,4.2\nTP53,7.8\nEGFR,3.1\nMYC,9.4\n", encoding="utf-8"
        )

        reader = IndustryReadingFiles()
        records = reader.stream_gene_expression_records(expression_file)
        print(f"[Industry] Streamed {len(records)} gene expression records:")
        for gene_id, expression_level in records:
            print(f"  {gene_id}: {expression_level}")

        malformed_file = demo_dir / "gene_expression_malformed.txt"
        malformed_file.write_text("BRCA1,4.2\nTP53,not_a_number\n", encoding="utf-8")
        print("[Industry] Handling malformed expression data:")
        try:
            reader.stream_gene_expression_records(malformed_file)
        except ValueError as error:
            print(f"Caught expected error: {error}")

        expression_file.unlink()
        malformed_file.unlink()
        demo_dir.rmdir()


if __name__ == "__main__":
    UniversityReadingFiles.run()
    InterviewReadingFiles.run()
    IndustryReadingFiles.run()
