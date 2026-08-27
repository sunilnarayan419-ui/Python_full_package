"""File-handling curriculum: portable path handling with
pathlib.Path."""

from __future__ import annotations

import tempfile
from pathlib import Path


class UniversityFilePaths:
    """Teaches basic Path construction, joining, and existence checks
    using a plant-sample directory layout."""

    @staticmethod
    def run() -> None:
        demo_dir = Path(tempfile.mkdtemp(prefix="university_paths_"))

        samples_dir = demo_dir / "plant_samples"
        samples_dir.mkdir()
        sample_file = samples_dir / "P001.txt"
        sample_file.write_text("species=Wheat\n", encoding="utf-8")

        print(f"[University] Joined path: {sample_file}")
        print(f"[University] Path exists: {sample_file.exists()}")
        print(f"[University] Is file: {sample_file.is_file()}")
        print(f"[University] Is directory: {samples_dir.is_dir()}")
        print(f"[University] Suffix: {sample_file.suffix}")
        print(f"[University] Filename: {sample_file.name}")
        print(f"[University] Parent directory: {sample_file.parent}")

        sample_file.unlink()
        samples_dir.rmdir()
        demo_dir.rmdir()


class InterviewFilePaths:
    """Demonstrates relative vs absolute paths and directory creation
    for a small gene-expression dataset layout."""

    @staticmethod
    def run() -> None:
        demo_dir = Path(tempfile.mkdtemp(prefix="interview_paths_"))

        dataset_dir = demo_dir / "gene_expression_dataset" / "raw"
        dataset_dir.mkdir(parents=True)
        print(f"[Interview] Created nested directories: {dataset_dir}")

        relative_style = Path("gene_expression_dataset") / "raw" / "sample_001.txt"
        print(f"[Interview] Relative-style path (not resolved): {relative_style}")

        absolute_path = dataset_dir.resolve()
        print(f"[Interview] Absolute resolved path: {absolute_path}")
        print(f"[Interview] Is absolute: {absolute_path.is_absolute()}")

        expression_file = dataset_dir / "sample_001.txt"
        expression_file.write_text("BRCA1,4.2\n", encoding="utf-8")
        print(f"[Interview] File suffix: {expression_file.suffix}")
        print(f"[Interview] File stem: {expression_file.stem}")

        expression_file.unlink()
        dataset_dir.rmdir()
        (demo_dir / "gene_expression_dataset").rmdir()
        demo_dir.rmdir()


class IndustryFilePaths:
    """Provides platform-independent path handling utilities suitable
    for scientific software, avoiding manual string concatenation and
    hard-coded absolute paths."""

    def __init__(self, project_root: Path) -> None:
        self._project_root = project_root

    def dataset_path(self, dataset_name: str, filename: str) -> Path:
        """Build a portable path for a dataset file, validating the
        filename has an acceptable extension."""
        allowed_suffixes = {".csv", ".json", ".txt"}
        candidate = self._project_root / "datasets" / dataset_name / filename
        if candidate.suffix not in allowed_suffixes:
            raise ValueError(
                f"Unsupported file suffix {candidate.suffix!r}; "
                f"expected one of {allowed_suffixes}."
            )
        return candidate

    def ensure_dataset_directory(self, dataset_name: str) -> Path:
        directory = self._project_root / "datasets" / dataset_name
        directory.mkdir(parents=True, exist_ok=True)
        return directory

    @staticmethod
    def run() -> None:
        demo_dir = Path(tempfile.mkdtemp(prefix="industry_paths_"))
        manager = IndustryFilePaths(demo_dir)

        dataset_dir = manager.ensure_dataset_directory("compound_descriptors")
        target_path = manager.dataset_path("compound_descriptors", "batch_01.csv")
        target_path.write_text("compound_id,molecular_weight\nCMP001,342.4\n", encoding="utf-8")

        print(f"[Industry] Portable dataset path: {target_path}")
        print(f"[Industry] Path is under project root: "
              f"{manager._project_root in target_path.parents}")

        print("[Industry] Rejecting an unsupported file suffix:")
        try:
            manager.dataset_path("compound_descriptors", "batch_02.exe")
        except ValueError as error:
            print(f"Caught expected error: {error}")

        target_path.unlink()
        dataset_dir.rmdir()
        (demo_dir / "datasets").rmdir()
        demo_dir.rmdir()


if __name__ == "__main__":
    UniversityFilePaths.run()
    InterviewFilePaths.run()
    IndustryFilePaths.run()
