"""Demonstrations of the built-in print() function for scientific reporting."""

import logging

logger = logging.getLogger(__name__)


class UniversityPrint:
    """Teach the fundamental behavior of print() for readable output."""

    def __init__(self, sample_id: str, species: str) -> None:
        self.sample_id = sample_id
        self.species = species

    def show_sample(self) -> None:
        print(self.sample_id, self.species)

    @staticmethod
    def run() -> None:
        processor = UniversityPrint(sample_id="P001", species="Wheat")
        processor.show_sample()


class InterviewPrint:
    """Produce formatted diagnostic output using sep= and end=."""

    def __init__(self, measurements: list[float]) -> None:
        self.measurements = measurements

    def print_measurement_row(self) -> None:
        print(*self.measurements, sep=" | ", end="\n")

    def print_progress(self, total: int) -> None:
        """Print a single-line style progress indicator using end=."""
        for step in range(1, total + 1):
            print(f"Processing sample {step}/{total}", end="; ")
        print()  # final newline

    @staticmethod
    def run() -> None:
        case_one = InterviewPrint([3.2, 3.6, 4.1])
        case_two = InterviewPrint([])

        case_one.print_measurement_row()
        case_two.print_measurement_row()
        case_one.print_progress(total=3)


class IndustryPrint:
    """Structured, human-readable scientific reporting output.

    print() is used here purely for direct human-facing console reports.
    For application diagnostics, warnings, or errors, the standard
    `logging` module is the appropriate tool, not print().
    """

    def __init__(self, samples: list[dict[str, object]]) -> None:
        self.samples = samples

    def print_report(self) -> None:
        print("=" * 40)
        print("SCIENTIFIC SAMPLE REPORT")
        print("=" * 40)
        for sample in self.samples:
            print(f"Sample: {sample['sample_id']:<8} Species: {sample['species']}")
        print("=" * 40)

    def log_processing_event(self, sample_id: str) -> None:
        """Application diagnostics belong in logging, not print()."""
        logger.info("Processed sample %s", sample_id)

    @staticmethod
    def run() -> None:
        samples: list[dict[str, object]] = [
            {"sample_id": "S001", "species": "Wheat"},
            {"sample_id": "S002", "species": "Rice"},
        ]

        reporter = IndustryPrint(samples)
        reporter.print_report()
        for sample in samples:
            reporter.log_processing_event(sample["sample_id"])


if __name__ == "__main__":
    UniversityPrint.run()
    InterviewPrint.run()
    IndustryPrint.run()
