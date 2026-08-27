"""Demonstrations of the built-in help() function using scientific utility code.

help() normally opens an interactive pager or writes to stdout in a way that
is hard to control programmatically. To keep this module deterministic and
automation-friendly, help() output is captured via pydoc rather than printed
directly to the interactive help system.
"""

import io
import contextlib
import pydoc


def calculate_growth_rate(initial_height: float, final_height: float, days: int) -> float:
    """Calculate the average daily growth rate of a plant sample.

    Args:
        initial_height: Height at the start of the observation period (cm).
        final_height: Height at the end of the observation period (cm).
        days: Number of days between measurements.

    Returns:
        Average growth rate in centimeters per day.
    """
    return (final_height - initial_height) / days


class UniversityHelp:
    """Teach the fundamental behavior of help() on a built-in function."""

    @staticmethod
    def documentation_for(obj: object) -> str:
        """Capture help() output as a string instead of printing interactively."""
        return pydoc.render_doc(obj, renderer=pydoc.plaintext)

    @staticmethod
    def run() -> None:
        doc_text = UniversityHelp.documentation_for(len)
        first_line = doc_text.strip().splitlines()[0]
        print(f"help(len) summary line: {first_line}")


class InterviewHelp:
    """Inspect a user-defined function's documentation programmatically."""

    @staticmethod
    def documentation_for(obj: object) -> str:
        return pydoc.render_doc(obj, renderer=pydoc.plaintext)

    @staticmethod
    def has_docstring(obj: object) -> bool:
        return bool(getattr(obj, "__doc__", None))

    @staticmethod
    def run() -> None:
        function_doc = InterviewHelp.documentation_for(calculate_growth_rate)
        first_line = function_doc.strip().splitlines()[0]
        print(f"help(calculate_growth_rate) summary line: {first_line}")

        print(f"calculate_growth_rate has docstring: {InterviewHelp.has_docstring(calculate_growth_rate)}")
        print(f"len has docstring: {InterviewHelp.has_docstring(len)}")


class IndustryHelp:
    """Controlled developer diagnostic workflow for documentation lookup."""

    def __init__(self, target_objects: dict[str, object]) -> None:
        self.target_objects = target_objects

    def documentation_report(self) -> dict[str, str]:
        """Return the first line of each target object's documentation.

        Redirects stdout defensively in case any inspected object triggers
        console output, keeping this diagnostic workflow side-effect free.
        """
        report: dict[str, str] = {}
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            for name, obj in self.target_objects.items():
                doc_text = pydoc.render_doc(obj, renderer=pydoc.plaintext)
                first_line = doc_text.strip().splitlines()[0]
                report[name] = first_line
        return report

    @staticmethod
    def run() -> None:
        diagnostics = IndustryHelp(
            {
                "calculate_growth_rate": calculate_growth_rate,
                "sorted": sorted,
            }
        )
        for name, summary in diagnostics.documentation_report().items():
            print(f"{name}: {summary}")


if __name__ == "__main__":
    UniversityHelp.run()
    InterviewHelp.run()
    IndustryHelp.run()
