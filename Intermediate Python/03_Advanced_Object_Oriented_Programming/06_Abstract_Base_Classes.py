from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


# ============================================================
# UNIVERSITY LEVEL
# ============================================================
# Goal: understand what an abstract method/class means.


class UniScientificProcessor(ABC):
    """Cannot be instantiated directly; forces subclasses to implement process()."""

    @abstractmethod
    def process(self, raw_value: float) -> float: ...


class UniDoublingProcessor(UniScientificProcessor):
    def process(self, raw_value: float) -> float:
        return raw_value * 2.0


class UniversityAbstractBaseClasses:
    @staticmethod
    def run() -> None:
        processor: UniScientificProcessor = UniDoublingProcessor()
        print("Processed:", processor.process(5.0))

        try:
            UniScientificProcessor()  # type: ignore[abstract]
        except TypeError as exc:
            print("Cannot instantiate ABC directly:", exc)


# ============================================================
# INTERVIEW LEVEL
# ============================================================
# Goal: multiple concrete implementations sharing a common contract and
# some shared (template-method-style) behavior.


class IvAssayProcessor(ABC):
    """Shares a concrete workflow method while delegating the
    algorithm-specific step to subclasses (a light template method)."""

    def run(self, raw_value: float) -> str:
        if raw_value < 0:
            raise ValueError("raw_value must be non-negative")
        result = self._transform(raw_value)
        return f"{self.name()}: {result:.2f}"

    @abstractmethod
    def _transform(self, raw_value: float) -> float: ...

    @abstractmethod
    def name(self) -> str: ...


class IvPCRAssayProcessor(IvAssayProcessor):
    def _transform(self, raw_value: float) -> float:
        return raw_value * 1.5

    def name(self) -> str:
        return "PCR"


class IvProteinAssayProcessor(IvAssayProcessor):
    def _transform(self, raw_value: float) -> float:
        return raw_value**0.5

    def name(self) -> str:
        return "Protein"


class InterviewAbstractBaseClasses:
    @staticmethod
    def run() -> None:
        processors: list[IvAssayProcessor] = [
            IvPCRAssayProcessor(),
            IvProteinAssayProcessor(),
        ]
        for processor in processors:
            print(processor.run(16.0))  # polymorphic dispatch

        try:
            processors[0].run(-1.0)
        except ValueError as exc:
            print("Rejected:", exc)


# ============================================================
# INDUSTRY LEVEL
# ============================================================
# Goal: a meaningful abstract domain service where inheritance is
# justified because subclasses share real invariants and a real
# algorithmic skeleton -- not used merely to demonstrate ABC syntax.


class SequencingError(RuntimeError):
    """Raised when a sequencing run cannot complete."""


@dataclass(frozen=True, slots=True)
class SequencingRun:
    run_id: str
    raw_reads: int


@dataclass(frozen=True, slots=True)
class SequencingResult:
    run_id: str
    aligned_reads: int
    quality_score: float


class SequencingPipeline(ABC):
    """Abstract because every real sequencing platform (short-read,
    long-read, ...) shares the same quality-control -> alignment ->
    scoring skeleton, but differs in how each step is implemented.
    Inheritance is justified here: subclasses genuinely are-a
    SequencingPipeline and must satisfy the same contract (Liskov
    substitutability) so client code can treat any platform uniformly.
    """

    def execute(self, run: SequencingRun) -> SequencingResult:
        self._validate(run)
        filtered_reads = self._quality_control(run.raw_reads)
        aligned = self._align(filtered_reads)
        score = self._score(aligned, run.raw_reads)
        return SequencingResult(run.run_id, aligned, score)

    def _validate(self, run: SequencingRun) -> None:
        if run.raw_reads <= 0:
            raise SequencingError(f"{run.run_id} has no raw reads")

    @abstractmethod
    def _quality_control(self, raw_reads: int) -> int:
        """Filter out low-quality reads; platform-specific."""

    @abstractmethod
    def _align(self, filtered_reads: int) -> int:
        """Align surviving reads to a reference; platform-specific."""

    def _score(self, aligned: int, raw_reads: int) -> float:
        """Shared scoring logic -- concrete because it is platform-agnostic."""
        return round(aligned / raw_reads, 3)


class ShortReadPipeline(SequencingPipeline):
    """High-throughput, high quality-loss short-read platform."""

    def _quality_control(self, raw_reads: int) -> int:
        return int(raw_reads * 0.85)

    def _align(self, filtered_reads: int) -> int:
        return int(filtered_reads * 0.95)


class LongReadPipeline(SequencingPipeline):
    """Lower throughput, higher per-read quality long-read platform."""

    def _quality_control(self, raw_reads: int) -> int:
        return int(raw_reads * 0.95)

    def _align(self, filtered_reads: int) -> int:
        return int(filtered_reads * 0.80)


class IndustryAbstractBaseClasses:
    @staticmethod
    def run() -> None:
        pipelines: list[SequencingPipeline] = [ShortReadPipeline(), LongReadPipeline()]
        run = SequencingRun("RUN-01", raw_reads=1_000_000)

        for pipeline in pipelines:
            result = pipeline.execute(run)
            print(
                f"{type(pipeline).__name__}: aligned={result.aligned_reads}, "
                f"quality={result.quality_score}"
            )

        try:
            pipelines[0].execute(SequencingRun("RUN-02", raw_reads=0))
        except SequencingError as exc:
            print("Rejected:", exc)


if __name__ == "__main__":
    UniversityAbstractBaseClasses.run()
    InterviewAbstractBaseClasses.run()
    IndustryAbstractBaseClasses.run()
