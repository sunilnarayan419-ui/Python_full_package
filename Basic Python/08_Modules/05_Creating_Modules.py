"""
05_Creating_Modules.py

Topic: Creating and reusing custom modules.

Demonstrates separating reusable functionality (greeter.py) from
execution code, and importing a custom module correctly.
"""

from greeter import create_greeting, create_report_label, format_sample_summary


class UniversityCreatingModules:
    """Introduces importing and using a custom module."""

    @staticmethod
    def run() -> None:
        greeting = create_greeting("Dr. Alvarez", "plant physiologist")

        print("University: creating and importing custom modules")
        print(f"  {greeting}")


class InterviewCreatingModules:
    """Uses the custom module to solve a realistic labeling problem."""

    @staticmethod
    def run() -> None:
        project_code = "CROP-DROUGHT-STUDY"
        report_label = create_report_label(project_code)

        sample_ids = ["S1", "S2", "S3"]
        measurement_counts = [12, 9, 15]
        summaries = [
            format_sample_summary(sample_id, count)
            for sample_id, count in zip(sample_ids, measurement_counts)
        ]

        print("Interview: creating and importing custom modules")
        print(f"  Report label: {report_label}")
        for summary in summaries:
            print(f"  {summary}")


class IndustryCreatingModules:
    """Demonstrates module-level organization and separation of concerns."""

    def __init__(self, project_code: str) -> None:
        if not project_code:
            raise ValueError("project_code must be a non-empty string.")
        self._project_code = project_code

    def build_report_header(self) -> str:
        return create_report_label(self._project_code)

    def build_sample_lines(self, sample_measurement_counts: dict[str, int]) -> list[str]:
        if not sample_measurement_counts:
            raise ValueError("sample_measurement_counts must not be empty.")

        return [
            format_sample_summary(sample_id, count)
            for sample_id, count in sample_measurement_counts.items()
        ]

    def compile_report(self, sample_measurement_counts: dict[str, int]) -> str:
        header = self.build_report_header()
        lines = self.build_sample_lines(sample_measurement_counts)
        return "\n".join([header, *lines])

    @staticmethod
    def run() -> None:
        sample_measurement_counts = {
            "GENE-EXPR-001": 24,
            "GENE-EXPR-002": 18,
            "GENE-EXPR-003": 21,
        }

        builder = IndustryCreatingModules("GENE-EXPRESSION-PANEL")
        report_text = builder.compile_report(sample_measurement_counts)

        print("Industry: creating and importing custom modules")
        print(f"  {report_text}")


if __name__ == "__main__":
    UniversityCreatingModules.run()
    InterviewCreatingModules.run()
    IndustryCreatingModules.run()
