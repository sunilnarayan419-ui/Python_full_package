from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Protocol


# ============================================================
# UNIVERSITY LEVEL
# ============================================================
# Goal: see the smallest possible illustration of a few common patterns,
# conceptually, without building a full system around them.


class UniNotifier(Protocol):
    """Minimal Observer-style contract."""

    def notify(self, message: str) -> None: ...


class UniConsoleNotifier:
    def notify(self, message: str) -> None:
        print(f"[notify] {message}")


class UniAnalysisStrategy(ABC):
    """Minimal Strategy contract."""

    @abstractmethod
    def analyze(self, value: float) -> float: ...


class UniAverageStrategy(UniAnalysisStrategy):
    def analyze(self, value: float) -> float:
        return value  # trivial stand-in


def uni_sample_factory(kind: str) -> str:
    """Minimal Factory-style function: hides which concrete label is built."""
    return {"plant": "PlantSample", "blood": "BloodSample"}.get(kind, "UnknownSample")


class UniversityDesignPatterns:
    @staticmethod
    def run() -> None:
        notifier = UniConsoleNotifier()
        notifier.notify("Experiment started")

        strategy: UniAnalysisStrategy = UniAverageStrategy()
        print("Strategy result:", strategy.analyze(42.0))

        print("Factory built:", uni_sample_factory("plant"))


# ============================================================
# INTERVIEW LEVEL
# ============================================================
# Goal: given a design problem, choose the right pattern and justify it.
#
# PROBLEM: "We need to add new sample-processing algorithms frequently,
# without modifying the class that runs them, and we need to be notified
# whenever processing finishes."
#
# DESIGN PRESSURE: adding an if/elif chain per algorithm violates
# Open/Closed; polling for completion instead of being told about it
# creates tight coupling and wasted cycles.
#
# PATTERN CHOICE: Strategy (swap algorithms) + Observer (react to
# completion) directly address these two pressures.


class IvProcessingStrategy(Protocol):
    def process(self, value: float) -> float: ...


class IvNormalize(IvProcessingStrategy):
    def process(self, value: float) -> float:
        return value / 100.0


class IvAmplify(IvProcessingStrategy):
    def process(self, value: float) -> float:
        return value * 10.0


class IvCompletionObserver(Protocol):
    def on_complete(self, sample_id: str, result: float) -> None: ...


class IvLoggingObserver:
    def on_complete(self, sample_id: str, result: float) -> None:
        print(f"[log] {sample_id} -> {result}")


class IvProcessingService:
    """RESULT: new strategies plug in without editing this class (Strategy
    solves the Open/Closed pressure); observers are notified rather than
    polled (Observer solves the coupling pressure)."""

    def __init__(self, strategy: IvProcessingStrategy) -> None:
        self._strategy = strategy
        self._observers: list[IvCompletionObserver] = []

    def subscribe(self, observer: IvCompletionObserver) -> None:
        self._observers.append(observer)

    def process(self, sample_id: str, value: float) -> float:
        result = self._strategy.process(value)
        for observer in self._observers:
            observer.on_complete(sample_id, result)
        return result


class InterviewDesignPatterns:
    @staticmethod
    def run() -> None:
        service = IvProcessingService(IvNormalize())
        service.subscribe(IvLoggingObserver())
        service.process("S-1", 500.0)

        service_alt = IvProcessingService(IvAmplify())
        service_alt.subscribe(IvLoggingObserver())
        service_alt.process("S-2", 3.0)


# ============================================================
# INDUSTRY LEVEL
# ============================================================
# Goal: one cohesive scientific workflow where Strategy, Factory,
# Observer, and Builder each solve a distinct, real problem -- not
# stacked for their own sake.
#
# PROBLEM -> PRESSURE -> PATTERN -> RESULT
# 1. Different assay types need different scoring algorithms, chosen at
#    runtime -> Strategy.
# 2. Constructing the right processor for a given assay type must not
#    leak concrete classes into client code -> Factory.
# 3. Multiple independent systems (audit log, alerting) must react to a
#    finished assay without the pipeline knowing about them -> Observer.
# 4. Configuring a pipeline run has several optional knobs and must
#    produce a validated, immutable configuration -> Builder.


class AssayType(Protocol):
    ...  # marker only; real discriminator is the AssayKind enum below


from enum import Enum, auto  # noqa: E402  (grouped here for readability)


class AssayKind(Enum):
    PCR = auto()
    PROTEIN = auto()


