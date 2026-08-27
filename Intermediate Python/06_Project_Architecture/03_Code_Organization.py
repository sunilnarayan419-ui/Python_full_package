"""Demonstrates professional code organization: strict separation between
domain models, business logic, infrastructure concerns, configuration,
and presentation/output for a laboratory results pipeline.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Domain models -- pure data, no behavior tied to I/O or formatting.
# ---------------------------------------------------------------------------


class InvalidResultError(ValueError):
    """Raised when a lab result fails a domain validation rule."""


@dataclass(frozen=True, slots=True)
class LabResult:
    sample_id: str
    analyte: str
    value: float


# ---------------------------------------------------------------------------
# Configuration -- isolated from business logic; passed in, not read
# ad-hoc from globals or the environment inside domain/business code.
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ResultProcessingConfig:
    max_valid_value: float
    output_directory: Path


# ---------------------------------------------------------------------------
# Business logic -- validation and transformation rules only. No file
# handling, no logging side effects beyond what the caller controls, no
# printing.
# ---------------------------------------------------------------------------


class LabResultValidator:
    """Encapsulates the domain rule for what constitutes a valid result."""

    def __init__(self, config: ResultProcessingConfig) -> None:
        self._config = config

    def validate(self, result: LabResult) -> None:
        if result.value < 0 or result.value > self._config.max_valid_value:
            raise InvalidResultError(
                f"{result.sample_id}: value {result.value} outside valid range "
                f"[0, {self._config.max_valid_value}] for {result.analyte}"
            )


class LabResultProcessor:
    """Applies validation and computes derived values for a batch of results."""

    def __init__(self, validator: LabResultValidator) -> None:
        self._validator = validator

    def process_batch(self, results: list[LabResult]) -> list[LabResult]:
        valid_results = []
        for result in results:
            try:
                self._validator.validate(result)
            except InvalidResultError:
                logger.warning("Rejected result for sample %s", result.sample_id)
                continue
            valid_results.append(result)
        return valid_results


# ---------------------------------------------------------------------------
# Infrastructure -- file I/O isolated behind a small, focused class. The
# business logic above has no knowledge of how or where results are
# written.
# ---------------------------------------------------------------------------


class LabResultFileWriter:
    """Persists processed results to disk. The only component in this
    module aware of filesystem details.
    """

    def __init__(self, config: ResultProcessingConfig) -> None:
        self._config = config

    def write(self, results: list[LabResult]) -> Path:
        self._config.output_directory.mkdir(parents=True, exist_ok=True)
        destination = self._config.output_directory / "results.csv"
        lines = [f"{r.sample_id},{r.analyte},{r.value}" for r in results]
        destination.write_text("\n".join(lines), encoding="utf-8")
        return destination


# ---------------------------------------------------------------------------
# Presentation/output -- formatting for human consumption, separate from
# both business logic and infrastructure.
# ---------------------------------------------------------------------------


def format_summary(results: list[LabResult]) -> str:
    if not results:
        return "No valid results to report."
    lines = [f"{r.sample_id} ({r.analyte}): {r.value:.2f}" for r in results]
    return "\n".join(lines)


if __name__ == "__main__":
    import tempfile

    config = ResultProcessingConfig(
        max_valid_value=1000.0,
        output_directory=Path(tempfile.mkdtemp()) / "lab_results",
    )

    validator = LabResultValidator(config)
    processor = LabResultProcessor(validator)
    writer = LabResultFileWriter(config)

    raw_results = [
        LabResult(sample_id="S-300", analyte="glucose", value=95.0),
        LabResult(sample_id="S-301", analyte="glucose", value=-5.0),  # rejected
    ]

    processed = processor.process_batch(raw_results)
    output_path = writer.write(processed)

    print(format_summary(processed))
    print(f"Written to: {output_path}")
