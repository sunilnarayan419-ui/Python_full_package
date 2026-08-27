from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Protocol, Sequence


# ============================================================
# UNIVERSITY LEVEL
# ============================================================
# Goal: understand interchangeable algorithms behind a common interface.


class UniAnalysisStrategy(ABC):
    @abstractmethod
    def analyze(self, values: list[float]) -> float: ...


class UniMeanStrategy(UniAnalysisStrategy):
    def analyze(self, values: list[float]) -> float:
        return sum(values) / len(values)


class UniMaxStrategy(UniAnalysisStrategy):
    def analyze(self, values: list[float]) -> float:
        return max(values)


class UniversityStrategy:
    @staticmethod
    def run() -> None:
        values = [2.0, 4.0, 6.0]
        for strategy in (UniMeanStrategy(), UniMaxStrategy()):
            print(f"{type(strategy).__name__}: {strategy.analyze(values)}")


# ============================================================
# INTERVIEW LEVEL
# ============================================================
# Goal: switch algorithms at runtime without modifying the service.


class IvNormalizationStrategy(Protocol):
    def normalize(self, values: list[float]) -> list[float]: ...


class IvMinMaxNormalization:
    def normalize(self, values: list[float]) -> list[float]:
        lo, hi = min(values), max(values)
        span = hi - lo or 1.0
        return [(v - lo) / span for v in values]


class IvZScoreNormalization:
    def normalize(self, values: list[float]) -> list[float]:
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        std = variance**0.5 or 1.0
        return [(v - mean) / std for v in values]


class IvAnalysisService:
    """Depends on the strategy abstraction; swapping strategies requires
    no changes to this class -- only a different constructor argument."""

    def __init__(self, strategy: IvNormalizationStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: IvNormalizationStrategy) -> None:
        self._strategy = strategy

    def run(self, values: list[float]) -> list[float]:
        return [round(v, 3) for v in self._strategy.normalize(values)]


class InterviewStrategy:
    @staticmethod
    def run() -> None:
        values = [10.0, 20.0, 30.0, 40.0]
        service = IvAnalysisService(IvMinMaxNormalization())
        print("MinMax:", service.run(values))

        service.set_strategy(IvZScoreNormalization())  # swapped at runtime
        print("ZScore:", service.run(values))


# ============================================================
# INDUSTRY LEVEL
# ============================================================
# Goal: a pluggable analysis pipeline where the service depends only on
# the strategy abstraction, strategies are independently testable, and
# invalid input produces meaningful exceptions.


class EmptyDatasetError(ValueError):
    """Raised when a strategy is asked to normalize an empty dataset."""


@dataclass(frozen=True, slots=True)
class Measurement:
    sample_id: str
    value: float


class NormalizationStrategy(Protocol):
    """The AnalysisService's only dependency -- concrete algorithms are
    invisible to it, satisfying dependency inversion."""

    def normalize(self, values: Sequence[float]) -> list[float]: ...

    def name(self) -> str: ...


class MeanNormalizationStrategy:
    def normalize(self, values: Sequence[float]) -> list[float]:
        if not values:
            raise EmptyDatasetError("Cannot normalize an empty dataset")
        mean = sum(values) / len(values)
        return [round(v - mean, 4) for v in values]

    def name(self) -> str:
        return "mean"


class ZScoreNormalizationStrategy:
    def normalize(self, values: Sequence[float]) -> list[float]:
        if not values:
            raise EmptyDatasetError("Cannot normalize an empty dataset")
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        std = variance**0.5 or 1.0
        return [round((v - mean) / std, 4) for v in values]

    def name(self) -> str:
        return "z-score"


class RobustNormalizationStrategy:
    """Median/IQR based -- resistant to outliers, unlike mean/z-score."""

    def normalize(self, values: Sequence[float]) -> list[float]:
        if not values:
            raise EmptyDatasetError("Cannot normalize an empty dataset")
        ordered = sorted(values)
        median = ordered[len(ordered) // 2]
        q1 = ordered[len(ordered) // 4]
        q3 = ordered[(3 * len(ordered)) // 4]
        iqr = (q3 - q1) or 1.0
        return [round((v - median) / iqr, 4) for v in values]

    def name(self) -> str:
        return "robust"


@dataclass
class AnalysisService:
    """Pluggable pipeline: the strategy can be swapped per dataset (e.g.
    RobustNormalizationStrategy for outlier-heavy assay batches) without
    any change to this class or its callers."""

    strategy: NormalizationStrategy
    runs_completed: int = field(default=0, init=False)

    def run(self, measurements: Sequence[Measurement]) -> dict[str, float]:
        values = [m.value for m in measurements]
        normalized = self.strategy.normalize(values)
        self.runs_completed += 1
        return {m.sample_id: n for m, n in zip(measurements, normalized)}


class IndustryStrategy:
    @staticmethod
    def run() -> None:
        measurements = [
            Measurement("S-1", 12.0),
            Measurement("S-2", 15.0),
            Measurement("S-3", 400.0),  # outlier
            Measurement("S-4", 14.0),
        ]

        for strategy in (
            MeanNormalizationStrategy(),
            ZScoreNormalizationStrategy(),
            RobustNormalizationStrategy(),
        ):
            service = AnalysisService(strategy)
            print(f"{strategy.name()}: {service.run(measurements)}")

        try:
            AnalysisService(MeanNormalizationStrategy()).run([])
        except EmptyDatasetError as exc:
            print("Rejected:", exc)


if __name__ == "__main__":
    UniversityStrategy.run()
    InterviewStrategy.run()
    IndustryStrategy.run()
