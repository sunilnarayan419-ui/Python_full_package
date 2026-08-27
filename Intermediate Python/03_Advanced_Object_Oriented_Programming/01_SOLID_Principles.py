from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Protocol


# ============================================================
# UNIVERSITY LEVEL
# ============================================================
# Goal: understand each SOLID letter as an isolated, minimal example.


@dataclass
class UniSample:
    """A single biological sample. (SRP: only holds sample data.)"""

    sample_id: str
    concentration_ng_ul: float


class UniSampleValidator:
    """Single Responsibility: validates samples, nothing else."""

    def is_valid(self, sample: UniSample) -> bool:
        return sample.concentration_ng_ul > 0


class UniShape(ABC):
    """Open/Closed: new shapes extend behavior without modifying this class."""

    @abstractmethod
    def area(self) -> float: ...


class UniCircularWell(UniShape):
    def __init__(self, radius_mm: float) -> None:
        self.radius_mm = radius_mm

    def area(self) -> float:
        return 3.14159 * self.radius_mm**2


class UniSquareWell(UniShape):
    def __init__(self, side_mm: float) -> None:
        self.side_mm = side_mm

    def area(self) -> float:
        return self.side_mm**2


class UniInstrument(ABC):
    """Liskov Substitution: any subclass must be usable wherever UniInstrument is expected."""

    @abstractmethod
    def measure(self) -> float: ...


class UniThermometer(UniInstrument):
    def measure(self) -> float:
        return 37.0


class UniPhMeter(UniInstrument):
    def measure(self) -> float:
        return 7.4


class UniReadable(Protocol):
    def read(self) -> float: ...


class UniWritable(Protocol):
    """Interface Segregation: writers aren't forced to implement read()."""

    def write(self, value: float) -> None: ...


class UniSensor:
    """Implements only the narrow interface it actually needs."""

    def __init__(self) -> None:
        self._value = 0.0

    def read(self) -> float:
        return self._value


class UniHighLevelAnalyzer:
    """Dependency Inversion: depends on an abstraction, not a concrete class."""

    def __init__(self, sensor: UniReadable) -> None:
        self._sensor = sensor

    def analyze(self) -> float:
        return self._sensor.read()


class UniversitySOLID:
    """Demonstrates each SOLID principle with a small, isolated example."""

    @staticmethod
    def run() -> None:
        sample = UniSample("S-001", 12.5)
        print("SRP valid sample:", UniSampleValidator().is_valid(sample))

        shapes: list[UniShape] = [UniCircularWell(4.0), UniSquareWell(3.0)]
        print("OCP areas:", [round(s.area(), 2) for s in shapes])

        instruments: list[UniInstrument] = [UniThermometer(), UniPhMeter()]
        print("LSP readings:", [i.measure() for i in instruments])

        print("ISP sensor read:", UniSensor().read())

        analyzer = UniHighLevelAnalyzer(UniSensor())
        print("DIP analysis:", analyzer.analyze())


# ============================================================
# INTERVIEW LEVEL
# ============================================================
# Goal: take a realistic scientific processing flow, spot SOLID violations,
# and redesign it. Trade-off discussion is embedded in comments.


class IvProcessingError(ValueError):
    """Raised when a sample cannot be processed."""


@dataclass
class IvSample:
    sample_id: str
    concentration_ng_ul: float


# --- VIOLATION SKETCH (kept only as documentation, not instantiated) ---
# class GodExperimentManager:
#     """Violates SRP (validation+processing+reporting+storage all in one),
#     violates OCP (new processing types require editing this class),
#     violates DIP (directly instantiates a concrete database class)."""
#     ...


class IvSampleValidator:
    """SRP: validation only."""

    def validate(self, sample: IvSample) -> None:
        if sample.concentration_ng_ul <= 0:
            raise IvProcessingError(f"Invalid concentration for {sample.sample_id}")


class IvProcessingStrategy(Protocol):
    """DIP + OCP: new processing algorithms plug in without touching callers."""

    def process(self, sample: IvSample) -> float: ...


class IvNormalizationProcessing:
    def process(self, sample: IvSample) -> float:
        return sample.concentration_ng_ul / 100.0


class IvDilutionProcessing:
    def process(self, sample: IvSample) -> float:
        return sample.concentration_ng_ul * 0.5


class IvReporter(Protocol):
    """ISP: reporting is a narrow, separate contract from storage."""

    def report(self, sample_id: str, result: float) -> str: ...


class IvConsoleReporter:
    def report(self, sample_id: str, result: float) -> str:
        return f"[REPORT] {sample_id} -> {result:.2f}"


class IvSampleRepository(Protocol):
    """DIP: persistence is an abstraction the service depends on."""

    def save(self, sample_id: str, result: float) -> None: ...


class IvInMemoryRepository:
    def __init__(self) -> None:
        self._store: dict[str, float] = {}

    def save(self, sample_id: str, result: float) -> None:
        self._store[sample_id] = result

    def all_results(self) -> dict[str, float]:
        return dict(self._store)


