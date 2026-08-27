from __future__ import annotations

import sys

import pytest

from memeff import GenomicInterval, IntervalStore, ReadAlignmentCache


def test_slots_prevents_arbitrary_attribute_assignment() -> None:
    interval = GenomicInterval("chr1", 100, 200)
    with pytest.raises(AttributeError):
        interval.unexpected_attribute = "value"  # type: ignore[attr-defined]


def test_slotted_instance_has_no_dict() -> None:
    interval = GenomicInterval("chr1", 100, 200)
    assert not hasattr(interval, "__dict__")


def test_interval_store_query_overlaps_finds_matches() -> None:
    store = IntervalStore()
    store.add(GenomicInterval("chr1", 100, 200))
    store.add(GenomicInterval("chr1", 500, 600))
    store.add(GenomicInterval("chr2", 100, 200))
    store.finalize()
    results = list(store.query_overlaps(GenomicInterval("chr1", 150, 250)))
    assert len(results) == 1
    assert results[0].start == 100


def test_interval_store_early_termination_on_sorted_data() -> None:
    store = IntervalStore()
    for start in range(0, 1000, 100):
        store.add(GenomicInterval("chr1", start, start + 50))
    store.finalize()
    results = list(store.query_overlaps(GenomicInterval("chr1", 0, 60)))
    assert {r.start for r in results} == {0}


def test_read_alignment_cache_evicts_least_recently_used() -> None:
    cache: ReadAlignmentCache[str, int] = ReadAlignmentCache(max_entries=2)
    cache.compute("A", object(), lambda _: 1)
    cache.compute("B", object(), lambda _: 2)
    cache.compute("C", object(), lambda _: 3)
    assert "A" not in cache
    assert "B" in cache and "C" in cache


def test_read_alignment_cache_reuses_cached_value_without_recompute() -> None:
    calls = 0

    def summarize(_source: object) -> int:
        nonlocal calls
        calls += 1
        return 42

    cache: ReadAlignmentCache[str, int] = ReadAlignmentCache(max_entries=10)
    cache.compute("A", object(), summarize)
    cache.compute("A", object(), summarize)
    assert calls == 1
