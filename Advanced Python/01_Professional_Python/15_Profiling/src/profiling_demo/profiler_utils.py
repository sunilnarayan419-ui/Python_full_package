"""Reusable profiling utilities: cProfile/pstats wrapper, timeit-based
microbenchmarking, and tracemalloc-based peak-memory measurement.
"""
from __future__ import annotations

import cProfile
import pstats
import time
import tracemalloc
from dataclasses import dataclass
from io import StringIO
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


@dataclass(frozen=True, slots=True)
class ProfileReport:
    stats_text: str
    result: object


def profile_call(func: Callable[P, R], *args: P.args, **kwargs: P.kwargs) -> ProfileReport:
    profiler = cProfile.Profile()
    profiler.enable()
    result = func(*args, **kwargs)
    profiler.disable()
    buffer = StringIO()
    stats = pstats.Stats(profiler, stream=buffer).sort_stats("cumulative")
    stats.print_stats(10)
    return ProfileReport(stats_text=buffer.getvalue(), result=result)


@dataclass(frozen=True, slots=True)
class TimingReport:
    best_seconds: float
    mean_seconds: float
    runs: int


def time_call(func: Callable[[], R], *, runs: int = 5) -> TimingReport:
    samples: list[float] = []
    for _ in range(runs):
        start = time.perf_counter()
        func()
        samples.append(time.perf_counter() - start)
    return TimingReport(best_seconds=min(samples), mean_seconds=sum(samples) / runs, runs=runs)


@dataclass(frozen=True, slots=True)
class MemoryReport:
    current_bytes: int
    peak_bytes: int
    top_lines: tuple[str, ...]


def trace_peak_memory(func: Callable[[], R], *, top_n: int = 5) -> tuple[R, MemoryReport]:
    tracemalloc.start()
    try:
        result = func()
        current, peak = tracemalloc.get_traced_memory()
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics("lineno")[:top_n]
        top_lines = tuple(str(stat) for stat in top_stats)
    finally:
        tracemalloc.stop()
    return result, MemoryReport(current_bytes=current, peak_bytes=peak, top_lines=top_lines)
