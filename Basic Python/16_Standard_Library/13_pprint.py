"""Demonstrates pprint for readable inspection of nested scientific records."""

from pprint import pformat, pprint


class UniversityPprint:
    """Introduces pretty-printing a nested plant-sample record."""

    def __init__(self, record: dict[str, object]) -> None:
        self.record = record

    def display(self) -> None:
        pprint(self.record)

    @staticmethod
    def run() -> None:
        record = {
            "sample_id": "PL-0042",
            "species": "Arabidopsis thaliana",
            "measurements": {"height_cm": 24.5, "leaf_count": 14},
            "collection_dates": ["2026-04-01", "2026-04-15", "2026-04-29"],
        }
        demo = UniversityPprint(record)
        demo.display()


class InterviewPprint:
    """Solves a complex-record-inspection problem, handling nested edge cases."""

    def inspect_record(self, record: dict[str, object], width: int = 60) -> str:
        """Return a readable, width-limited representation of a nested record.

        Raises ValueError for an empty record, since pretty-printing nothing
        usually indicates an upstream bug rather than a meaningful result.
        """
        if not record:
            raise ValueError("record must not be empty.")
        return pformat(record, width=width, sort_dicts=True)

    @staticmethod
    def run() -> None:
        solver = InterviewPprint()

        # Test case 1: normal nested record with a deeply nested structure
        record = {
            "experiment_id": "EXP-2026-07",
            "conditions": {"temperature_c": 25, "humidity_pct": 60},
            "replicates": [
                {"replicate": 1, "expression_level": 4.2},
                {"replicate": 2, "expression_level": 4.6},
            ],
        }
        formatted = solver.inspect_record(record, width=50)
        print(formatted)

        # Test case 2: edge case, empty record
        try:
            solver.inspect_record({})
        except ValueError as error:
            print(f"Handled empty record: {error}")


class IndustryPprint:
    """Readable diagnostic reporting utility, distinct from JSON serialization."""

    def build_diagnostic_report(self, pipeline_state: dict[str, object]) -> str:
        """Produce a human-readable diagnostic report for developers/operators.

        This is intentionally separate from JSON serialization: pprint output
        is for human debugging in logs/consoles, not for machine-readable
        persistence or interchange between systems.
        """
        header = "=== Pipeline Diagnostic Report ==="
        body = pformat(pipeline_state, indent=2, width=70, sort_dicts=True)
        return f"{header}\n{body}"

    @staticmethod
    def run() -> None:
        reporter = IndustryPprint()

        pipeline_state = {
            "stage": "quality_control",
            "samples_processed": 128,
            "failed_samples": ["PL-0007", "PL-0033"],
            "thresholds": {"min_read_depth": 30, "max_missing_pct": 5.0},
        }

        report = reporter.build_diagnostic_report(pipeline_state)
        print(report)


if __name__ == "__main__":
    UniversityPprint.run()
    InterviewPprint.run()
    IndustryPprint.run()
