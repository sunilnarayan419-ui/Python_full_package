from __future__ import annotations

from uuid import UUID

from ..domain.entities import AssayType, ScreeningRun, ScreeningRunStatus
from ..repositories.screening_run_repository import ScreeningRunRepository


class ScreeningService:
    def __init__(self, repository: ScreeningRunRepository) -> None:
        self._repository = repository

    async def submit_run(self, compound_id: UUID, assay_type: AssayType) -> ScreeningRun:
        run = ScreeningRun.create(compound_id=compound_id, assay_type=assay_type)
        await self._repository.add(run)
        return run

    async def get_run(self, run_id: UUID) -> ScreeningRun:
        return await self._repository.get(run_id)

    async def list_runs(self, compound_id: UUID, *, limit: int, offset: int) -> list[ScreeningRun]:
        return await self._repository.list_by_compound(compound_id, limit=limit, offset=offset)

    async def advance_run(self, run_id: UUID, target: ScreeningRunStatus, *, score: float | None = None) -> ScreeningRun:
        run = await self._repository.get(run_id)
        run.transition_to(target, score=score)
        await self._repository.save(run)
        return run
