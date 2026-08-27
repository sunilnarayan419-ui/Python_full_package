from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


# ============================================================
# UNIVERSITY LEVEL
# ============================================================
# Goal: understand ownership ("has-a") and lifecycle coupling.


@dataclass
class UniSampleCollection:
    """Owned data: destroyed together with its owning experiment."""

    samples: list[str] = field(default_factory=list)

    def add(self, sample_id: str) -> None:
        self.samples.append(sample_id)


class UniPlantExperiment:
    """Composition: a PlantExperiment OWNS a SampleCollection.

    The collection is created inside the experiment and has no meaning
    or lifecycle independent of it -- if the experiment goes away, so
    does its collection.
    """

    def __init__(self, experiment_id: str) -> None:
        self.experiment_id = experiment_id
        self._collection = UniSampleCollection()  # owned, not injected

    def register_sample(self, sample_id: str) -> None:
        self._collection.add(sample_id)

    def sample_count(self) -> int:
        return len(self._collection.samples)


class UniversityComposition:
    @staticmethod
    def run() -> None:
        experiment = UniPlantExperiment("EXP-001")
        experiment.register_sample("LEAF-01")
        experiment.register_sample("LEAF-02")
        print(f"{experiment.experiment_id} owns {experiment.sample_count()} samples")


# ============================================================
# INTERVIEW LEVEL
# ============================================================
# Goal: articulate why composition beats inheritance for a realistic case.


# --- REJECTED ALTERNATIVE (documentation only) ---
# class GerminationExperiment(SampleCollection):
#     """Inheriting from SampleCollection would wrongly claim an experiment
#     IS-A collection of samples, expose collection internals (add/remove)
#     on the experiment's public API, and prevent an experiment from ever
#     swapping in a different storage strategy at runtime."""


class IvMeasurementLog:
    """A focused, independently testable component."""

    def __init__(self) -> None:
        self._entries: list[tuple[str, float]] = []

    def record(self, sample_id: str, value: float) -> None:
        self._entries.append((sample_id, value))

    def average(self) -> float:
        if not self._entries:
            return 0.0
        return sum(v for _, v in self._entries) / len(self._entries)


class IvGerminationExperiment:
    """Owns a MeasurementLog through composition, not inheritance.

    This lets the experiment expose only the API it wants (record_growth)
    while the log stays a swappable, independently testable implementation
    detail. Composition also avoids the fragile-base-class problem: changes
    to IvMeasurementLog can't silently break subclass invariants because
    there is no subclassing relationship at all.
    """

    def __init__(self, experiment_id: str) -> None:
        self.experiment_id = experiment_id
        self._log = IvMeasurementLog()  # created and owned here

    def record_growth(self, sample_id: str, height_cm: float) -> None:
        self._log.record(sample_id, height_cm)

    def average_growth(self) -> float:
        return self._log.average()


class InterviewComposition:
    @staticmethod
    def run() -> None:
        experiment = IvGerminationExperiment("EXP-100")
        experiment.record_growth("SEED-01", 4.2)
        experiment.record_growth("SEED-02", 5.1)
        print(f"Average growth: {experiment.average_growth():.2f} cm")


# ============================================================
# INDUSTRY LEVEL
# ============================================================
# Goal: a modular pipeline composed of interchangeable, independently
# testable components. Composition roots (owned parts) vs injected
# collaborators are both demonstrated, with a clear boundary.


class SampleRejectedError(ValueError):
    """Raised when a sample fails validation."""


@dataclass(frozen=True, slots=True)
class Measurement:
    sample_id: str
    value: float


class SampleValidator(Protocol):
    def validate(self, sample_id: str, value: float) -> None: ...


class MeasurementProcessor(Protocol):
    def process(self, measurement: Measurement) -> Measurement: ...


class ResultReporter(Protocol):
    def report(self, measurements: list[Measurement]) -> str: ...


class RangeValidator:
    """Owned component: purely local validation policy, no external state."""

    def __init__(self, minimum: float, maximum: float) -> None:
        self._minimum = minimum
        self._maximum = maximum

    def validate(self, sample_id: str, value: float) -> None:
        if not (self._minimum <= value <= self._maximum):
            raise SampleRejectedError(
                f"{sample_id}={value} outside [{self._minimum}, {self._maximum}]"
            )


class ScalingProcessor:
    def __init__(self, factor: float) -> None:
        self._factor = factor

    def process(self, measurement: Measurement) -> Measurement:
        return Measurement(measurement.sample_id, measurement.value * self._factor)


class SummaryReporter:
    def report(self, measurements: list[Measurement]) -> str:
        if not measurements:
            return "No measurements recorded."
        total = sum(m.value for m in measurements)
        return f"{len(measurements)} samples, total={total:.2f}"


class ExperimentPipeline:
    """Composed of three independently testable parts.

    - Owns its own list of processed measurements (exclusive lifecycle:
      the history disappears with the pipeline).
    - The validator/processor/reporter are still injected because they
      represent *policy* the caller should control, while the measurement
      history is *pipeline-internal state* the caller should not manage.

    This distinguishes composition (strong ownership of the history list)
    from dependency injection of swappable strategies -- both patterns can
    coexist inside one composed object.
    """

    def __init__(
        self,
        validator: SampleValidator,
        processor: MeasurementProcessor,
        reporter: ResultReporter,
    ) -> None:
        self._validator = validator
        self._processor = processor
        self._reporter = reporter
        self._history: list[Measurement] = []  # owned, exclusive lifecycle

    def submit(self, sample_id: str, raw_value: float) -> None:
        self._validator.validate(sample_id, raw_value)
        processed = self._processor.process(Measurement(sample_id, raw_value))
        self._history.append(processed)

    def summarize(self) -> str:
        return self._reporter.report(self._history)


class IndustryComposition:
    @staticmethod
    def run() -> None:
        pipeline = ExperimentPipeline(
            validator=RangeValidator(minimum=0.0, maximum=100.0),
            processor=ScalingProcessor(factor=1.05),
            reporter=SummaryReporter(),
        )

        pipeline.submit("LEAF-10", 42.0)
        pipeline.submit("LEAF-11", 55.5)

        try:
            pipeline.submit("LEAF-12", 250.0)
        except SampleRejectedError as exc:
            print("Rejected:", exc)

        print(pipeline.summarize())


if __name__ == "__main__":
    UniversityComposition.run()
    InterviewComposition.run()
    IndustryComposition.run()
