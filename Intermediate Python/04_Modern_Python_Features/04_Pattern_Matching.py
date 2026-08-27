from __future__ import annotations

from dataclasses import dataclass


class UniversityPatternMatching:
    """Simple scientific record classification using match/case with
    literal and wildcard patterns."""

    @staticmethod
    def classify_ph(ph_level: float) -> str:
        """Time: O(1)."""
        match round(ph_level):
            case 7:
                return "neutral"
            case value if value < 7:
                return "acidic"
            case _:
                return "basic"

    @staticmethod
    def run() -> None:
        for ph in [4.2, 7.0, 9.8]:
            print(f"University: pH {ph} ->", UniversityPatternMatching.classify_ph(ph))


class InterviewPatternMatching:
    """Handle multiple structured input cases and edge cases using
    sequence and mapping patterns over heterogeneous lab event payloads."""

    @staticmethod
    def handle_event(event: object) -> str:
        """Time: O(1).

        Sequence patterns match tuples/lists by shape; mapping patterns
        match dict keys. Guards add extra conditions to a case.
        """
        match event:
            case {"type": "reading", "sample_id": str(sample_id), "value": float(value)} if value < 0:
                return f"invalid negative reading for {sample_id}"
            case {"type": "reading", "sample_id": str(sample_id), "value": float(value)}:
                return f"reading recorded for {sample_id}: {value}"
            case {"type": "alert" | "warning", "message": str(message)}:
                return f"attention: {message}"
            case (sample_id, value) if isinstance(sample_id, str) and isinstance(value, (int, float)):
                return f"legacy tuple reading for {sample_id}: {value}"
            case []:
                return "empty event batch"
            case _:
                return "unrecognized event"

    @staticmethod
    def run() -> None:
        events: list[object] = [
            {"type": "reading", "sample_id": "S001", "value": 5.6},
            {"type": "reading", "sample_id": "S002", "value": -1.0},
            {"type": "warning", "message": "instrument drift detected"},
            ("S003", 7.2),
            [],
            {"type": "unknown"},
        ]
        for event in events:
            print("Interview:", InterviewPatternMatching.handle_event(event))


@dataclass(frozen=True, slots=True)
class SampleReceived:
    sample_id: str
    volume_ml: float


@dataclass(frozen=True, slots=True)
class AssayCompleted:
    sample_id: str
    result_value: float
    passed_qc: bool


@dataclass(frozen=True, slots=True)
class InstrumentFault:
    instrument_id: str
    error_code: int


ExperimentEvent = SampleReceived | AssayCompleted | InstrumentFault


class UnhandledEventError(ValueError):
    """Raised when an experiment event type is not recognized."""


class IndustryPatternMatching:
    """Uses class patterns to classify and route strongly typed
    experiment-event objects in a realistic event-processing pipeline -
    pattern matching here replaces a brittle chain of isinstance checks
    with a single, exhaustive, readable dispatch point.
    """

    @staticmethod
    def route_event(event: ExperimentEvent) -> str:
        """Time: O(1). Raises UnhandledEventError for unknown event types."""
        match event:
            case SampleReceived(sample_id=sample_id, volume_ml=volume_ml) if volume_ml <= 0:
                return f"REJECTED: {sample_id} has non-positive volume {volume_ml}"
            case SampleReceived(sample_id=sample_id, volume_ml=volume_ml):
                return f"ACCEPTED: {sample_id} received with {volume_ml}mL"
            case AssayCompleted(sample_id=sample_id, passed_qc=True, result_value=result_value):
                return f"PASSED: {sample_id} completed with result {result_value}"
            case AssayCompleted(sample_id=sample_id, passed_qc=False):
                return f"FAILED_QC: {sample_id} did not pass quality control"
            case InstrumentFault(instrument_id=instrument_id, error_code=error_code):
                return f"FAULT: instrument {instrument_id} raised error {error_code}"
            case _:
                raise UnhandledEventError(f"unrecognized event: {event!r}")

    @staticmethod
    def run() -> None:
        events: list[ExperimentEvent] = [
            SampleReceived("S101", volume_ml=2.5),
            SampleReceived("S102", volume_ml=0.0),
            AssayCompleted("S101", result_value=0.87, passed_qc=True),
            AssayCompleted("S103", result_value=0.12, passed_qc=False),
            InstrumentFault("SEQ-9000", error_code=42),
        ]
        for event in events:
            print("Industry:", IndustryPatternMatching.route_event(event))


if __name__ == "__main__":
    UniversityPatternMatching.run()
    InterviewPatternMatching.run()
    IndustryPatternMatching.run()
