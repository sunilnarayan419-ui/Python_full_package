from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from app.repositories.collaboration_repository import CollaborationRepository


@pytest.mark.asyncio
async def test_add_researcher_to_project_raises_on_missing_project() -> None:
    session = AsyncMock()
    session.get.side_effect = [None, object()]
    repo = CollaborationRepository(session)

    with pytest.raises(ValueError, match="does not exist"):
        await repo.add_researcher_to_project(project_id=1, researcher_id=2)


@pytest.mark.asyncio
async def test_add_researcher_to_project_is_idempotent() -> None:
    class FakeResearcher:
        pass

    class FakeProject:
        def __init__(self) -> None:
            self.researchers: list[FakeResearcher] = []

    researcher = FakeResearcher()
    project = FakeProject()
    project.researchers.append(researcher)

    session = AsyncMock()
    session.get.side_effect = [project, researcher]
    repo = CollaborationRepository(session)

    await repo.add_researcher_to_project(project_id=1, researcher_id=2)

    assert project.researchers.count(researcher) == 1


@pytest.mark.asyncio
async def test_delete_project_cascades_notebooks_is_noop_when_missing() -> None:
    session = AsyncMock()
    session.get.return_value = None
    repo = CollaborationRepository(session)

    await repo.delete_project_cascades_notebooks(project_id=999)

    session.delete.assert_not_awaited()
