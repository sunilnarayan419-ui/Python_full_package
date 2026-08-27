"""Detects leaked (never-closed) file-like resources using
`weakref.finalize`, and demonstrates a legitimate, narrow use of
explicit `gc.collect()` — verifying in a test/diagnostic context that
a resource was reclaimed promptly rather than lingering in a reference
cycle.
"""
from __future__ import annotations

import gc
import io
import weakref
from typing import Callable


class TrackedFileHandle:
    """Wraps a file-like object; registers a finalizer that fires a
    leak-detection callback if the handle is garbage-collected while
    still open (i.e. the caller forgot to call `close()`/use it as a
    context manager).
    """

    def __init__(self, handle: io.IOBase, on_leak: Callable[[str], None]) -> None:
        self._handle = handle
        self._closed = False
        self._label = repr(handle)
        self._finalizer = weakref.finalize(self, self._check_leak, on_leak, self._label)

    def close(self) -> None:
        self._closed = True
        self._handle.close()
        self._finalizer.detach()

    @staticmethod
    def _check_leak(on_leak: Callable[[str], None], label: str) -> None:
        on_leak(f"resource leaked without explicit close(): {label}")

    def __enter__(self) -> "TrackedFileHandle":
        return self

    def __exit__(self, *exc_info: object) -> None:
        if not self._closed:
            self.close()


class ResourceLeakDetector:
    """Test/diagnostic helper: forces a full generational collection and
    reports whether tracked objects were actually reclaimed. This
    explicit `gc.collect()` call is legitimate here — it is scoped to
    diagnostics/tests, not routine production request handling, where
    calling it would only mask an underlying cycle rather than fix it.
    """

    @staticmethod
    def force_collect_and_count_unreachable() -> int:
        gc.collect()
        return len(gc.garbage)

    @staticmethod
    def object_is_alive(ref: "weakref.ReferenceType[object]") -> bool:
        gc.collect()
        return ref() is not None
