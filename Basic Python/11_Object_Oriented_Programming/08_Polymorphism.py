"""
08_Polymorphism.py

Concept: Polymorphism
Polymorphism lets different objects respond to the same operation with
their own implementation, so calling code can treat them uniformly. This
file progresses from a single overridden method to clean, duck-typed
polymorphism that avoids explicit type checks.
"""

from __future__ import annotations


# --------------------------------------------------------------------------- #
# University Level
# --------------------------------------------------------------------------- #
class UniversityPolymorphism:
    """Base class with a method meant to be overridden."""

    def sound_of_growth(self) -> str:
        return "..."

    @staticmethod
    def run() -> None:
        print("--- UniversityPolymorphism ---")

        class FastGrowingPlant(UniversityPolymorphism):
            def sound_of_growth(self) -> str:
                return "rapid rustling"

        class SlowGrowingPlant(UniversityPolymorphism):
            def sound_of_growth(self) -> str:
                return "barely audible"

        for plant in (FastGrowingPlant(), SlowGrowingPlant()):
            print(plant.sound_of_growth())


# --------------------------------------------------------------------------- #
# Interview Level
# --------------------------------------------------------------------------- #
class InterviewPolymorphism:
    """Common base defining a shared operation; subclasses process
    different sample types through the same interface."""

    def analyze(self) -> str:
        raise NotImplementedError

    @staticmethod
    def run() -> None:
        print("--- InterviewPolymorphism ---")

        class DNASample(InterviewPolymorphism):
            def __init__(self, sequence: str) -> None:
                self.sequence = sequence.upper()

            def analyze(self) -> str:
                gc = sum(1 for b in self.sequence if b in "GC")
                pct = (gc / len(self.sequence) * 100) if self.sequence else 0.0
                return f"DNA sample: GC content {pct:.1f}%"

        class ProteinSample(InterviewPolymorphism):
            def __init__(self, residues: str) -> None:
                self.residues = residues.upper()

            def analyze(self) -> str:
                return f"Protein sample: {len(self.residues)} residues"

        samples: list[InterviewPolymorphism] = [
            DNASample("ACGTACGT"),
            ProteinSample("MKTAYIAKQR"),
        ]

        for sample in samples:
            # Calling code uses one interface; it never checks concrete type.
            print(sample.analyze())


# --------------------------------------------------------------------------- #
# Industry Level
# --------------------------------------------------------------------------- #
class _AnalysisStrategy:
    """Common interface implemented by every concrete analysis strategy."""

    def analyze(self, payload: str) -> float:
        raise NotImplementedError


class _GCContentStrategy(_AnalysisStrategy):
    def analyze(self, payload: str) -> float:
        sequence = payload.upper()
        if not sequence:
            return 0.0
        gc = sum(1 for base in sequence if base in "GC")
        return round(gc / len(sequence) * 100.0, 2)


class _MeanResidueHydrophobicityStrategy(_AnalysisStrategy):
    _HYDROPHOBIC = set("AVLIPFMW")

    def analyze(self, payload: str) -> float:
        residues = payload.upper()
        if not residues:
            return 0.0
        hydrophobic_count = sum(1 for r in residues if r in self._HYDROPHOBIC)
        return round(hydrophobic_count / len(residues) * 100.0, 2)


class IndustryPolymorphism:
    """Demonstrates clean polymorphism: the calling code (run_pipeline)
    never needs isinstance() checks to know which strategy it is using,
    it only relies on the shared analyze() contract.
    """

    def __init__(self) -> None:
        self._strategies: dict[str, _AnalysisStrategy] = {
            "gc_content": _GCContentStrategy(),
            "hydrophobicity": _MeanResidueHydrophobicityStrategy(),
        }

    def run_pipeline(self, strategy_name: str, payload: str) -> float:
        if strategy_name not in self._strategies:
            raise KeyError(f"unknown strategy '{strategy_name}'")
        strategy = self._strategies[strategy_name]
        return strategy.analyze(payload)

    @staticmethod
    def run() -> None:
        print("--- IndustryPolymorphism ---")
        pipeline = IndustryPolymorphism()

        gc_result = pipeline.run_pipeline("gc_content", "ACGTGGCCAA")
        hydro_result = pipeline.run_pipeline("hydrophobicity", "MKTAYIAKQRQISFVK")

        print(f"GC content result: {gc_result}%")
        print(f"Hydrophobicity result: {hydro_result}%")


if __name__ == "__main__":
    UniversityPolymorphism.run()
    InterviewPolymorphism.run()
    IndustryPolymorphism.run()
