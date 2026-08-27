"""Performance engineering example: profiling and optimizing k-mer counting
over DNA sequences using pure Python.

Workflow demonstrated: baseline -> measure -> identify bottleneck ->
optimize -> measure again.
"""

from __future__ import annotations

import cProfile
import pstats
import time
from collections import Counter
from io import StringIO


def generate_sequence(length: int, seed: int = 42) -> str:
    """Deterministic pseudo-random DNA sequence generator (no external RNG
    dependency, fully reproducible across runs and machines).
    """
    bases = "ACGT"
    state = seed
    chars = []
    for _ in range(length):
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        chars.append(bases[state % 4])
    return "".join(chars)


def count_kmers_naive(sequence: str, k: int) -> dict[str, int]:
    """Baseline implementation: builds substrings and a plain dict.

    Algorithmic cost: O(n*k) due to substring creation and repeated
    dict key lookups without pre-sizing.
    """
    counts: dict[str, int] = {}
    for i in range(len(sequence) - k + 1):
        kmer = sequence[i : i + k]
        if kmer in counts:
            counts[kmer] += 1
        else:
            counts[kmer] = 1
    return counts


def count_kmers_optimized(sequence: str, k: int) -> dict[str, int]:
    """Optimized implementation: delegates counting to collections.Counter,
    which uses a C-implemented fast path for bulk counting.

    This is an algorithmic/data-structure optimization (better-suited
    built-in for the counting operation), not a micro-optimization --
    it removes redundant branch checks and Python-level increment
    logic from the hot loop.
    """
    kmers = (sequence[i : i + k] for i in range(len(sequence) - k + 1))
    return dict(Counter(kmers))


def _time_call(func, *args) -> tuple[float, dict[str, int]]:
    start = time.perf_counter()
    result = func(*args)
    elapsed = time.perf_counter() - start
    return elapsed, result


def _profile_call(func, *args) -> str:
    profiler = cProfile.Profile()
    profiler.enable()
    func(*args)
    profiler.disable()

    buffer = StringIO()
    stats = pstats.Stats(profiler, stream=buffer).sort_stats("cumulative")
    stats.print_stats(5)
    return buffer.getvalue()


if __name__ == "__main__":
    sequence = generate_sequence(length=200_000, seed=7)
    k = 6

    naive_time, naive_result = _time_call(count_kmers_naive, sequence, k)
    optimized_time, optimized_result = _time_call(count_kmers_optimized, sequence, k)

    # Correctness must hold before any performance claim is meaningful.
    assert naive_result == optimized_result, "optimization changed output correctness"

    print(f"naive implementation:     {naive_time:.4f}s")
    print(f"optimized implementation: {optimized_time:.4f}s")
    print(
        "Note: relative improvement is machine-dependent; only the "
        "correctness equivalence and profiling breakdown below are relied upon."
    )

    print("\n--- cProfile breakdown: naive implementation (top 5 by cumulative time) ---")
    print(_profile_call(count_kmers_naive, sequence, k))
