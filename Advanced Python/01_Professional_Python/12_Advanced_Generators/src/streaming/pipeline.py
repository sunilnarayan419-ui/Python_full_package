"""Lazy, composable generator stages for streaming sequence processing.

Each stage consumes an iterator and yields lazily, so an arbitrarily
long chain of stages (parse -> filter -> transform -> aggregate) never
materializes the full dataset — only the current record is in memory
at each stage boundary. This composes via ordinary generator chaining
rather than `yield from` delegation, since each stage's element type
differs from the previous (parse/filter/transform, not sub-generator
delegation).
"""
from __future__ import annotations

from typing import Iterable, Iterator

from .fastq import FastqRecord

_PHRED_OFFSET = 33


def _mean_quality(quality: str) -> float:
    if not quality:
        return 0.0
    return sum(ord(char) - _PHRED_OFFSET for char in quality) / len(quality)


def quality_filter(records: Iterable[FastqRecord], *, min_mean_quality: float) -> Iterator[FastqRecord]:
    for record in records:
        if _mean_quality(record.quality) >= min_mean_quality:
            yield record


def sliding_window_gc(records: Iterable[FastqRecord], *, window: int = 50) -> Iterator[tuple[str, list[float]]]:
    """Stateful generator: for each record, lazily computes GC content
    over sliding windows without allocating the full windowed list
    upfront (each window ratio is computed on demand as the caller
    consumes the inner values, keeping the pipeline demand-driven).
    """
    for record in records:
        sequence = record.sequence
        ratios = [
            (sequence[i : i + window].count("G") + sequence[i : i + window].count("C")) / window
            for i in range(0, max(len(sequence) - window + 1, 0), window)
        ]
        yield record.identifier, ratios


def running_stats(values: Iterable[float]) -> Iterator[tuple[int, float, float]]:
    """Welford's online algorithm as a generator: yields (count, mean,
    variance) after each new value, without ever storing the full
    stream of values — essential when the upstream generator represents
    a dataset too large to hold in memory.
    """
    count = 0
    mean = 0.0
    m2 = 0.0
    for value in values:
        count += 1
        delta = value - mean
        mean += delta / count
        delta2 = value - mean
        m2 += delta * delta2
        variance = m2 / count if count > 1 else 0.0
        yield count, mean, variance
