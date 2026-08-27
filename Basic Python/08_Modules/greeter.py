"""
greeter.py

Reusable module providing greeting and report-label utilities for
scientific software projects. Contains no execution side effects when
imported.
"""

from datetime import datetime


def create_greeting(name: str, role: str) -> str:
    """Return a formatted greeting for a lab team member."""
    if not name:
        raise ValueError("name must be a non-empty string.")
    if not role:
        raise ValueError("role must be a non-empty string.")

    return f"Hello, {name}. Welcome to the lab as {role}."


def create_report_label(project_code: str) -> str:
    """Return a timestamped report label for a given project code."""
    if not project_code:
        raise ValueError("project_code must be a non-empty string.")

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{project_code}_{timestamp}"


def format_sample_summary(sample_id: str, measurement_count: int) -> str:
    """Return a concise human-readable summary line for a sample."""
    if not sample_id:
        raise ValueError("sample_id must be a non-empty string.")
    if measurement_count < 0:
        raise ValueError("measurement_count must be non-negative.")

    return f"Sample '{sample_id}' contains {measurement_count} measurement(s)."
