"""Bounded, weak-reference-aware cache for expensive-to-recompute read
alignment summaries, avoiding both unbounded memory growth and
accidental lifetime-extension of large underlying alignment objects.
"""
from __future__ import annotations

import weakref
from collections import OrderedDict
from typing import Callable, Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class ReadAlignmentCache(Generic[K, V]):
    """LRU cache bounded by `max_entries`. Values are held strongly
    (they are cheap summary objects), but the cache additionally tracks
    a weak-reference registry of any large source objects passed to
    `compute`, so evicting a cache entry doesn't hold a large alignment
    buffer alive beyond the caller's own reference to it.
    """

    def __init__(self, max_entries: int = 10_000) -> None:
        if max_entries < 1:
            raise ValueError("max_entries must be at least 1")
        self._max_entries = max_entries
        self._cache: OrderedDict[K, V] = OrderedDict()
        self._source_refs: "weakref.WeakValueDictionary[K, object]" = weakref.WeakValueDictionary()

    def compute(self, key: K, source: object, summarize: Callable[[object], V]) -> V:
        if key in self._cache:
            self._cache.move_to_end(key)
            return self._cache[key]

        value = summarize(source)
        self._cache[key] = value
        try:
            self._source_refs[key] = source
        except TypeError:
            pass  # source does not support weak references; skip tracking
        if len(self._cache) > self._max_entries:
            self._cache.popitem(last=False)
        return value

    def __len__(self) -> int:
        return len(self._cache)

    def __contains__(self, key: object) -> bool:
        return key in self._cache