class IvExperimentService:
    """Composed from narrow collaborators instead of doing everything itself.

    Why better than the naive alternative? Each collaborator can be unit
    tested and swapped independently (e.g. swap IvInMemoryRepository for a
    SQL-backed one) without touching validation, processing, or reporting.
    """

    def __init__(
        self,
        validator: IvSampleValidator,
        strategy: IvProcessingStrategy,
        reporter: IvReporter,
        repository: IvSampleRepository,
    ) -> None:
        self._validator = validator
        self._strategy = strategy
        self._reporter = reporter
        self._repository = repository

    def run_sample(self, sample: IvSample) -> str:
        self._validator.validate(sample)
        result = self._strategy.process(sample)
        self._repository.save(sample.sample_id, result)
        return self._reporter.report(sample.sample_id, result)


class InterviewSOLID:
    """Realistic scientific processing system redesigned around SOLID."""

    @staticmethod
    def run() -> None:
        repo = IvInMemoryRepository()
        service = IvExperimentService(
            validator=IvSampleValidator(),
            strategy=IvNormalizationProcessing(),
            reporter=IvConsoleReporter(),
            repository=repo,
        )
        print(service.run_sample(IvSample("S-100", 250.0)))

        try:
            service.run_sample(IvSample("S-101", -5.0))
        except IvProcessingError as exc:
            print("Rejected:", exc)

        print("Stored results:", repo.all_results())


# ============================================================
# INDUSTRY LEVEL
# ============================================================
# Goal: a cohesive scientific processing architecture where the five
# principles emerge naturally from good boundaries, not from labeling.


class SampleState(Enum):
    RECEIVED = auto()
    PROCESSED = auto()
    REPORTED = auto()


class InvalidSampleError(ValueError):
    """Raised when a Sample fails domain validation."""


class ProcessingFailureError(RuntimeError):
    """Raised when a Processor cannot produce a result."""


@dataclass(frozen=True, slots=True)
class Sample:
    """Immutable domain object: a physical/biological sample under study."""

    sample_id: str
    concentration_ng_ul: float
    origin: str = "unknown"

    def __post_init__(self) -> None:
        if self.concentration_ng_ul <= 0:
            raise InvalidSampleError(
                f"Sample {self.sample_id} has non-positive concentration"
            )


@dataclass(frozen=True, slots=True)
class ProcessingResult:
    sample_id: str
    value: float
    state: SampleState = SampleState.PROCESSED


class Processor(Protocol):
    """DIP: the pipeline depends on this abstraction, never a concrete algorithm."""

    def process(self, sample: Sample) -> ProcessingResult: ...


class NormalizationProcessor:
    def process(self, sample: Sample) -> ProcessingResult:
        if sample.concentration_ng_ul > 10_000:
            raise ProcessingFailureError(f"{sample.sample_id} out of assay range")
        return ProcessingResult(sample.sample_id, sample.concentration_ng_ul / 100.0)


class DilutionProcessor:
    def process(self, sample: Sample) -> ProcessingResult:
        return ProcessingResult(sample.sample_id, sample.concentration_ng_ul * 0.5)


class Reporter(Protocol):
    """ISP: reporting is decoupled from storage and processing."""

    def build_report(self, result: ProcessingResult) -> str: ...


class ScientificReporter:
    def build_report(self, result: ProcessingResult) -> str:
        return f"Sample {result.sample_id}: {result.value:.3f} ({result.state.name})"


class ResultStorage(Protocol):
    """DIP: storage abstraction; concrete backend is an implementation detail."""

    def persist(self, result: ProcessingResult) -> None: ...

    def fetch(self, sample_id: str) -> ProcessingResult | None: ...


class InMemoryResultStorage:
    def __init__(self) -> None:
        self._results: dict[str, ProcessingResult] = {}

    def persist(self, result: ProcessingResult) -> None:
        self._results[result.sample_id] = result

    def fetch(self, sample_id: str) -> ProcessingResult | None:
        return self._results.get(sample_id)


@dataclass
class ExperimentPipeline:
    """Coordinates Sample -> Processor -> Reporter -> Storage.

    Each collaborator is injected (DIP), each has one job (SRP), new
    Processor/Reporter/Storage implementations can be added without
    modifying this class (OCP), and any Processor/Reporter/ResultStorage
    implementation is substitutable for another (LSP) because they share
    the same narrow Protocol (ISP).
    """

    processor: Processor
    reporter: Reporter
    storage: ResultStorage
    processed: int = field(default=0, init=False)

    def run(self, sample: Sample) -> str:
        result = self.processor.process(sample)
        self.storage.persist(result)
        self.processed += 1
        return self.reporter.build_report(result)


class IndustrySOLID:
    """A small but genuinely cohesive SOLID-driven processing architecture."""

    @staticmethod
    def run() -> None:
        storage = InMemoryResultStorage()
        pipeline = ExperimentPipeline(
            processor=NormalizationProcessor(),
            reporter=ScientificReporter(),
            storage=storage,
        )

        for sample in (
            Sample("S-200", 480.0, origin="greenhouse-A"),
            Sample("S-201", 15.5, origin="greenhouse-B"),
        ):
            print(pipeline.run(sample))

        try:
            Sample("S-202", -1.0)
        except InvalidSampleError as exc:
            print("Rejected:", exc)

        fetched = storage.fetch("S-200")
        print("Fetched:", fetched)
        print("Total processed:", pipeline.processed)


if __name__ == "__main__":
    UniversitySOLID.run()
    InterviewSOLID.run()
    IndustrySOLID.run()
