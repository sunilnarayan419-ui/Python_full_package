from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


# ============================================================
# UNIVERSITY LEVEL
# ============================================================
# Goal: understand constructor injection vs internal instantiation.


class UniDataProcessor:
    def process(self, raw_value: float) -> float:
        return raw_value * 2.0


class UniExperimentService:
    """The processor is injected through the constructor rather than
    created inside the class -- the service does not need to know HOW
    to build a processor, only that it can call .process()."""

    def __init__(self, processor: UniDataProcessor) -> None:
        self._processor = processor

    def run_experiment(self, raw_value: float) -> float:
        return self._processor.process(raw_value)


class UniversityDependencyInjection:
    @staticmethod
    def run() -> None:
        service = UniExperimentService(UniDataProcessor())
        print("Result:", service.run_experiment(21.0))


# ============================================================
# INTERVIEW LEVEL
# ============================================================
# Goal: inject interchangeable providers/processors via a Protocol, and
# discuss testability with a fake implementation.


class IvDataProvider(Protocol):
    """Abstraction: any object exposing get_readings() qualifies."""

    def get_readings(self) -> list[float]: ...


class IvSensorDataProvider:
    def get_readings(self) -> list[float]:
        return [22.1, 22.4, 22.0]  # simulated hardware readings


class IvFakeDataProvider:
    """Test double: lets the service be tested without real hardware."""

    def __init__(self, canned_readings: list[float]) -> None:
        self._canned_readings = canned_readings

    def get_readings(self) -> list[float]:
        return self._canned_readings


class IvAnalysisService:
    """Depends on the IvDataProvider Protocol, not a concrete class.

    Why is this better than instantiating IvSensorDataProvider directly
    inside __init__? Because unit tests can inject IvFakeDataProvider and
    verify the averaging logic deterministically, without touching real
    (and possibly unavailable or non-deterministic) hardware.
    """

    def __init__(self, provider: IvDataProvider) -> None:
        self._provider = provider

    def average_reading(self) -> float:
        readings = self._provider.get_readings()
        if not readings:
            return 0.0
        return sum(readings) / len(readings)


class InterviewDependencyInjection:
    @staticmethod
    def run() -> None:
        live_service = IvAnalysisService(IvSensorDataProvider())
        print("Live average:", round(live_service.average_reading(), 2))

        test_service = IvAnalysisService(IvFakeDataProvider([10.0, 20.0, 30.0]))
        print("Test average:", test_service.average_reading())


# ============================================================
# INDUSTRY LEVEL
# ============================================================
# Goal: a service whose dependencies are fully injected, with real,
# in-memory, and test-double implementations for each collaborator.


class SampleNotFoundError(KeyError):
    """Raised when a sample cannot be located in the repository."""


@dataclass(frozen=True, slots=True)
class Sample:
    sample_id: str
    concentration_ng_ul: float


@dataclass(frozen=True, slots=True)
class AnalysisReport:
    sample_id: str
    score: float
    summary: str


class SampleRepository(Protocol):
    def get(self, sample_id: str) -> Sample: ...

    def all_ids(self) -> list[str]: ...


class Analyzer(Protocol):
    def analyze(self, sample: Sample) -> float: ...


class Reporter(Protocol):
    def build(self, sample: Sample, score: float) -> AnalysisReport: ...


class InMemorySampleRepository:
    """Real (but lightweight) implementation used at runtime."""

    def __init__(self, samples: dict[str, Sample] | None = None) -> None:
        self._samples: dict[str, Sample] = dict(samples or {})

    def add(self, sample: Sample) -> None:
        self._samples[sample.sample_id] = sample

    def get(self, sample_id: str) -> Sample:
        try:
            return self._samples[sample_id]
        except KeyError as exc:
            raise SampleNotFoundError(sample_id) from exc

    def all_ids(self) -> list[str]:
        return list(self._samples.keys())


class ConcentrationAnalyzer:
    def analyze(self, sample: Sample) -> float:
        return round(sample.concentration_ng_ul / 10.0, 3)


class StandardReporter:
    def build(self, sample: Sample, score: float) -> AnalysisReport:
        return AnalysisReport(
            sample_id=sample.sample_id,
            score=score,
            summary=f"{sample.sample_id} scored {score}",
        )


class StubAnalyzer:
    """Test double: returns a fixed score regardless of input, isolating
    ExperimentService tests from real analysis logic."""

    def __init__(self, fixed_score: float) -> None:
        self._fixed_score = fixed_score

    def analyze(self, sample: Sample) -> float:
        return self._fixed_score


@dataclass
class ExperimentService:
    """All collaborators are injected -- none are constructed internally.

    This lets callers assemble the service with:
      - real implementations in production,
      - in-memory implementations in integration tests,
      - stub/fake implementations in fast unit tests,
    without ExperimentService ever changing.
    """

    sample_repository: SampleRepository
    analyzer: Analyzer
    reporter: Reporter
    reports_generated: int = field(default=0, init=False)

    def analyze_sample(self, sample_id: str) -> AnalysisReport:
        sample = self.sample_repository.get(sample_id)
        score = self.analyzer.analyze(sample)
        report = self.reporter.build(sample, score)
        self.reports_generated += 1
        return report


class IndustryDependencyInjection:
    @staticmethod
    def run() -> None:
        repo = InMemorySampleRepository()
        repo.add(Sample("S-500", 87.3))
        repo.add(Sample("S-501", 42.0))

        production_service = ExperimentService(
            sample_repository=repo,
            analyzer=ConcentrationAnalyzer(),
            reporter=StandardReporter(),
        )
        report = production_service.analyze_sample("S-500")
        print(report.summary)

        try:
            production_service.analyze_sample("S-999")
        except SampleNotFoundError as exc:
            print("Not found:", exc)

        test_service = ExperimentService(
            sample_repository=repo,
            analyzer=StubAnalyzer(fixed_score=1.0),
            reporter=StandardReporter(),
        )
        print(test_service.analyze_sample("S-501").summary)
        print("Reports generated (prod):", production_service.reports_generated)


if __name__ == "__main__":
    UniversityDependencyInjection.run()
    InterviewDependencyInjection.run()
    IndustryDependencyInjection.run()
