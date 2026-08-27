from __future__ import annotations

import cProfile
import io
import pstats
import random
import time
from dataclasses import dataclass, field
from typing import Callable, TypeVar

T = TypeVar("T")

_NUCLEOTIDES = ("A", "C", "G", "T")


@dataclass
class BenchmarkResult:
    """Structured record of a single benchmark measurement."""

    label: str
    elapsed_seconds: float
    extra: dict[str, float] = field(default_factory=dict)

    def __str__(self) -> str:
        detail = ", ".join(f"{key}={value:.6f}" for key, value in self.extra.items())
        return f"{self.label}: {self.elapsed_seconds:.6f}s ({detail})" if detail else f"{self.label}: {self.elapsed_seconds:.6f}s"


class GenomicProfilingWorkflow:
    """Profiles a realistic sequence-analysis pipeline to locate bottlenecks.

    Workflow: MEASURE -> IDENTIFY BOTTLENECK -> OPTIMIZE -> MEASURE AGAIN.
    The pipeline computes GC content, k-mer frequency tables, and a sliding
    window entropy score across a synthetic but deterministic genome sample.
    """

    def __init__(self, sequence_length: int, kmer_size: int, seed: int = 42) -> None:
        if sequence_length <= 0:
            raise ValueError("sequence_length must be positive")
        if kmer_size <= 0 or kmer_size > sequence_length:
            raise ValueError("kmer_size must be positive and <= sequence_length")
        self.sequence_length = sequence_length
        self.kmer_size = kmer_size
        self.sequence = self._generate_sequence(sequence_length, seed)

    @staticmethod
    def _generate_sequence(length: int, seed: int) -> str:
        rng = random.Random(seed)
        return "".join(rng.choice(_NUCLEOTIDES) for _ in range(length))

    def compute_gc_content(self) -> float:
        gc_count = 0
        for base in self.sequence:
            if base == "G" or base == "C":
                gc_count += 1
        return gc_count / len(self.sequence)

    def count_kmers(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        seq = self.sequence
        k = self.kmer_size
        for index in range(len(seq) - k + 1):
            kmer = seq[index:index + k]
            counts[kmer] = counts.get(kmer, 0) + 1
        return counts

    def sliding_window_entropy(self, window: int = 50) -> list[float]:
        import math

        scores: list[float] = []
        seq = self.sequence
        for start in range(0, len(seq) - window + 1, window):
            chunk = seq[start:start + window]
            freqs: dict[str, int] = {}
            for base in chunk:
                freqs[base] = freqs.get(base, 0) + 1
            entropy = 0.0
            for count in freqs.values():
                probability = count / len(chunk)
                entropy -= probability * math.log2(probability)
            scores.append(entropy)
        return scores

    def run_pipeline(self) -> dict[str, object]:
        gc_content = self.compute_gc_content()
        kmer_counts = self.count_kmers()
        entropy_scores = self.sliding_window_entropy()
        return {
            "gc_content": gc_content,
            "unique_kmers": len(kmer_counts),
            "mean_entropy": sum(entropy_scores) / len(entropy_scores) if entropy_scores else 0.0,
        }

    def benchmark(self, function: Callable[..., T], *args: object, **kwargs: object) -> tuple[T, float]:
        start = time.perf_counter()
        result = function(*args, **kwargs)
        elapsed = time.perf_counter() - start
        return result, elapsed

    def profile_pipeline(self, top_n: int = 8) -> str:
        profiler = cProfile.Profile()
        profiler.enable()
        self.run_pipeline()
        profiler.disable()

        stream = io.StringIO()
        stats = pstats.Stats(profiler, stream=stream).strip_dirs()
        stats.sort_stats(pstats.SortKey.CUMULATIVE)
        stats.print_stats(top_n)
        return stream.getvalue()

    @staticmethod
    def run() -> None:
        workflow = GenomicProfilingWorkflow(sequence_length=60_000, kmer_size=6, seed=7)

        _, elapsed = workflow.benchmark(workflow.run_pipeline)
        baseline_result = BenchmarkResult("full_pipeline", elapsed)
        print(baseline_result)

        report = workflow.profile_pipeline(top_n=8)
        print("Top cumulative-time functions (bottleneck identification):")
        print(report)


if __name__ == "__main__":
    GenomicProfilingWorkflow.run()
