"""Practical use of small-integer and string interning behavior:
building stable, memory-cheap batch keys for grouping large numbers of
short-lived pipeline-stage records.

Relies on documented CPython behavior (small ints -5..256 and most
identifier-like strings are interned) purely as a memory/perf
observation, never as a correctness guarantee — equality (`==`), not
identity (`is`), is always used for the actual grouping logic.
"""
from __future__ import annotations

import sys
from typing import Hashable


def identity_batch_key(stage_name: str, shard_index: int) -> tuple[str, int]:
    """Interning `stage_name` explicitly via `sys.intern` ensures
    repeated identical stage-name strings across millions of records
    share one underlying string object, reducing memory overhead in
    large batch-key dictionaries — while grouping logic downstream
    still relies on tuple equality, not `is`, for correctness.
    """
    return (sys.intern(stage_name), shard_index)


def group_by_batch_key(records: list[tuple[str, int, float]]) -> dict[Hashable, list[float]]:
    grouped: dict[Hashable, list[float]] = {}
    for stage_name, shard_index, value in records:
        key = identity_batch_key(stage_name, shard_index)
        grouped.setdefault(key, []).append(value)
    return grouped
