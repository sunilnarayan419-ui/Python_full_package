from __future__ import annotations

from collections import Counter


class UniversityCounter:
    """Demonstrates collections.Counter for basic frequency counting."""

    @staticmethod
    def count_species(observations: list[str]) -> Counter[str]:
        return Counter(observations)

    @staticmethod
    def run() -> None:
        observations = ["oak", "maple", "oak", "pine", "oak", "maple"]
        counts = UniversityCounter.count_species(observations)
        print(counts)
        print(f"most common: {counts.most_common(1)}")


class InterviewCounter:
    """Demonstrates Counter arithmetic and comparison operations, showing
    practical use for comparing observed trait distributions between two
    experimental groups."""

    @staticmethod
    def run() -> None:
        control_traits = Counter(["tall", "tall", "short", "tall", "short"])
        treated_traits = Counter(["tall", "short", "short", "short", "short"])

        difference = treated_traits - control_traits
        combined = control_traits + treated_traits
        shared = control_traits & treated_traits

        print(f"control: {control_traits}")
        print(f"treated: {treated_traits}")
        print(f"treated minus control: {difference}")
        print(f"combined totals: {combined}")
        print(f"shared minimum counts: {shared}")


class IndustryCounter:
    """Demonstrates Counter within a codon/gene-annotation analysis
    pipeline: efficient frequency analysis over large sequence data with
    derived statistics built cleanly on top of Counter's interface."""

    class CodonUsageAnalyzer:
        def __init__(self, sequence: str) -> None:
            if len(sequence) % 3 != 0:
                raise ValueError("sequence length must be a multiple of 3")
            self.sequence = sequence.upper()
            self._codon_counts = self._compute_codon_counts()

        def _compute_codon_counts(self) -> Counter[str]:
            codons = [self.sequence[i : i + 3] for i in range(0, len(self.sequence), 3)]
            return Counter(codons)

        def most_common_codons(self, n: int = 3) -> list[tuple[str, int]]:
            return self._codon_counts.most_common(n)

        def codon_frequency(self, codon: str) -> float:
            total = sum(self._codon_counts.values())
            return round(self._codon_counts[codon.upper()] / total, 4) if total else 0.0

        def rare_codons(self, threshold: int = 1) -> list[str]:
            return [codon for codon, count in self._codon_counts.items() if count <= threshold]

    @staticmethod
    def run() -> None:
        sequence = "ATGGCCATGGCCTTTGCCATGAAATAA"
        analyzer = IndustryCounter.CodonUsageAnalyzer(sequence)

        print(f"most common codons: {analyzer.most_common_codons()}")
        print(f"frequency of ATG: {analyzer.codon_frequency('ATG')}")
        print(f"rare codons: {analyzer.rare_codons()}")

        try:
            IndustryCounter.CodonUsageAnalyzer("ATGCC")
        except ValueError as exc:
            print(f"caught expected error: {exc}")


if __name__ == "__main__":
    UniversityCounter.run()
    InterviewCounter.run()
    IndustryCounter.run()
