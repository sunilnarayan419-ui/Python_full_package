"""
10_Abstraction.py

Concept: Abstraction
Abstraction separates what an object does from how it does it, usually
expressed through an interface or contract that concrete classes must
fulfil. This file progresses from an informal contract to a formal
abstract base class used inside a realistic scientific pipeline.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


# --------------------------------------------------------------------------- #
# University Level
# --------------------------------------------------------------------------- #
class UniversitySequenceAnalyzer:
    """Informal contract: subclasses are expected to implement analyze(),
    but nothing enforces it yet. Used to introduce the *idea* of
    abstraction before introducing ABC."""

    def analyze(self, sequence: str) -> str:
        raise NotImplementedError("Subclasses must implement analyze()")


class UniversityAbstraction:
    """Demonstrates abstraction through a simple, informally-enforced
    contract: callers only need to know that analyze() exists, not how
    each analyzer computes its result."""

    @staticmethod
    def run() -> None:
        print("--- UniversityAbstraction ---")

        class LengthAnalyzer(UniversitySequenceAnalyzer):
            def analyze(self, sequence: str) -> str:
                return f"Length: {len(sequence)}"

        analyzer: UniversitySequenceAnalyzer = LengthAnalyzer()
        print(analyzer.analyze("ACGTACGT"))


# --------------------------------------------------------------------------- #
# Interview Level
# --------------------------------------------------------------------------- #
class ExperimentAnalyzer(ABC):
    """A formal, enforced contract: any subclass that does not implement
    analyze() cannot be instantiated at all."""

    @abstractmethod
    def analyze(self, values: list[float]) -> float:
        """Return a single summary statistic for the given measurements."""


class MeanAnalyzer(ExperimentAnalyzer):
    def analyze(self, values: list[float]) -> float:
        if not values:
            raise ValueError("values cannot be empty")
        return sum(values) / len(values)


class MaxAnalyzer(ExperimentAnalyzer):
    def analyze(self, values: list[float]) -> float:
        if not values:
            raise ValueError("values cannot be empty")
        return max(values)


class InterviewAbstraction:
    """Demonstrates an abstract base class with concrete implementations,
    and shows that the ABC itself cannot be instantiated directly."""

    @staticmethod
    def run() -> None:
        print("--- InterviewAbstraction ---")
        readings = [4.2, 5.6, 3.9, 7.1]

        analyzers: list[ExperimentAnalyzer] = [MeanAnalyzer(), MaxAnalyzer()]
        for analyzer in analyzers:
            print(f"{type(analyzer).__name__}: {analyzer.analyze(readings):.2f}")

        try:
            ExperimentAnalyzer()  # type: ignore[abstract]
        except TypeError as error:
            print(f"Cannot instantiate abstract class: {error}")


# --------------------------------------------------------------------------- #
# Industry Level
# --------------------------------------------------------------------------- #
class MolecularScoringStrategy(ABC):
    """A small, realistic scientific processing interface: every scoring
    strategy accepts a compound's descriptors and returns a single score
    in the range [0.0, 1.0]. Concrete implementations decide how."""

    @abstractmethod
    def score(self, molecular_weight: float, logp: float) -> float:
        """Return a drug-likeness style score between 0.0 and 1.0."""

    def score_batch(self, compounds: list[tuple[float, float]]) -> list[float]:
        """Concrete helper built on top of the abstract contract: shared
        behavior lives here so subclasses only implement score()."""
        return [self.score(mw, logp) for mw, logp in compounds]


class LipinskiScoringStrategy(MolecularScoringStrategy):
    def score(self, molecular_weight: float, logp: float) -> float:
        weight_ok = molecular_weight <= 500.0
        logp_ok = -0.4 <= logp <= 5.6
        return 1.0 if (weight_ok and logp_ok) else 0.0


class WeightedScoringStrategy(MolecularScoringStrategy):
    def score(self, molecular_weight: float, logp: float) -> float:
        weight_component = max(0.0, 1.0 - molecular_weight / 1000.0)
        logp_component = max(0.0, 1.0 - abs(logp - 2.5) / 10.0)
        return round((weight_component + logp_component) / 2.0, 3)


class IndustryAbstraction:
    """Demonstrates using an abstract base class to define a scientific
    processing contract, then relying on the concrete strategy chosen at
    runtime without the caller needing to know its internals."""

    @staticmethod
    def run() -> None:
        print("--- IndustryAbstraction ---")
        compounds = [(320.5, 2.1), (610.0, 4.9), (180.2, 1.0)]

        strategies: list[MolecularScoringStrategy] = [
            LipinskiScoringStrategy(),
            WeightedScoringStrategy(),
        ]

        for strategy in strategies:
            scores = strategy.score_batch(compounds)
            print(f"{type(strategy).__name__}: {scores}")


if __name__ == "__main__":
    UniversityAbstraction.run()
    InterviewAbstraction.run()
    IndustryAbstraction.run()
