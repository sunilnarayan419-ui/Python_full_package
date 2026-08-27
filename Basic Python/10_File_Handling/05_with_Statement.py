"""File-handling curriculum: the with statement and context managers
for exception-safe resource handling."""

from __future__ import annotations

import tempfile
from pathlib import Path


class UniversityWithStatement:
    """Teaches the basic with open(...) as file pattern using a
    biological sample record."""

    @staticmethod
    def run() -> None:
        demo_dir = Path(tempfile.mkdtemp(prefix="university_with_"))
        sample_file = demo_dir / "sample_record.txt"

        with open(sample_file, mode="w", encoding="utf-8") as file_handle:
            file_handle.write("sample_id=P001\nspecies=Wheat\n")

        with open(sample_file, mode="r", encoding="utf-8") as file_handle:
            contents = file_handle.read()

        print("[University] File automatically closed after the with block:")
        print(f"file_handle.closed == {file_handle.closed}")
        print(contents)

        sample_file.unlink()
        demo_dir.rmdir()


class InterviewWithStatement:
    """Demonstrates exception-safe processing using with, showing that
    the file is closed even when an error occurs mid-processing."""

    @staticmethod
    def _process_enzyme_records(file_path: Path) -> list[float]:
        activity_levels: list[float] = []
        with open(file_path, mode="r", encoding="utf-8") as file_handle:
            for line in file_handle:
                enzyme_id, _, raw_activity = line.strip().partition(",")
                if not raw_activity:
                    raise ValueError(f"Missing activity value for {enzyme_id!r}")
                activity_levels.append(float(raw_activity))
        return activity_levels

    @staticmethod
    def run() -> None:
        demo_dir = Path(tempfile.mkdtemp(prefix="interview_with_"))
        enzyme_file = demo_dir / "enzyme_activity.txt"
        enzyme_file.write_text("ENZ001,3.4\nENZ002,5.1\n", encoding="utf-8")

        print("[Interview] Processing valid enzyme activity records:")
        print(InterviewWithStatement._process_enzyme_records(enzyme_file))

        broken_file = demo_dir / "broken_enzyme_activity.txt"
        broken_file.write_text("ENZ001,3.4\nENZ002,\n", encoding="utf-8")

        print("[Interview] File handle is still closed after an error:")
        file_handle_ref = open(broken_file, mode="r", encoding="utf-8")
        file_handle_ref.close()
        try:
            InterviewWithStatement._process_enzyme_records(broken_file)
        except ValueError as error:
            print(f"Caught expected error: {error}")

        enzyme_file.unlink()
        broken_file.unlink()
        demo_dir.rmdir()


class IndustryWithStatement:
    """Uses a small custom context manager to guarantee cleanup of a
    scratch directory used during scientific data processing, without
    over-engineering the abstraction."""

    def __init__(self, base_dir: Path) -> None:
        self._base_dir = base_dir
        self._scratch_dir: Path | None = None

    def __enter__(self) -> Path:
        self._scratch_dir = self._base_dir / "scratch_processing"
        self._scratch_dir.mkdir(parents=True, exist_ok=True)
        return self._scratch_dir

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if self._scratch_dir is not None:
            for child in self._scratch_dir.iterdir():
                child.unlink()
            self._scratch_dir.rmdir()

    @staticmethod
    def run() -> None:
        demo_dir = Path(tempfile.mkdtemp(prefix="industry_with_"))

        with IndustryWithStatement(demo_dir) as scratch_dir:
            protein_file = scratch_dir / "protein_sequences.txt"
            with open(protein_file, mode="w", encoding="utf-8") as file_handle:
                file_handle.write("PROT001,MKTAYIAKQR\nPROT002,MVLSPADKTN\n")

            with open(protein_file, mode="r", encoding="utf-8") as file_handle:
                print("[Industry] Processed within managed scratch directory:")
                print(file_handle.read())

        scratch_removed = not (demo_dir / "scratch_processing").exists()
        print(f"[Industry] Scratch directory removed: {scratch_removed}")

        demo_dir.rmdir()


if __name__ == "__main__":
    UniversityWithStatement.run()
    InterviewWithStatement.run()
    IndustryWithStatement.run()
