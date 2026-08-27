from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.collaboration import LabNotebook, NotebookEntry, ResearchProject, Researcher


class CollaborationRepository:
    """Demonstrates deliberate prevention of common ORM pitfalls."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_projects_with_researchers(self) -> list[ResearchProject]:
        # selectinload avoids N+1: one extra query for all researcher associations,
        # instead of one query per project.
        stmt = select(ResearchProject).options(
            selectinload(ResearchProject.researchers), selectinload(ResearchProject.notebooks)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().unique().all())

    async def add_researcher_to_project(
        self, *, project_id: int, researcher_id: int, role: str = "contributor"
    ) -> None:
        project = await self._session.get(
            ResearchProject, project_id, options=[selectinload(ResearchProject.researchers)]
        )
        researcher = await self._session.get(Researcher, researcher_id)
        if project is None or researcher is None:
            raise ValueError("project or researcher does not exist")
        if researcher not in project.researchers:
            project.researchers.append(researcher)
        await self._session.flush()

    async def paginated_notebook_entries(
        self, notebook_id: int, *, page: int, page_size: int = 50
    ) -> list[NotebookEntry]:
        """Explicit, bounded fetch — entries relationship is lazy='raise' precisely to
        force every read path through a paginated query like this one."""
        stmt = (
            select(NotebookEntry)
            .where(NotebookEntry.notebook_id == notebook_id)
            .order_by(NotebookEntry.entry_id)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def delete_project_cascades_notebooks(self, project_id: int) -> None:
        """Deleting the aggregate root removes owned notebooks via ORM cascade,
        while the many-to-many researcher associations are simply unlinked, not deleted."""
        project = await self._session.get(
            ResearchProject, project_id, options=[selectinload(ResearchProject.notebooks)]
        )
        if project is None:
            return
        await self._session.delete(project)
        await self._session.flush()

    async def get_notebook(self, notebook_id: int) -> LabNotebook | None:
        return await self._session.get(LabNotebook, notebook_id)
