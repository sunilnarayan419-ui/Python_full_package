from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.experiment import AnalysisJob, Experiment


@dataclass(frozen=True, slots=True)
class ExperimentSummary:
    experiment_id: int
    title: str
    job_count: int


class ExperimentRepositoryBefore:
    """BEFORE: classic N+1. One query for experiments, then one additional query
    per experiment to count its jobs -- 1 + N round trips for N experiments."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_summaries(self, limit: int = 50) -> list[ExperimentSummary]:
        experiments = (
            (await self._session.execute(select(Experiment).limit(limit))).scalars().all()
        )
        summaries: list[ExperimentSummary] = []
        for experiment in experiments:
            jobs = (
                await self._session.execute(
                    select(AnalysisJob).where(AnalysisJob.experiment_id == experiment.experiment_id)
                )
            ).scalars().all()
            summaries.append(
                ExperimentSummary(
                    experiment_id=experiment.experiment_id,
                    title=experiment.title,
                    job_count=len(jobs),
                )
            )
        return summaries


class ExperimentRepositoryAfter:
    """AFTER: two round trips total regardless of N -- one for experiments, one batched
    selectinload for all jobs -- eliminating the N+1 pattern entirely."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_summaries(self, limit: int = 50) -> list[ExperimentSummary]:
        stmt = (
            select(Experiment)
            .options(selectinload(Experiment.analysis_jobs))
            .limit(limit)
        )
        experiments = (await self._session.execute(stmt)).scalars().unique().all()
        return [
            ExperimentSummary(
                experiment_id=e.experiment_id,
                title=e.title,
                job_count=len(e.analysis_jobs),
            )
            for e in experiments
        ]
