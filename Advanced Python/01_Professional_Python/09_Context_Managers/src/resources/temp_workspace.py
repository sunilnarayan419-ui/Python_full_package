"""Sync and async ephemeral workspace context managers for large
intermediate scientific-computing artifacts, guaranteeing cleanup even
on failure and demonstrating nested resource composition.
"""
from __future__ import annotations

import shutil
import tempfile
from contextlib import asynccontextmanager, contextmanager
from pathlib import Path
from typing import AsyncIterator, Iterator


@contextmanager
def scratch_workspace(*, prefix: str = "pipeline-") -> Iterator[Path]:
    workspace = Path(tempfile.mkdtemp(prefix=prefix))
    try:
        yield workspace
    finally:
        shutil.rmtree(workspace, ignore_errors=True)


@asynccontextmanager
async def async_scratch_workspace(*, prefix: str = "pipeline-async-") -> AsyncIterator[Path]:
    """Async variant for use inside `async def` pipeline stages (e.g.
    coroutine-based ingestion of remote datasets into a scratch dir).
    """
    workspace = Path(tempfile.mkdtemp(prefix=prefix))
    try:
        yield workspace
    finally:
        shutil.rmtree(workspace, ignore_errors=True)
