"""Demonstrations of the built-in open() function using temporary biological data files."""

import os
import tempfile


class UniversityOpen:
    """Teach the fundamental behavior of open() for reading and writing text files."""

    def write_and_read(self, file_path: str, content: str) -> str:
        with open(file_path, "w", encoding="utf-8") as file_handle:
            file_handle.write(content)

        with open(file_path, "r", encoding="utf-8") as file_handle:
            return file_handle.read()

    @staticmethod
    def run() -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "sample_report.txt")
            processor = UniversityOpen()
            content = processor.write_and_read(file_path, "sample_id,species\nP001,Wheat\n")
            print("File contents:")
            print(content)


class InterviewOpen:
    """Read/write with validation and explicit encoding, handling edge cases."""

    def append_reading(self, file_path: str, line: str) -> None:
        with open(file_path, "a", encoding="utf-8") as file_handle:
            file_handle.write(line + "\n")

    def read_lines_safely(self, file_path: str) -> list[str]:
        """Return stripped lines, or an empty list if the file does not exist."""
        if not os.path.exists(file_path):
            return []
        with open(file_path, "r", encoding="utf-8") as file_handle:
            return [line.strip() for line in file_handle if line.strip()]

    @staticmethod
    def run() -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "experiment_log.csv")
            analyzer = InterviewOpen()

            analyzer.append_reading(file_path, "sample_id,concentration")
            analyzer.append_reading(file_path, "S001,3.4")
            analyzer.append_reading(file_path, "S002,5.9")

            lines = analyzer.read_lines_safely(file_path)
            print(f"Log lines: {lines}")

            missing_path = os.path.join(temp_dir, "does_not_exist.csv")
            print(f"Missing file lines: {analyzer.read_lines_safely(missing_path)}")


class IndustryOpen:
    """Safe scientific file-processing workflow for FASTA-like sequence data."""

    def __init__(self, directory: str) -> None:
        self.directory = directory

    def write_fasta_record(self, filename: str, header: str, sequence: str) -> str:
        file_path = os.path.join(self.directory, filename)
        with open(file_path, "w", encoding="utf-8") as file_handle:
            file_handle.write(f">{header}\n{sequence}\n")
        return file_path

    def parse_fasta_record(self, file_path: str) -> dict[str, str]:
        """Parse a simple single-record FASTA-like file safely."""
        with open(file_path, "r", encoding="utf-8") as file_handle:
            lines = [line.rstrip("\n") for line in file_handle]

        if not lines or not lines[0].startswith(">"):
            raise ValueError("Invalid FASTA-like file: missing header")

        header = lines[0][1:]
        sequence = "".join(lines[1:])
        return {"header": header, "sequence": sequence}

    @staticmethod
    def run() -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            processor = IndustryOpen(temp_dir)
            file_path = processor.write_fasta_record(
                "sample.fasta", header="P001_Wheat", sequence="ATCGGTAACGT"
            )
            record = processor.parse_fasta_record(file_path)
            print(f"Parsed FASTA record: {record}")


if __name__ == "__main__":
    UniversityOpen.run()
    InterviewOpen.run()
    IndustryOpen.run()
