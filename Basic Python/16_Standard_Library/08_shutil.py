"""Demonstrates shutil for safely backing up and archiving experimental data."""

import shutil
import tempfile
from pathlib import Path


class UniversityShutil:
    """Introduces basic file copying using a demo results file."""

    def copy_file(self, source: Path, destination: Path) -> Path:
        return Path(shutil.copy2(source, destination))

    @staticmethod
    def run() -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            source_file = tmp_path / "results.csv"
            source_file.write_text("sample_id,value\n001,12.5\n", encoding="utf-8")

            destination_dir = tmp_path / "backup"
            destination_dir.mkdir()

            demo = UniversityShutil()
            copied_path = demo.copy_file(source_file, destination_dir / "results.csv")
            print(f"Copied file to: {copied_path.name}, exists={copied_path.exists()}")


class InterviewShutil:
    """Solves a safe dataset-organization problem with overwrite protection."""

    def copy_without_overwrite(self, source: Path, destination: Path) -> Path:
        """Copy a file only if the destination does not already exist.

        Raises FileExistsError rather than silently overwriting, since
        overwriting experimental results could destroy prior data.
        """
        if destination.exists():
            raise FileExistsError(f"Refusing to overwrite existing file: {destination}")
        return Path(shutil.copy2(source, destination))

    def organize_by_extension(self, source_dir: Path, target_dir: Path) -> dict[str, int]:
        """Copy files from source_dir into extension-named subfolders under target_dir."""
        if not source_dir.exists():
            raise FileNotFoundError(f"Source directory does not exist: {source_dir}")

        counts: dict[str, int] = {}
        for file_path in source_dir.iterdir():
            if not file_path.is_file():
                continue
            extension = file_path.suffix.lstrip(".") or "unknown"
            destination_folder = target_dir / extension
            destination_folder.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file_path, destination_folder / file_path.name)
            counts[extension] = counts.get(extension, 0) + 1
        return counts

    @staticmethod
    def run() -> None:
        solver = InterviewShutil()

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            source_file = tmp_path / "sample.fasta"
            source_file.write_text(">seq1\nACGT\n", encoding="utf-8")
            destination = tmp_path / "archive" / "sample.fasta"
            destination.parent.mkdir()

            # Test case 1: normal copy
            copied = solver.copy_without_overwrite(source_file, destination)
            print(f"Copied without overwrite: {copied.name}")

            # Test case 2: edge case, destination already exists
            try:
                solver.copy_without_overwrite(source_file, destination)
            except FileExistsError as error:
                print(f"Handled overwrite protection: {error}")

            raw_dir = tmp_path / "raw"
            raw_dir.mkdir()
            (raw_dir / "reads.fastq").write_text("@r1\nACGT\n+\n!!!!\n", encoding="utf-8")
            (raw_dir / "notes.txt").write_text("notes", encoding="utf-8")

            organized = solver.organize_by_extension(raw_dir, tmp_path / "organized")
            print(f"Organized file counts by extension: {organized}")


class IndustryShutil:
    """Controlled backup and archive workflow for experimental output data."""

    def backup_results_directory(self, source_dir: Path, backup_root: Path) -> Path:
        """Copy an entire results directory into a timestamped backup location.

        Uses copytree so the full directory structure is preserved, and always
        targets a new subdirectory under backup_root to avoid touching existing
        backups or arbitrary user files.
        """
        if not source_dir.exists():
            raise FileNotFoundError(f"Source directory does not exist: {source_dir}")

        backup_root.mkdir(parents=True, exist_ok=True)
        destination = backup_root / source_dir.name
        shutil.copytree(source_dir, destination)
        return destination

    def create_archive(self, source_dir: Path, archive_base_path: Path) -> str:
        """Create a zip archive of a results directory for distribution."""
        if not source_dir.exists():
            raise FileNotFoundError(f"Source directory does not exist: {source_dir}")
        return shutil.make_archive(str(archive_base_path), "zip", root_dir=source_dir)

    @staticmethod
    def run() -> None:
        manager = IndustryShutil()

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            results_dir = tmp_path / "experiment_results"
            results_dir.mkdir()
            (results_dir / "summary.csv").write_text("metric,value\nyield,88.4\n", encoding="utf-8")
            (results_dir / "log.txt").write_text("run completed\n", encoding="utf-8")

            backup_root = tmp_path / "backups"
            backup_path = manager.backup_results_directory(results_dir, backup_root)
            print(f"Backed up results to: {backup_path.name}")

            archive_path = manager.create_archive(results_dir, tmp_path / "experiment_archive")
            print(f"Created archive: {Path(archive_path).name}")


if __name__ == "__main__":
    UniversityShutil.run()
    InterviewShutil.run()
    IndustryShutil.run()
