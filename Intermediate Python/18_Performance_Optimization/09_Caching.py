from __future__ import annotations

import functools
import time
from typing import Callable, TypeVar

T = TypeVar("T")

_MONOISOTOPIC_MASSES: dict[str, float] = {
    "A": 71.03711, "R": 156.10111, "N": 114.04293, "D": 115.02694,
    "C": 103.00919, "E": 129.04259, "Q": 128.05858, "G": 57.02146,
    "H": 137.05891, "I": 113.08406, "L": 113.08406, "K": 128.09496,
    "M": 131.04049, "F": 147.06841, "P": 97.05276, "S": 87.03203,
    "T": 101.04768, "W": 186.07931, "Y": 163.06333, "V": 99.06841,
}
_WATER_MASS = 18.01056


def _expensive_peptide_mass(sequence: str) -> float:
    """Deterministic but artificially expensive monoisotopic mass calculation."""
    total_mass = _WATER_MASS
    for residue in sequence:
        if residue not in _MONOISOTOPIC_MASSES:
            raise ValueError(f"unknown residue: {residue}")
        # Simulate an expensive per-residue calculation via redundant work.
        partial = 0.0
        for _ in range(2000):
            partial += _MONOISOTOPIC_MASSES[residue] / 2000
        total_mass += partial
    return total_mass


class PeptideMassCachingWorkflow:
    """Demonstrates caching of an expensive, purely deterministic mass calculation.

    Workload: computing monoisotopic peptide mass for repeated peptide
    sequences, as occurs when scoring candidate peptides against a
    spectral library with many duplicate or overlapping sequences.
    """

    def __init__(self, peptide_sequences: list[str]) -> None:
        if not peptide_sequences:
            raise ValueError("peptide_sequences must be non-empty")
        self.peptide_sequences = peptide_sequences
        self._cached_mass = functools.cache(_expensive_peptide_mass)

    def compute_uncached(self, sequence: str) -> float:
        return _expensive_peptide_mass(sequence)

    def compute_cached(self, sequence: str) -> float:
        return self._cached_mass(sequence)

    def run_uncached_batch(self) -> list[float]:
        return [self.compute_uncached(sequence) for sequence in self.peptide_sequences]

    def run_cached_batch(self) -> list[float]:
        return [self.compute_cached(sequence) for sequence in self.peptide_sequences]

    def invalidate_cache(self) -> None:
        self._cached_mass.cache_clear()

    def benchmark(self, function: Callable[..., T], *args: object, **kwargs: object) -> tuple[T, float]:
        start = time.perf_counter()
        result = function(*args, **kwargs)
        elapsed = time.perf_counter() - start
        return result, elapsed

    @staticmethod
    def run() -> None:
        unique_peptides = ["PEPTIDEK", "MASSIVELY", "GATTACAWQ", "SEQVENCER", "KINASEACT"]
        # Simulate a realistic batch where many peptides recur (e.g. repeated spectra).
        repeated_peptides = (unique_peptides * 40)
        workflow = PeptideMassCachingWorkflow(repeated_peptides)

        uncached_result, uncached_elapsed = workflow.benchmark(workflow.run_uncached_batch)
        print(f"uncached batch: {uncached_elapsed:.6f}s")

        cached_result, cached_elapsed = workflow.benchmark(workflow.run_cached_batch)
        print(f"cached batch (cold): {cached_elapsed:.6f}s")

        cached_result_warm, cached_elapsed_warm = workflow.benchmark(workflow.run_cached_batch)
        print(f"cached batch (warm, all hits): {cached_elapsed_warm:.6f}s")

        if uncached_result != cached_result or cached_result != cached_result_warm:
            raise RuntimeError("Optimized implementation changed the numerical result.")

        speedup = cached_elapsed / cached_elapsed_warm if cached_elapsed_warm > 0 else float("inf")
        print(f"warm-cache speedup vs cold-cache: {speedup:.2f}x")

        info = workflow._cached_mass.cache_info()
        print(f"cache_info: hits={info.hits}, misses={info.misses}, currsize={info.currsize}")

        workflow.invalidate_cache()
        info_after_clear = workflow._cached_mass.cache_info()
        print(f"cache_info after clear: hits={info_after_clear.hits}, misses={info_after_clear.misses}")


if __name__ == "__main__":
    PeptideMassCachingWorkflow.run()
