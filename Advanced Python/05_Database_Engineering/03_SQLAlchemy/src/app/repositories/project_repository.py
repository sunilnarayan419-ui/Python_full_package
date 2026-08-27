from __future__ import annotations

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.models.research import Compound, ResearchProject, ScreeningResult


class ProjectRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_with_compounds(self, project_id: int) -> ResearchProject | None:
        stmt = (
            select(ResearchProject)
            .where(ResearchProject.project_id == project_id)
            .options(selectinload(ResearchProject.compounds))
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_compound_with_hits(self, compound_id: int) -> Compound | None:
        """joinedload for a single-row, tightly-bound relationship fetch."""
        stmt = (
            select(Compound)
            .where(Compound.compound_id == compound_id)
            .options(joinedload(Compound.project))
        )
        result = await self._session.execute(stmt)
        return result.unique().scalar_one_or_none()

    async def list_active_projects(self, limit: int = 50) -> list[ResearchProject]:
        stmt = (
            select(ResearchProject)
            .where(ResearchProject.status == "active")
            .order_by(ResearchProject.project_code)
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def create_project(
        self, *, project_code: str, title: str, started_at, status: str = "planning"
    ) -> ResearchProject:
        project = ResearchProject(
            project_code=project_code, title=title, status=status, started_at=started_at
        )
        self._session.add(project)
        await self._session.flush()
        return project

    async def mark_completed(self, project_id: int) -> int:
        stmt = (
            update(ResearchProject)
            .where(ResearchProject.project_id == project_id, ResearchProject.status == "active")
            .values(status="completed")
        )
        result = await self._session.execute(stmt)
        return result.rowcount

    async def delete_project(self, project_id: int) -> int:
        stmt = delete(ResearchProject).where(ResearchProject.project_id == project_id)
        result = await self._session.execute(stmt)
        return result.rowcount

    async def hit_count_for_compound(self, compound_id: int) -> int:
        """Explicit query instead of lazy-loading screening_results (relationship is lazy='raise')."""
        stmt = select(ScreeningResult).where(
            ScreeningResult.compound_id == compound_id, ScreeningResult.is_hit.is_(True)
        )
        result = await self._session.execute(stmt)
        return len(result.scalars().all())
