from __future__ import annotations

from datetime import date

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.project_repository import ProjectRepository

pytestmark = pytest.mark.integration


@pytest.mark.asyncio
async def test_create_and_fetch_project_with_compounds(session: AsyncSession) -> None:
    repo = ProjectRepository(session)
    project = await repo.create_project(
        project_code="PRJ-TEST-01", title="Test Project", started_at=date(2025, 1, 1)
    )
    await session.commit()

    fetched = await repo.get_with_compounds(project.project_id)
    assert fetched is not None
    assert fetched.project_code == "PRJ-TEST-01"
    assert fetched.compounds == []


@pytest.mark.asyncio
async def test_mark_completed_only_affects_active_projects(session: AsyncSession) -> None:
    repo = ProjectRepository(session)
    project = await repo.create_project(
        project_code="PRJ-TEST-02",
        title="Planning Stage",
        started_at=date(2025, 1, 1),
        status="planning",
    )
    await session.commit()

    rows_affected = await repo.mark_completed(project.project_id)
    assert rows_affected == 0
