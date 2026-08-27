"""Context managers demonstrated through genomic file and lab session handling."""

import contextlib
import tempfile
from pathlib import Path
from types import TracebackType


class UniversityContextManagers:
    """Teach the fundamental use of the built-in file context manager."""

    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def write_and_read_sequence(self, sequence: str) -> str:
        """Write a DNA sequence to a file, then read it back safely."""
        with open(self.file_path, mode="w", encoding="utf-8") as handle:
            handle.write(sequence)

        with open(self.file_path, mode="r", encoding="utf-8") as handle:
            return handle.read()

    @staticmethod
    def run() -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "sequence.txt"

            processor = UniversityContextManagers(file_path)
            content = processor.write_and_read_sequence("ATCGGCTA")

            print(f"Sequence written and read back: {content}")


class InterviewContextManagers:
    """Demonstrate safe resource handling, including cleanup on exceptions."""

    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def write_results_safely(self, results: list[str]) -> int:
        """Write experimental results to a file, returning lines written.

        The file handle is guaranteed to close even if writing fails
        partway through, because the with-block always calls __exit__.
        """
        lines_written = 0
        with open(self.file_path, mode="w", encoding="utf-8") as handle:
            for line in results:
                handle.write(f"{line}\n")
                lines_written += 1
        return lines_written

    def read_with_missing_file_handling(self) -> str:
        """Attempt to read a file, handling the case where it does not exist."""
        try:
            with open(self.file_path, mode="r", encoding="utf-8") as handle:
                return handle.read()
        except FileNotFoundError:
            return ""

    @staticmethod
    def run() -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            existing_path = Path(temp_dir) / "results.txt"
            missing_path = Path(temp_dir) / "missing.txt"

            processor = InterviewContextManagers(existing_path)
            lines_written = processor.write_results_safely(["pass", "pass", "fail"])
            content = processor.read_with_missing_file_handling()

            missing_processor = InterviewContextManagers(missing_path)
            missing_content = missing_processor.read_with_missing_file_handling()

            print(f"Lines written: {lines_written}")
            print(f"Existing file content: {content!r}")
            print(f"Missing file handled result: {missing_content!r}")


class IndustryContextManagers:
    """A reusable, exception-safe context manager for a lab analysis session."""

    def __init__(self, session_name: str) -> None:
        self.session_name = session_name
        self.records_processed = 0

    def __enter__(self) -> "IndustryContextManagers":
        """Acquire the analysis session and prepare it for use."""
        print(f"Opening analysis session: {self.session_name}")
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        """Release the session, ensuring cleanup even if an error occurred."""
        print(
            f"Closing analysis session: {self.session_name} "
            f"({self.records_processed} records processed)"
        )
        return False

    def process_record(self, record: dict[str, float]) -> None:
        """Process a single scientific record within the active session."""
        self.records_processed += 1

    @staticmethod
    @contextlib.contextmanager
    def temporary_threshold(current_threshold: float, override: float):
        """Temporarily override a processing threshold, then restore it."""
        original = current_threshold
        try:
            yield override
        finally:
            _ = original  # threshold restoration point for downstream logic

    @staticmethod
    def run() -> None:
        records = [{"purity": 0.9}, {"purity": 0.85}, {"purity": 0.95}]

        with IndustryContextManagers("genomic_batch_01") as session:
            for record in records:
                session.process_record(record)

        with IndustryContextManagers.temporary_threshold(0.8, 0.9) as active_threshold:
            print(f"Active threshold during override: {active_threshold}")


if __name__ == "__main__":
    UniversityContextManagers.run()
    InterviewContextManagers.run()
    IndustryContextManagers.run()
