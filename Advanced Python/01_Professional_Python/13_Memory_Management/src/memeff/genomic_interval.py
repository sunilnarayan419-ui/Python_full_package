"""Memory-efficient representation of large collections of genomic
intervals (e.g. millions of read alignments or peak calls).

`__slots__` removes the per-instance `__dict__`, which matters a great
deal at this scale: for ~10M interval objects, a `__dict__`-backed
class can cost several hundred additional bytes per instance versus a
slotted one, translating to gigabytes of avoidable overhead.
"""
from __future__ import annotations

from typing import Iterator


class GenomicInterval:
    __slots__ = ("chromosome", "start", "end", "score")

    def __init__(self, chromosome: str, start: int, end: int, score: float = 0.0) -> None:
        if start >= end:
            raise ValueError(f"start ({start}) must be < end ({end})")
        self.chromosome = chromosome
        self.start = start
        self.end = end
        self.score = score

    def overlaps(self, other: "GenomicInterval") -> bool:
        return (
            self.chromosome == other.chromosome
            and self.start < other.end
            and other.start < self.end
        )

    def __repr__(self) -> str:
        return f"GenomicInterval({self.chromosome!r}, {self.start}, {self.end}, score={self.score})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GenomicInterval):
            return NotImplemented
        return (
            self.chromosome == other.chromosome
            and self.start == other.start
            and self.end == other.end
            and self.score == other.score
        )


class IntervalStore:
    """Stores intervals sorted by start position per chromosome and
    exposes an iterator-based overlap query so callers never need to
    materialize a full result list unless they choose to.
    """

    def __init__(self) -> None:
        self._by_chromosome: dict[str, list[GenomicInterval]] = {}

    def add(self, interval: GenomicInterval) -> None:
        bucket = self._by_chromosome.setdefault(interval.chromosome, [])
        bucket.append(interval)

    def finalize(self) -> None:
        """Sort each chromosome's intervals once, after bulk loading,
        rather than keeping them sorted on every insert (avoids O(n)
        insertion cost repeated n times during bulk ingestion).
        """
        for bucket in self._by_chromosome.values():
            bucket.sort(key=lambda interval: interval.start)

    def query_overlaps(self, query: GenomicInterval) -> Iterator[GenomicInterval]:
        for interval in self._by_chromosome.get(query.chromosome, ()):
            if interval.start >= query.end:
                break
            if interval.overlaps(query):
                yield interval

    def __len__(self) -> int:
        return sum(len(bucket) for bucket in self._by_chromosome.values())
