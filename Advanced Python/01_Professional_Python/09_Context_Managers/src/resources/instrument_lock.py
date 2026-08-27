"""File-lock-based context manager for exclusive access to a shared
lab instrument, using `contextlib.contextmanager` with guaranteed
exception-safe release via `try/finally`.
"""
from __future__ import annotations

import errno
import os
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


class InstrumentBusyError(Exception):
    pass


class InstrumentLock:
    def __init__(self, lock_dir: Path, instrument_id: str, *, timeout_seconds: float = 5.0) -> None:
        self._lock_path = lock_dir / f"{instrument_id}.lock"
        self._timeout_seconds = timeout_seconds

    @contextmanager
    def acquire(self) -> Iterator[None]:
        deadline = time.monotonic() + self._timeout_seconds
        fd: int | None = None
        while fd is None:
            try:
                fd = os.open(self._lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            except FileExistsError:
                if time.monotonic() >= deadline:
                    raise InstrumentBusyError(
                        f"could not acquire lock {self._lock_path} within "
                        f"{self._timeout_seconds}s"
                    ) from None
                time.sleep(0.05)
        try:
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            yield
        finally:
            try:
                self._lock_path.unlink()
            except OSError as exc:
                if exc.errno != errno.ENOENT:
                    raise
