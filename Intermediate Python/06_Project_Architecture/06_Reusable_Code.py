"""Demonstrates designing reusable components: stable, single-purpose
services that are reused unchanged across different experiments, rather
than abstractions introduced merely to avoid minor duplication.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class Measurement:
    sample_id: str
    raw_value: float


# ---------------------------------------------------------------------------
# Reusable component 1: a single-purpose normalizer with a stable,
# narrow interface. It has no knowledge of what experiment calls it.
# ---------------------------------------------------------------------------


class MeasurementNormalizer:
    """Scales raw measurement values into a [0, 1] range given known bounds.

    Reused identically across every experiment that needs min-max
    normalization -- the abstraction is stable because the normalization
    formula itself does not vary by experiment, only its bounds do.
    """

    def __init__(self, min_value: float, max_value: float) -> None:
        if max_value <= min_value:
            raise ValueError("max_value must be greater than min_value")
        self._min_value = min_value
        self._max_value = max_value

    def normalize(self, measurement: Measurement) -> float:
        span = self._max_value - self._min_value
        return (measurement.raw_value - self._min_value) / span


# ---------------------------------------------------------------------------
# Reusable component 2: validation, kept separate because its lifecycle
# and rules change independently of normalization.
# ---------------------------------------------------------------------------


class SampleValidator:
    """Validates that a sample_id follows the organization-wide format.

    Reused by any pipeline that ingests samples, regardless of what
    scientific analysis happens afterward.
    """

    def __init__(self, required_prefix: str) -> None:
        self._required_prefix = required_prefix

    def validate(self, measurement: Measurement) -> None:
        if not measurement.sample_id.startswith(self._required_prefix):
            raise ValueError(
                f"sample_id '{measurement.sample_id}' missing required prefix "
                f"'{self._required_prefix}'"
            )


# ---------------------------------------------------------------------------
# Reusable component 3: report generation depends only on already-
# normalized values, so it is reusable across experiments with entirely
# different normalization bounds.
# ---------------------------------------------------------------------------


class ScientificReportGenerator:
    """Formats a set of (sample_id, normalized_value) pairs into a report.

    Deliberately generic over the source of normalized values -- it
    accepts any object satisfying HasNormalizedValue, so it can be reused
    by pipelines that normalize differently as long as they produce the
    same shape of result.
    """

    def generate(self, normalized: dict[str, float]) -> str:
        lines = [f"{sample_id}: {value:.4f}" for sample_id, value in normalized.items()]
        return "\n".join(lines)


class Experiment(Protocol):
    """Structural contract each experiment-specific pipeline must satisfy
    to reuse the shared components above.
    """

    def bounds(self) -> tuple[float, float]: ...

    def required_prefix(self) -> str: ...


@dataclass(frozen=True, slots=True)
class TemperatureExperiment:
    def bounds(self) -> tuple[float, float]:
        return (-20.0, 50.0)

    def required_prefix(self) -> str:
        return "TEMP-"


@dataclass(frozen=True, slots=True)
class FluorescenceExperiment:
    def bounds(self) -> tuple[float, float]:
        return (0.0, 10_000.0)

    def required_prefix(self) -> str:
        return "FLU-"


def run_experiment_pipeline(
    experiment: Experiment, measurements: list[Measurement]
) -> str:
    """Same three reusable components, wired differently per experiment
    purely through configuration -- no component-level code changes.
    """
    min_value, max_value = experiment.bounds()
    validator = SampleValidator(experiment.required_prefix())
    normalizer = MeasurementNormalizer(min_value, max_value)
    reporter = ScientificReportGenerator()

    normalized: dict[str, float] = {}
    for measurement in measurements:
        validator.validate(measurement)
        normalized[measurement.sample_id] = normalizer.normalize(measurement)

    return reporter.generate(normalized)


if __name__ == "__main__":
    temperature_readings = [
        Measurement(sample_id="TEMP-001", raw_value=22.5),
        Measurement(sample_id="TEMP-002", raw_value=-5.0),
    ]
    print("Temperature experiment:")
    print(run_experiment_pipeline(TemperatureExperiment(), temperature_readings))

    fluorescence_readings = [
        Measurement(sample_id="FLU-001", raw_value=4200.0),
    ]
    print("\nFluorescence experiment:")
    print(run_experiment_pipeline(FluorescenceExperiment(), fluorescence_readings))
