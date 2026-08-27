"""Demonstrates pathlib for managing scientific project directory structures."""

import tempfile
from pathlib import Path


class UniversityPathlib:
    """Introduces basic Path operations using a scientific project layout."""

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root

    def build_data_path(self, filename: str) -> Path:
        return self.project_root / "data" / filename

    def describe_file(self, file_path: Path) -> dict[str, str]:
        return {
            "name": file_path.name,
            "stem": file_path.stem,
            "suffix": file_path.suffix,
        }

    @staticmethod
    def run() -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_root = Path(tmp_dir) / "genomics_project"
            demo = UniversityPathlib(project_root)

            data_file = demo.build_data_path("sample_001.fasta")
            print(f"Constructed data path: {data_file}")
            print(f"File details: {demo.describe_file(data_file)}")


class InterviewPathlib:
    """Solves a file-discovery problem across a scientific directory tree."""

    def find_files_by_extension(self, root: Path, extension: str) -> list[Path]:
        """Recursively find files with a given extension under root.

        Raises FileNotFoundError if root does not exist, so callers get a clear
        signal rather than a silently empty result for a typo'd path.
        """
        if not root.exists():
            raise FileNotFoundError(f"Directory does not exist: {root}")
        return sorted(root.rglob(f"*{extension}"))

    def ensure_results_directory(self, root: Path) -> Path:
        """Create a results subdirectory if missing, without disturbing existing data."""
        results_dir = root / "results"
        results_dir.mkdir(parents=True, exist_ok=True)
        return results_dir

    @staticmethod
    def run() -> None:
        solver = InterviewPathlib()

        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir) / "experiments"
            (root / "samples").mkdir(parents=True)
            (root / "samples" / "sample_a.csv").write_text("id,value\n1,2\n", encoding="utf-8")
            (root / "samples" / "sample_b.csv").write_text("id,value\n3,4\n", encoding="utf-8")
            (root / "notes.txt").write_text("lab notes", encoding="utf-8")

            # Test case 1: extension that matches files
            csv_files = solver.find_files_by_extension(root, ".csv")
            print(f"Found CSV files: {[f.name for f in csv_files]}")

            # Test case 2: edge case, nonexistent directory
            try:
                solver.find_files_by_extension(root / "missing", ".csv")
            except FileNotFoundError as error:
                print(f"Handled missing directory: {error}")

            results_dir = solver.ensure_results_directory(root)
            print(f"Results directory ready at: {results_dir.exists()}")


class IndustryPathlib:
    """Clean, reusable path management for a scientific project layout."""

    STANDARD_SUBDIRS = ("data", "results", "samples", "genomics", "experiments")

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root

    def initialize_project_layout(self) -> dict[str, Path]:
        """Create the standard scientific project directory layout safely."""
        layout: dict[str, Path] = {}
        for subdir in self.STANDARD_SUBDIRS:
            path = self.project_root / subdir
            path.mkdir(parents=True, exist_ok=True)
            layout[subdir] = path
        return layout

    def write_sample_record(self, sample_id: str, content: str) -> Path:
        """Write a sample record file under the samples directory."""
        samples_dir = self.project_root / "samples"
        samples_dir.mkdir(parents=True, exist_ok=True)
        record_path = samples_dir / f"{sample_id}.txt"
        record_path.write_text(content, encoding="utf-8")
        return record_path

    def iter_data_files(self) -> list[Path]:
        """List files present in the data directory, without recursing into subfolders."""
        data_dir = self.project_root / "data"
        if not data_dir.exists():
            return []
        return sorted(path for path in data_dir.iterdir() if path.is_file())

    @staticmethod
    def run() -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            manager = IndustryPathlib(Path(tmp_dir) / "plant_genomics")

            layout = manager.initialize_project_layout()
            print(f"Initialized project layout: {sorted(layout.keys())}")

            record_path = manager.write_sample_record("sample_042", "species: Zea mays\n")
            print(f"Wrote sample record: {record_path.name}")

            data_files = manager.iter_data_files()
            print(f"Data files present: {len(data_files)}")


if __name__ == "__main__":
    UniversityPathlib.run()
    InterviewPathlib.run()
    IndustryPathlib.run()
