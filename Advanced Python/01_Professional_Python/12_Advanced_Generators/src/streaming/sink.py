"""Bounded-buffer generator sink implementing simple backpressure: the
producer generator is only advanced up to `capacity` items ahead of
the consumer, preventing unbounded memory growth when a slow
downstream consumer (e.g. a network upload) lags behind a fast
upstream producer (e.g. local file parsing).
"""
from __future__ import annotations

from collections import deque
from typing import Iterable, Iterator, TypeVar

T = TypeVar("T")


class BoundedBuffer:
    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self._capacity = capacity

    def throttle(self, source: Iterable[T]) -> Iterator[T]:
        buffer: deque[T] = deque()
        iterator = iter(source)
        for _ in range(self._capacity):
            try:
                buffer.append(next(iterator))
            except StopIteration:
                break
        while buffer:
            yield buffer.popleft()
            try:
                buffer.append(next(iterator))
            except StopIteration:
                continue
