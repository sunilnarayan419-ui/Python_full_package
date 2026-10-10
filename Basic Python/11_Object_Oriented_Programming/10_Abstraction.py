"""
TOPIC: Abstraction

MAIN POINTS
- Abstraction exposes essential behavior while hiding implementation details.
- The abc module provides tools for defining abstract base classes.
- An abstract class can define a common interface for subclasses.
- The @abstractmethod decorator marks methods that concrete subclasses must implement.
- A class with unimplemented abstract methods cannot be instantiated.
- Abstraction allows different biological analysis methods to follow the same interface.
- It is useful when designing extensible scientific analysis systems.
"""

from abc import ABC, abstractmethod


class BiologicalAnalysis(ABC):
    """Abstract interface for biological analysis methods."""

    def __init__(self, sample_id, organism):
        self.sample_id = sample_id
        self.organism = organism

    @abstractmethod
    def analyze(self):
        """Perform the analysis and return a result."""
        pass

    @abstractmethod
    def generate_report(self):
        """Return a human-readable analysis report."""
        pass

    def identify_sample(self):
        return f"{self.sample_id} ({self.organism})"


class DNA_Analysis(BiologicalAnalysis):
    """Implement DNA sequence analysis."""

    def __init__(self, sample_id, organism, sequence):
        super().__init__(sample_id, organism)
        self.sequence = sequence.upper()

    def analyze(self):
        valid_bases = {"A", "T", "G", "C"}

        if not self.sequence:
            raise ValueError("DNA sequence cannot be empty.")

        if set(self.sequence) - valid_bases:
            raise ValueError("DNA sequence contains invalid characters.")

        gc_count = self.sequence.count("G") + self.sequence.count("C")
        gc_percentage = gc_count / len(self.sequence) * 100

        return {
            "sequence_length": len(self.sequence),
            "gc_percentage": gc_percentage
        }

    def generate_report(self):
        result = self.analyze()

        return (
            f"DNA Analysis Report\n"
            f"Sample: {self.identify_sample()}\n"
            f"Sequence length: {result['sequence_length']}\n"
            f"GC percentage: {result['gc_percentage']:.2f}%"
        )


class Protein_Analysis(BiologicalAnalysis):
    """Implement basic protein sequence analysis."""

    def __init__(self, sample_id, organism, sequence):
        super().__init__(sample_id, organism)
        self.sequence = sequence.upper()

    def analyze(self):
        amino_acids = set("ACDEFGHIKLMNPQRSTVWY")

        if not self.sequence:
            raise ValueError("Protein sequence cannot be empty.")

        if set(self.sequence) - amino_acids:
            raise ValueError("Protein sequence contains invalid characters.")

        return {
            "sequence_length": len(self.sequence),
            "methionine_count": self.sequence.count("M")
        }

    def generate_report(self):
        result = self.analyze()

        return (
            f"Protein Analysis Report\n"
            f"Sample: {self.identify_sample()}\n"
            f"Sequence length: {result['sequence_length']}\n"
            f"Methionine count: {result['methionine_count']}"
        )


dna_analysis = DNA_Analysis(
    "DNA_001",
    "Homo sapiens",
    "ATGCGCGT"
)

protein_analysis = Protein_Analysis(
    "PROT_001",
    "Homo sapiens",
    "MKWVTF"
)

analyses = [dna_analysis, protein_analysis]

# Every implementation follows the same abstract interface.
for analysis in analyses:
    print(analysis.generate_report())
    print()

# This would raise TypeError because abstract methods are unimplemented.
# generic_analysis = BiologicalAnalysis("SAMPLE_001", "Homo sapiens")