from __future__ import annotations

from collections.abc import AsyncIterator
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from src.api.main import app, get_repository
from src.domain.entities import AssayType, ScreeningRun
from src.repositories.screening_run_repository import InMemoryScreeningRunRepository


@pytest.fixture
def repository() -> InMemoryScreeningRunRepository:
    return InMemoryScreeningRunRepository()


@pytest.fixture(autouse=True)
def override_dependencies(repository: InMemoryScreeningRunRepository):
    app.dependency_overrides[get_repository] = lambda: repository
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client() -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as async_client:
        yield async_client


@pytest_asyncio.fixture
async def seeded_run(repository: InMemoryScreeningRunRepository) -> ScreeningRun:
    run = ScreeningRun.create(compound_id=uuid4(), assay_type=AssayType.BINDING)
    await repository.add(run)
    return run
