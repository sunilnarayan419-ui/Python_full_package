"""File-handling curriculum: opening files with open()."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import IO


class UniversityOpeningFiles:
    """Teaches the fundamental open()/close() workflow using a simple
    biological experiment file."""

    @staticmethod
    def run() -> None:
        demo_dir = Path(tempfile.mkdtemp(prefix="university_opening_"))
        experiment_file = demo_dir / "experiment_log.txt"

        experiment_file.write_text(
            "sample_id,species,height_cm\n"
            "P001,Wheat,28.5\n"
            "P002,Rice,31.2\n",
            encoding="utf-8",
        )

        file_handle: IO[str] = open(experiment_file, mode="r", encoding="utf-8")
        contents = file_handle.read()
        file_handle.close()

        print("[University] Opened file manually with open()/close():")
        print(contents)

        experiment_file.unlink()
        demo_dir.rmdir()


class InterviewOpeningFiles:
    """Demonstrates safe opening and handling of common file errors."""

    @staticmethod
    def _open_experiment_file(path: Path) -> str:
        try:
            file_handle = open(path, mode="r", encoding="utf-8")
        except FileNotFoundError:
            return f"Error: experiment file not found at {path}"
        except PermissionError:
            return f"Error: insufficient permissions to read {path}"
        except IsADirectoryError:
            return f"Error: expected a file but found a directory at {path}"

        try:
            return file_handle.read()
        finally:
            file_handle.close()

    @staticmethod
    def run() -> None:
        demo_dir = Path(tempfile.mkdtemp(prefix="interview_opening_"))
        gene_file = demo_dir / "gene_expression.txt"
        gene_file.write_text(
            "gene_id,expression_level\nBRCA1,4.2\nTP53,7.8\n", encoding="utf-8"
        )

        print("[Interview] Reading an existing file:")
        print(InterviewOpeningFiles._open_experiment_file(gene_file))

        missing_file = demo_dir / "missing_gene_expression.txt"
        print("[Interview] Attempting to read a missing file:")
        print(InterviewOpeningFiles._open_experiment_file(missing_file))

        gene_file.unlink()
        demo_dir.rmdir()


class IndustryOpeningFiles:
    """Maintainable file-opening utility built on pathlib and explicit
    typing, suitable for reuse across a scientific codebase."""

    def __init__(self, encoding: str = "utf-8") -> None:
        self._encoding = encoding

    def open_text_file(self, path: Path, mode: str = "r") -> IO[str]:
        """Open a text file with validated mode and explicit encoding.

        Raises:
            ValueError: if a binary mode is requested.
            FileNotFoundError: if the file does not exist for read modes.
            IsADirectoryError: if path points to a directory.
        """
        if "b" in mode:
            raise ValueError("Use a dedicated binary-handling method for binary I/O.")
        if path.is_dir():
            raise IsADirectoryError(f"Expected a file, got a directory: {path}")
        return open(path, mode=mode, encoding=self._encoding)

    def read_compound_record(self, path: Path) -> str:
        with self.open_text_file(path, mode="r") as file_handle:
            return file_handle.read()

    @staticmethod
    def run() -> None:
        demo_dir = Path(tempfile.mkdtemp(prefix="industry_opening_"))
        compound_file = demo_dir / "compound_descriptors.txt"
        compound_file.write_text(
            "compound_id,molecular_weight,logp\nCMP001,342.4,2.1\n",
            encoding="utf-8",
        )

        opener = IndustryOpeningFiles()
        print("[Industry] Reading via IndustryOpeningFiles utility:")
        print(opener.read_compound_record(compound_file))

        print("[Industry] Handling a directory passed as a file path:")
        try:
            opener.read_compound_record(demo_dir)
        except IsADirectoryError as error:
            print(f"Caught expected error: {error}")

        compound_file.unlink()
        demo_dir.rmdir()


if __name__ == "__main__":
    UniversityOpeningFiles.run()
    InterviewOpeningFiles.run()
    IndustryOpeningFiles.run()
