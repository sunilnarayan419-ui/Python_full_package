from __future__ import annotations

from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.sample import AnalysisJob, Sample
from app.schemas.sample_schemas import AnalysisJobCreateRequest, SampleCreateRequest


class SampleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_sample(self, payload: SampleCreateRequest) -> Sample:
        sample = Sample(subject_code=payload.subject_code, collected_at=payload.collected_at)
        self._session.add(sample)
        await self._session.flush()
        return sample

    async def get_sample(self, sample_id: UUID) -> Sample | None:
        stmt = select(Sample).where(Sample.sample_id == sample_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def enqueue_analysis_job(self, payload: AnalysisJobCreateRequest) -> AnalysisJob:
        job = AnalysisJob(sample_id=payload.sample_id, pipeline_name=payload.pipeline_name)
        self._session.add(job)
        await self._session.flush()
        return job

    async def list_queued_jobs(self, limit: int = 100) -> list[AnalysisJob]:
        stmt = select(AnalysisJob).where(AnalysisJob.status == "queued").limit(limit)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
