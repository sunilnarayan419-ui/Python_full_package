"""
02_from_import.py

Topic: The `from module import name` statement.

Demonstrates importing specific names to avoid unnecessary namespace
qualification, contrasted with `import module`.
"""

from math import sqrt, log2
from statistics import mean, pstdev
from datetime import datetime


class UniversityFromImport:
    """Introduces `from module import name` for direct name access."""

    @staticmethod
    def run() -> None:
        gene_expression_counts: list[float] = [120.0, 340.0, 95.0, 480.0, 210.0]

        log_transformed = [log2(count + 1) for count in gene_expression_counts]
        average_expression = mean(gene_expression_counts)

        print("University: from module import name")
        print(f"  Raw counts: {gene_expression_counts}")
        print(f"  Log2(count + 1): {[round(v, 2) for v in log_transformed]}")
        print(f"  Mean expression: {average_expression:.2f}")


class InterviewFromImport:
    """Solves a realistic scientific calculation using imported names."""

    @staticmethod
    def _population_variability(values: list[float]) -> float:
        if not values:
            raise ValueError("values must contain at least one measurement.")
        return pstdev(values)

    @staticmethod
    def run() -> None:
        protein_concentrations_ng_ml: list[float] = [2.4, 2.6, 2.1, 2.9, 2.3, 2.7]

        variability = InterviewFromImport._population_variability(protein_concentrations_ng_ml)
        signal_to_noise = mean(protein_concentrations_ng_ml) / sqrt(variability) if variability > 0 else float("inf")

        print("Interview: from module import name")
        print(f"  Concentrations (ng/mL): {protein_concentrations_ng_ml}")
        print(f"  Population stdev: {variability:.3f}")
        print(f"  Signal-to-noise estimate: {signal_to_noise:.2f}")


class IndustryFromImport:
    """Demonstrates disciplined use of selective imports in maintainable code."""

    def __init__(self, compound_id: str, molecular_weights: list[float]) -> None:
        if not compound_id:
            raise ValueError("compound_id must be a non-empty string.")
        if not molecular_weights:
            raise ValueError("molecular_weights must contain at least one value.")
        if any(weight <= 0 for weight in molecular_weights):
            raise ValueError("molecular_weights must all be positive.")

        self._compound_id = compound_id
        self._molecular_weights = molecular_weights
        self._analyzed_at = datetime.now()

    def average_weight(self) -> float:
        return mean(self._molecular_weights)

    def weight_dispersion(self) -> float:
        return pstdev(self._molecular_weights)

    def log_scaled_weights(self) -> list[float]:
        return [round(log2(weight), 3) for weight in self._molecular_weights]

    def report(self) -> str:
        return (
            f"Compound {self._compound_id} | "
            f"avg_weight={self.average_weight():.2f} | "
            f"dispersion={self.weight_dispersion():.3f} | "
            f"analyzed={self._analyzed_at.isoformat(timespec='seconds')}"
        )

    @staticmethod
    def run() -> None:
        molecular_weights_da: list[float] = [342.3, 338.9, 345.1, 340.0, 341.7]

        analyzer = IndustryFromImport("CMP-DRUG-0042", molecular_weights_da)
        print("Industry: from module import name")
        print(f"  {analyzer.report()}")
        print(f"  Log-scaled weights: {analyzer.log_scaled_weights()}")


if __name__ == "__main__":
    UniversityFromImport.run()
    InterviewFromImport.run()
    IndustryFromImport.run()
