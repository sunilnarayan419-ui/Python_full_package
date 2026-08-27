"""Demonstrates a realistic reference-cycle hazard — an observer
pattern between pipeline stages — and how to break it correctly with
`weakref` instead of relying on the cyclic garbage collector to clean
up promptly.

A naive bidirectional stage<->observer link creates a reference cycle:
CPython's refcounting alone cannot free such cycles immediately; they
only get collected when the generational `gc` module's cycle detector
runs, which can delay cleanup of possibly-large per-stage buffers.
Using `weakref` on the back-reference avoids creating the cycle at all.
"""
from __future__ import annotations

import weakref
from typing import Protocol


class StageObserver(Protocol):
    def on_stage_complete(self, stage: "PipelineStage", *, records_processed: int) -> None: ...  # noqa: E704


class PipelineStage:
    """A pipeline stage holds only a *weak* reference to its observer.

    If the observer (e.g. a metrics collector owned elsewhere) goes out
    of scope, the stage does not keep it alive, and the stage itself
    does not participate in a reference cycle with the observer even if
    the observer also happens to hold a reference back to the stage.
    """

    def __init__(self, name: str, observer: StageObserver | None = None) -> None:
        self.name = name
        self._observer_ref: weakref.ReferenceType[StageObserver] | None = (
            weakref.ref(observer) if observer is not None else None
        )
        self.buffer: bytearray = bytearray()

    def attach_observer(self, observer: StageObserver) -> None:
        self._observer_ref = weakref.ref(observer)

    def run(self, records: list[bytes]) -> None:
        for record in records:
            self.buffer.extend(record)
        observer = self._observer_ref() if self._observer_ref is not None else None
        if observer is not None:
            observer.on_stage_complete(self, records_processed=len(records))
