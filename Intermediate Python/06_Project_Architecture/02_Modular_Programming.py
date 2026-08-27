"""Demonstrates modular programming through cohesive, loosely coupled
components representing a validation -> processing -> reporting pipeline.

Each class below represents what would become an independent module in
a real package (e.g. sample_validation.py, measurement_processing.py,
result_reporting.py), exposing a small, stable public interface rather
than sharing internal state.
"""

from __future__ import annotations

from dataclasses import dataclass


class InvalidSampleError(ValueError):
    """Raised when a sample fails validation."""


@dataclass(frozen=True, slots=True)
class Sample:
    sample_id: str
    concentration_ng_ul: float


@dataclass(frozen=True, slots=True)
class ProcessedMeasurement:
    sample_id: str
    normalized_value: float


# ---------------------------------------------------------------------------
# Module boundary 1: SampleValidation
#
# Public interface: validate(). Nothing outside this class needs to know
# how validation rules are implemented internally.
# ---------------------------------------------------------------------------


class SampleValidation:
    """Encapsulates all rules for whether a sample may enter the pipeline."""

    MIN_CONCENTRATION = 0.5

    def validate(self, sample: Sample) -> None:
        if sample.concentration_ng_ul < self.MIN_CONCENTRATION:
            raise InvalidSampleError(
                f"sample {sample.sample_id} below minimum concentration"
            )


# ---------------------------------------------------------------------------
# Module boundary 2: MeasurementProcessing
#
# Depends on SampleValidation through its public interface only -- it
# does not reach into validation internals, so either module can change
# independently as long as the interface contract holds.
# ---------------------------------------------------------------------------


class MeasurementProcessing:
    """Transforms validated samples into normalized measurements."""

    def __init__(self, validator: SampleValidation) -> None:
        self._validator = validator

    def process(self, sample: Sample) -> ProcessedMeasurement:
        self._validator.validate(sample)
        normalized_value = sample.concentration_ng_ul / 100.0
        return ProcessedMeasurement(
            sample_id=sample.sample_id, normalized_value=normalized_value
        )


# ---------------------------------------------------------------------------
# Module boundary 3: ResultReporting
#
# Consumes ProcessedMeasurement objects only -- it has no dependency on
# Sample, SampleValidation, or MeasurementProcessing internals, keeping
# coupling to the minimum shared data contract.
# ---------------------------------------------------------------------------


class ResultReporting:
    """Formats processed measurements into a human-readable report."""

    def build_report(self, measurements: list[ProcessedMeasurement]) -> str:
        lines = [
            f"{m.sample_id}: normalized_value={m.normalized_value:.4f}"
            for m in measurements
        ]
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Composition root: wires the modules together. In a real package this
# would live in the application/service layer, not inside any one module.
# ---------------------------------------------------------------------------


def run_pipeline(samples: list[Sample]) -> str:
    validator = SampleValidation()
    processor = MeasurementProcessing(validator)
    reporter = ResultReporting()

    processed = [processor.process(sample) for sample in samples]
    return reporter.build_report(processed)


if __name__ == "__main__":
    samples = [
        Sample(sample_id="S-200", concentration_ng_ul=25.0),
        Sample(sample_id="S-201", concentration_ng_ul=80.0),
    ]
    print(run_pipeline(samples))
