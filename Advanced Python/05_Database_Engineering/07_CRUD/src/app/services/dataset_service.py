from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.dataset_repository import ConcurrentModificationError, DatasetRepository
from app.schemas.dataset_schemas import DatasetCreateRequest, DatasetUpdateRequest, Page


class DatasetNotFoundError(Exception):
    pass


class DatasetService:
    """Owns transaction boundaries and translates repository errors into service-level ones."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._repo = DatasetRepository(session)

    async def create_dataset(self, payload: DatasetCreateRequest):
        async with self._session.begin_nested():
            dataset = await self._repo.create(name=payload.name, description=payload.description)
        await self._session.commit()
        return dataset

    async def get_dataset(self, dataset_id: int):
        dataset = await self._repo.get(dataset_id)
        if dataset is None:
            raise DatasetNotFoundError(dataset_id)
        return dataset

    async def list_datasets(
        self, *, page: int = 1, page_size: int = 25, name_filter: str | None = None, sort_desc: bool = True
    ) -> Page:
        page_size = min(page_size, 100)
        items, total = await self._repo.list_page(
            page=page, page_size=page_size, name_filter=name_filter, sort_desc=sort_desc
        )
        return Page(items=items, total=total, page=page, page_size=page_size)  # type: ignore[arg-type]

    async def update_dataset(self, dataset_id: int, payload: DatasetUpdateRequest):
        try:
            dataset = await self._repo.update_with_optimistic_lock(
                dataset_id=dataset_id,
                expected_version=payload.expected_version,
                name=payload.name,
                description=payload.description,
            )
        except LookupError as exc:
            raise DatasetNotFoundError(dataset_id) from exc
        except ConcurrentModificationError:
            await self._session.rollback()
            raise
        await self._session.commit()
        return dataset

    async def delete_dataset(self, dataset_id: int) -> None:
        deleted = await self._repo.soft_delete(dataset_id)
        if not deleted:
            raise DatasetNotFoundError(dataset_id)
        await self._session.commit()
