"""
06_Packages.py

Topic: Python packages.

Demonstrates the `bioutils` package located alongside this file, showing
package namespace organization and importing functionality from package
modules.
"""

from bioutils import gc_content, reverse_complement, summarize_measurements
from bioutils.sequence_tools import gc_content as gc_content_direct


class UniversityPackages:
    """Introduces importing from a package's top-level namespace."""

    @staticmethod
    def run() -> None:
        dna_sequence = "ATGCCGTATAGC"

        content = gc_content(dna_sequence)
        complement = reverse_complement(dna_sequence)

        print("University: package imports")
        print(f"  Sequence: {dna_sequence}")
        print(f"  GC content: {content:.2f}%")
        print(f"  Reverse complement: {complement}")


class InterviewPackages:
    """Uses package functionality to solve a realistic sequence-analysis task."""

    @staticmethod
    def run() -> None:
        sequences = ["ATGCGTAC", "GGCCATTA", "TTAAGGCC"]

        gc_contents = [round(gc_content(seq), 2) for seq in sequences]
        summary = summarize_measurements(gc_contents)

        print("Interview: package imports")
        print(f"  Sequences: {sequences}")
        print(f"  GC contents: {gc_contents}")
        print(f"  Summary across sequences: {summary}")


class IndustryPackages:
    """Demonstrates how a small bioinformatics package supports maintainable code."""

    def __init__(self, sequences: list[str]) -> None:
        if not sequences:
            raise ValueError("sequences must contain at least one entry.")
        self._sequences = sequences

    def analyze(self) -> dict[str, float]:
        gc_values = [gc_content(seq) for seq in self._sequences]
        return summarize_measurements(gc_values)

    def complements(self) -> list[str]:
        return [reverse_complement(seq) for seq in self._sequences]

    def report(self) -> str:
        summary = self.analyze()
        return (
            f"n={len(self._sequences)} | "
            f"mean_gc={summary['mean']:.2f}% | "
            f"stdev_gc={summary['stdev']:.3f}"
        )

    @staticmethod
    def run() -> None:
        sequences = ["ATGCGTACGT", "CGGATCCGTA", "TATAGCGCTA", "GGCATGCTAA"]

        analyzer = IndustryPackages(sequences)
        print("Industry: package imports")
        print(f"  {analyzer.report()}")
        print(f"  Complements: {analyzer.complements()}")
        print(f"  Direct submodule import check: {gc_content_direct(sequences[0]):.2f}%")


if __name__ == "__main__":
    UniversityPackages.run()
    InterviewPackages.run()
    IndustryPackages.run()