class ScoringStrategy(Protocol):
    """Problem 1: interchangeable scoring algorithms."""

    def score(self, raw_value: float) -> float: ...


class PCRScoring:
    def score(self, raw_value: float) -> float:
        return round(raw_value * 1.2, 2)


class ProteinScoring:
    def score(self, raw_value: float) -> float:
        return round(raw_value**0.5, 2)


class AssayProcessor(ABC):
    def __init__(self, strategy: ScoringStrategy) -> None:
        self._strategy = strategy

    def run(self, raw_value: float) -> float:
        return self._strategy.score(raw_value)


class PCRAssayProcessor(AssayProcessor):
    def __init__(self) -> None:
        super().__init__(PCRScoring())


class ProteinAssayProcessor(AssayProcessor):
    def __init__(self) -> None:
        super().__init__(ProteinScoring())


class AssayProcessorFactory:
    """Problem 2: clients ask for a processor by kind and never see the
    concrete PCRAssayProcessor/ProteinAssayProcessor classes directly."""

    _registry: dict[AssayKind, type[AssayProcessor]] = {
        AssayKind.PCR: PCRAssayProcessor,
        AssayKind.PROTEIN: ProteinAssayProcessor,
    }

    @classmethod
    def create(cls, kind: AssayKind) -> AssayProcessor:
        try:
            return cls._registry[kind]()
        except KeyError as exc:
            raise ValueError(f"Unsupported assay kind: {kind}") from exc


class AssayCompletionObserver(Protocol):
    """Problem 3: reactive, decoupled subscribers."""

    def on_assay_complete(self, sample_id: str, score: float) -> None: ...


class AuditLogger:
    def on_assay_complete(self, sample_id: str, score: float) -> None:
        print(f"[audit] {sample_id} scored {score}")


class AlertHandler:
    def __init__(self, threshold: float) -> None:
        self._threshold = threshold

    def on_assay_complete(self, sample_id: str, score: float) -> None:
        if score > self._threshold:
            print(f"[alert] {sample_id} exceeded threshold ({score} > {self._threshold})")


@dataclass(frozen=True, slots=True)
class PipelineConfig:
    """Problem 4: validated, immutable configuration -- see PipelineConfigBuilder."""

    assay_kind: AssayKind
    alert_threshold: float
    label: str


class PipelineConfigBuilder:
    """Fluent builder producing an immutable, validated PipelineConfig."""

    def __init__(self) -> None:
        self._assay_kind: AssayKind | None = None
        self._alert_threshold: float = 100.0  # sensible default
        self._label: str = "unlabeled-run"

    def with_assay_kind(self, kind: AssayKind) -> PipelineConfigBuilder:
        self._assay_kind = kind
        return self

    def with_alert_threshold(self, threshold: float) -> PipelineConfigBuilder:
        self._alert_threshold = threshold
        return self

    def with_label(self, label: str) -> PipelineConfigBuilder:
        self._label = label
        return self

    def build(self) -> PipelineConfig:
        if self._assay_kind is None:
            raise ValueError("assay_kind is required")
        return PipelineConfig(self._assay_kind, self._alert_threshold, self._label)


@dataclass
class AssayWorkflow:
    """Ties the four patterns together around one real workflow."""

    config: PipelineConfig
    observers: list[AssayCompletionObserver] = field(default_factory=list)

    def subscribe(self, observer: AssayCompletionObserver) -> None:
        self.observers.append(observer)

    def execute(self, sample_id: str, raw_value: float) -> float:
        processor = AssayProcessorFactory.create(self.config.assay_kind)
        score = processor.run(raw_value)
        for observer in self.observers:
            observer.on_assay_complete(sample_id, score)
        return score


class IndustryDesignPatterns:
    @staticmethod
    def run() -> None:
        config = (
            PipelineConfigBuilder()
            .with_assay_kind(AssayKind.PCR)
            .with_alert_threshold(50.0)
            .with_label("batch-2026-08")
            .build()
        )

        workflow = AssayWorkflow(config)
        workflow.subscribe(AuditLogger())
        workflow.subscribe(AlertHandler(config.alert_threshold))

        score = workflow.execute("S-900", raw_value=60.0)
        print(f"Final score for {config.label}: {score}")


if __name__ == "__main__":
    UniversityDesignPatterns.run()
    InterviewDesignPatterns.run()
    IndustryDesignPatterns.run()
