"""Demonstrates Python-native breakpoint-driven debugging practices.

IMPORTANT: normal execution of this file (python 06_Breakpoints.py) does
NOT enter an interactive debugger. The breakpoint() call is isolated
inside `debug_session()`, which is only invoked when explicitly
requested via the DEBUG_SESSION environment variable, so automated
runs and CI never hang waiting for input.
"""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SequencingRead:
    read_id: str
    quality_scores: list[int]


def mean_quality(read: SequencingRead) -> float:
    if not read.quality_scores:
        raise ValueError(f"read {read.read_id} has no quality scores")
    return sum(read.quality_scores) / len(read.quality_scores)


def filter_low_quality_reads(
    reads: list[SequencingRead], min_mean_quality: float
) -> list[SequencingRead]:
    """Filters reads below a mean Phred quality threshold.

    A developer investigating why certain reads unexpectedly pass or
    fail this filter would, during local development, place a
    breakpoint() call right before the comparison below to inspect
    `score` and `read.read_id` interactively:

        score = mean_quality(read)
        # breakpoint()  <- inspect `score`, `read.quality_scores` here
        if score >= min_mean_quality:
            ...
    """
    passing_reads = []
    for read in reads:
        score = mean_quality(read)
        if score >= min_mean_quality:
            passing_reads.append(read)
    return passing_reads


def debug_session() -> None:
    """Isolated, opt-in demonstration of breakpoint()-driven inspection.

    Only entered when DEBUG_SESSION=1 is set in the environment, so
    normal test runs and CI pipelines never block on interactive input.
    Within a real pdb session a developer would use commands such as:

        n (next), s (step), c (continue), p <expr> (print), l (list)
    """
    reads = [
        SequencingRead(read_id="R1", quality_scores=[30, 32, 28]),
        SequencingRead(read_id="R2", quality_scores=[12, 15, 10]),
    ]

    for read in reads:
        score = mean_quality(read)
        if read.read_id == "R2":
            # Conditional breakpoint pattern: only stop for the case
            # under investigation, rather than every loop iteration.
            breakpoint()  # noqa: T100 -- intentional, gated by DEBUG_SESSION
        print(f"{read.read_id}: mean_quality={score:.2f}")


if __name__ == "__main__":
    reads = [
        SequencingRead(read_id="R1", quality_scores=[30, 32, 28]),
        SequencingRead(read_id="R2", quality_scores=[12, 15, 10]),
        SequencingRead(read_id="R3", quality_scores=[25, 26, 24]),
    ]

    passing = filter_low_quality_reads(reads, min_mean_quality=20.0)
    print(f"Reads passing quality filter: {[r.read_id for r in passing]}")

    if os.environ.get("DEBUG_SESSION") == "1":
        debug_session()
