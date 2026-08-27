from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from app.repositories.dataset_repository import ConcurrentModificationError
from app.schemas.dataset_schemas import DatasetCreateRequest, DatasetUpdateRequest
from app.services.dataset_service import DatasetNotFoundError, DatasetService


@pytest.mark.asyncio
async def test_get_dataset_raises_not_found() -> None:
    session = AsyncMock()
    with patch("app.services.dataset_service.DatasetRepository") as MockRepo:
        MockRepo.return_value.get = AsyncMock(return_value=None)
        service = DatasetService(session)
        with pytest.raises(DatasetNotFoundError):
            await service.get_dataset(999)


@pytest.mark.asyncio
async def test_update_dataset_propagates_concurrency_conflict_and_rolls_back() -> None:
    session = AsyncMock()
    with patch("app.services.dataset_service.DatasetRepository") as MockRepo:
        MockRepo.return_value.update_with_optimistic_lock = AsyncMock(
            side_effect=ConcurrentModificationError("stale version")
        )
        service = DatasetService(session)
        with pytest.raises(ConcurrentModificationError):
            await service.update_dataset(
                1, DatasetUpdateRequest(name="new name", expected_version=1)
            )
    session.rollback.assert_awaited_once()
    session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_list_datasets_caps_page_size_at_100() -> None:
    session = AsyncMock()
    with patch("app.services.dataset_service.DatasetRepository") as MockRepo:
        MockRepo.return_value.list_page = AsyncMock(return_value=([], 0))
        service = DatasetService(session)
        page = await service.list_datasets(page=1, page_size=500)

    assert page.page_size == 100
    called_kwargs = MockRepo.return_value.list_page.call_args.kwargs
    assert called_kwargs["page_size"] == 100


@pytest.mark.asyncio
async def test_delete_dataset_raises_not_found_when_repo_reports_missing() -> None:
    session = AsyncMock()
    with patch("app.services.dataset_service.DatasetRepository") as MockRepo:
        MockRepo.return_value.soft_delete = AsyncMock(return_value=False)
        service = DatasetService(session)
        with pytest.raises(DatasetNotFoundError):
            await service.delete_dataset(42)
