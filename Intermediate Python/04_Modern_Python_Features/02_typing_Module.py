from __future__ import annotations

from typing import Callable, Final, Literal, Protocol, TypedDict


class UniversityTypingModule:
    """Introduce a few useful typing utilities: TypedDict for
    structured lab records and Literal for constrained status values.
    """

    class SampleRecord(TypedDict):
        sample_id: str
        ph_level: float
        status: Literal["pending", "processed", "failed"]

    @staticmethod
    def describe_record(record: "UniversityTypingModule.SampleRecord") -> str:
        """Time: O(1)."""
        return f"{record['sample_id']}: pH={record['ph_level']} ({record['status']})"

    @staticmethod
    def run() -> None:
        record: UniversityTypingModule.SampleRecord = {
            "sample_id": "S001",
            "ph_level": 6.8,
            "status": "processed",
        }
        print("University:", UniversityTypingModule.describe_record(record))


class UnsupportedInstrumentError(ValueError):
    """Raised when an instrument reading type is not recognized."""


class Measurable(Protocol):
    """Structural protocol: anything exposing to_concentration() qualifies,
    without needing explicit inheritance (duck typing made type-safe)."""

    def to_concentration(self) -> float: ...


class RawSensorReading:
    def __init__(self, millivolts: float) -> None:
        self.millivolts = millivolts

    def to_concentration(self) -> float:
        return self.millivolts / 100.0


class CalibratedReading:
    def __init__(self, concentration: float) -> None:
        self.concentration = concentration

    def to_concentration(self) -> float:
        return self.concentration


class InterviewTypingModule:
    """Combine multiple typing constructs - Protocol, Literal, and
    Callable - in a practical instrument-reading normalization problem.
    """

    ReadingKind = Literal["raw", "calibrated"]

    @staticmethod
    def normalize(reading: Measurable) -> float:
        """Accept anything satisfying the Measurable protocol.

        Time: O(1)
        """
        return reading.to_concentration()

    @staticmethod
    def build_reading(kind: "InterviewTypingModule.ReadingKind", value: float) -> Measurable:
        """Time: O(1). Raises UnsupportedInstrumentError for unknown kinds."""
        match kind:
            case "raw":
                return RawSensorReading(value)
            case "calibrated":
                return CalibratedReading(value)
            case _:
                raise UnsupportedInstrumentError(f"unknown reading kind: {kind}")

    @staticmethod
    def run() -> None:
        raw = InterviewTypingModule.build_reading("raw", 620.0)
        calibrated = InterviewTypingModule.build_reading("calibrated", 5.9)
        print("Interview: raw normalized ->", InterviewTypingModule.normalize(raw))
        print("Interview: calibrated normalized ->", InterviewTypingModule.normalize(calibrated))

        try:
            InterviewTypingModule.build_reading("unknown", 1.0)  # type: ignore[arg-type]
        except UnsupportedInstrumentError as error:
            print("Interview: validation caught ->", error)


type ExperimentId = str


class ExperimentSummary(TypedDict):
    experiment_id: ExperimentId
    sample_count: int
    mean_value: float


class IndustryTypingModule:
    """A reusable typed scientific processing interface combining
    Final constants, TypedDict result contracts, and Callable-based
    pluggable aggregation strategies.
    """

    MAX_SAMPLES_PER_EXPERIMENT: Final[int] = 10_000

    def __init__(self) -> None:
        self._experiments: dict[ExperimentId, list[float]] = {}

    def add_reading(self, experiment_id: ExperimentId, value: float) -> None:
        """Time: O(1) amortized. Raises OverflowError beyond the per-
        experiment sample cap."""
        readings = self._experiments.setdefault(experiment_id, [])
        if len(readings) >= self.MAX_SAMPLES_PER_EXPERIMENT:
            raise OverflowError(
                f"experiment {experiment_id} exceeded {self.MAX_SAMPLES_PER_EXPERIMENT} samples"
            )
        readings.append(value)

    def summarize(
        self,
        experiment_id: ExperimentId,
        aggregator: Callable[[list[float]], float] = lambda values: sum(values) / len(values),
    ) -> ExperimentSummary:
        """Summarize an experiment using a pluggable aggregation function.

        Time: O(n)
        Raises KeyError if the experiment has no recorded readings.
        """
        readings = self._experiments.get(experiment_id)
        if not readings:
            raise KeyError(f"no readings recorded for experiment {experiment_id}")
        return {
            "experiment_id": experiment_id,
            "sample_count": len(readings),
            "mean_value": aggregator(readings),
        }

    @staticmethod
    def run() -> None:
        processor = IndustryTypingModule()
        for value in [4.1, 4.5, 3.9, 4.7]:
            processor.add_reading("EXP-001", value)

        summary = processor.summarize("EXP-001")
        print("Industry: experiment summary ->", summary)

        max_summary = processor.summarize("EXP-001", aggregator=max)
        print("Industry: max-based summary ->", max_summary)


if __name__ == "__main__":
    UniversityTypingModule.run()
    InterviewTypingModule.run()
    IndustryTypingModule.run()
