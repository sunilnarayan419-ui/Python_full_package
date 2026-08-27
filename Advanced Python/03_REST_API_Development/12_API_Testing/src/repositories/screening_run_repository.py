from __future__ import annotations

from typing import Protocol
from uuid import UUID

from ..domain.entities import ScreeningRun, ScreeningRunNotFoundError


class ScreeningRunRepository(Protocol):
    async def add(self, run: ScreeningRun) -> None: ...

    async def get(self, run_id: UUID) -> ScreeningRun: ...

    async def list_by_compound(self, compound_id: UUID, *, limit: int, offset: int) -> list[ScreeningRun]: ...

    async def save(self, run: ScreeningRun) -> None: ...


class InMemoryScreeningRunRepository:
    def __init__(self) -> None:
        self._runs: dict[UUID, ScreeningRun] = {}

    async def add(self, run: ScreeningRun) -> None:
        self._runs[run.run_id] = run

    async def get(self, run_id: UUID) -> ScreeningRun:
        run = self._runs.get(run_id)
        if run is None:
            raise ScreeningRunNotFoundError(run_id)
        return run

    async def list_by_compound(self, compound_id: UUID, *, limit: int, offset: int) -> list[ScreeningRun]:
        matching = [run for run in self._runs.values() if run.compound_id == compound_id]
        matching.sort(key=lambda run: run.created_at)
        return matching[offset : offset + limit]

    async def save(self, run: ScreeningRun) -> None:
        self._runs[run.run_id] = run
