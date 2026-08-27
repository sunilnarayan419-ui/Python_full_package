from __future__ import annotations

import tempfile
from pathlib import Path


class UniversityPathlib:
    """Basic scientific-data directory operations using pathlib.Path,
    demonstrated inside a temporary directory so nothing persists on
    the user's filesystem."""

    def __init__(self, base_dir: Path) -> None:
        self.base_dir = base_dir

    def create_sample_directory(self, sample_id: str) -> Path:
        """Time: O(1) (single filesystem call)."""
        sample_dir = self.base_dir / sample_id
        sample_dir.mkdir(parents=True, exist_ok=True)
        return sample_dir

    def write_reading(self, sample_dir: Path, filename: str, content: str) -> Path:
        """Time: O(n) in content length."""
        file_path = sample_dir / filename
        file_path.write_text(content, encoding="utf-8")
        return file_path

    @staticmethod
    def run() -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base_dir = Path(tmp)
            demo = UniversityPathlib(base_dir)
            sample_dir = demo.create_sample_directory("S001")
            file_path = demo.write_reading(sample_dir, "reading.txt", "pH=6.8\n")
            print("University: created ->", file_path)
            print("University: exists ->", file_path.exists())
            print("University: is_file ->", file_path.is_file())
            print("University: content ->", file_path.read_text(encoding="utf-8").strip())


class DatasetNotFoundError(FileNotFoundError):
    """Raised when an expected dataset directory does not exist."""


class InterviewPathlib:
    """Search and filter files robustly, with explicit handling of
    missing directories and unexpected file types."""

    @staticmethod
    def find_csv_files(dataset_dir: Path) -> list[Path]:
        """Recursively find all .csv files under dataset_dir.

        Time: O(f) where f is the number of filesystem entries scanned
        Raises DatasetNotFoundError if dataset_dir does not exist.
        """
        if not dataset_dir.exists():
            raise DatasetNotFoundError(f"dataset directory not found: {dataset_dir}")
        if not dataset_dir.is_dir():
            raise NotADirectoryError(f"expected a directory, got: {dataset_dir}")
        return sorted(dataset_dir.rglob("*.csv"))

    @staticmethod
    def group_by_stem_prefix(files: list[Path], prefix_length: int = 3) -> dict[str, list[Path]]:
        """Group files by the first prefix_length characters of their
        stem (filename without suffix) - e.g. grouping "S001_run1.csv"
        and "S001_run2.csv" under "S00".

        Time: O(n)
        """
        groups: dict[str, list[Path]] = {}
        for file_path in files:
            key = file_path.stem[:prefix_length]
            groups.setdefault(key, []).append(file_path)
        return groups

    @staticmethod
    def run() -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dataset_dir = Path(tmp) / "genomics_dataset"
            dataset_dir.mkdir()
            (dataset_dir / "S001_run1.csv").write_text("id,value\n1,2\n", encoding="utf-8")
            (dataset_dir / "S001_run2.csv").write_text("id,value\n3,4\n", encoding="utf-8")
            (dataset_dir / "notes.txt").write_text("not a csv\n", encoding="utf-8")
            nested = dataset_dir / "batch2"
            nested.mkdir()
            (nested / "S002_run1.csv").write_text("id,value\n5,6\n", encoding="utf-8")

            csv_files = InterviewPathlib.find_csv_files(dataset_dir)
            print("Interview: found csv files ->", [f.name for f in csv_files])

            grouped = InterviewPathlib.group_by_stem_prefix(csv_files)
            print("Interview: grouped by prefix ->", {k: [f.name for f in v] for k, v in grouped.items()})

            try:
                InterviewPathlib.find_csv_files(Path(tmp) / "does_not_exist")
            except DatasetNotFoundError as error:
                print("Interview: missing directory caught ->", error)


class DatasetFile:
    """Lightweight wrapper describing one managed dataset file."""

    __slots__ = ("path",)

    def __init__(self, path: Path) -> None:
        self.path = path

    @property
    def sample_id(self) -> str:
        return self.path.stem.split("_")[0]

    @property
    def size_bytes(self) -> int:
        return self.path.stat().st_size


class IndustryPathlib:
    """A reusable scientific dataset/file-management component that
    indexes a dataset directory, exposes safe read-only metadata, and
    never performs destructive filesystem operations.
    """

    def __init__(self, dataset_root: Path) -> None:
        if not dataset_root.exists():
            raise DatasetNotFoundError(f"dataset root not found: {dataset_root}")
        self.dataset_root = dataset_root

    def index_files(self, suffix: str = ".csv") -> list[DatasetFile]:
        """Time: O(f), Space: O(f) for the returned index."""
        return [DatasetFile(path) for path in sorted(self.dataset_root.rglob(f"*{suffix}"))]

    def total_size_bytes(self, files: list[DatasetFile]) -> int:
        """Time: O(n)."""
        return sum(f.size_bytes for f in files)

    def group_by_sample(self, files: list[DatasetFile]) -> dict[str, list[Path]]:
        """Time: O(n), Space: O(n)."""
        groups: dict[str, list[Path]] = {}
        for dataset_file in files:
            groups.setdefault(dataset_file.sample_id, []).append(dataset_file.path)
        return groups

    @staticmethod
    def run() -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dataset_root = Path(tmp) / "proteomics_dataset"
            dataset_root.mkdir()
            (dataset_root / "S001_batchA.csv").write_text("a,b\n1,2\n", encoding="utf-8")
            (dataset_root / "S002_batchA.csv").write_text("a,b\n3,4\n", encoding="utf-8")
            archive = dataset_root / "archive"
            archive.mkdir()
            (archive / "S001_batchB.csv").write_text("a,b\n5,6\n", encoding="utf-8")

            manager = IndustryPathlib(dataset_root)
            files = manager.index_files(suffix=".csv")
            print("Industry: indexed files ->", [f.path.relative_to(dataset_root) for f in files])
            print("Industry: total size (bytes) ->", manager.total_size_bytes(files))

            grouped = manager.group_by_sample(files)
            print("Industry: grouped by sample_id ->", {k: [p.name for p in v] for k, v in grouped.items()})


if __name__ == "__main__":
    UniversityPathlib.run()
    InterviewPathlib.run()
    IndustryPathlib.run()
