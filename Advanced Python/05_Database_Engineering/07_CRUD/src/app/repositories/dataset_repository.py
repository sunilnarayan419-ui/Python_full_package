from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import StaleDataError

from app.models.dataset import Dataset


class ConcurrentModificationError(Exception):
    pass


class DatasetRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, *, name: str, description: str) -> Dataset:
        dataset = Dataset(name=name, description=description)
        self._session.add(dataset)
        await self._session.flush()
        return dataset

    async def get(self, dataset_id: int) -> Dataset | None:
        stmt = select(Dataset).where(
            Dataset.dataset_id == dataset_id, Dataset.is_deleted.is_(False)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_page(
        self, *, page: int, page_size: int, name_filter: str | None, sort_desc: bool
    ) -> tuple[list[Dataset], int]:
        base_stmt = select(Dataset).where(Dataset.is_deleted.is_(False))
        if name_filter:
            base_stmt = base_stmt.where(Dataset.name.ilike(f"%{name_filter}%"))

        count_stmt = select(func.count()).select_from(base_stmt.subquery())
        total = (await self._session.execute(count_stmt)).scalar_one()

        order_col = Dataset.created_at.desc() if sort_desc else Dataset.created_at.asc()
        page_stmt = base_stmt.order_by(order_col).offset((page - 1) * page_size).limit(page_size)
        rows = (await self._session.execute(page_stmt)).scalars().all()
        return list(rows), total

    async def update_with_optimistic_lock(
        self, *, dataset_id: int, expected_version: int, name: str | None, description: str | None
    ) -> Dataset:
        dataset = await self.get(dataset_id)
        if dataset is None:
            raise LookupError(f"dataset {dataset_id} not found")
        if dataset.version != expected_version:
            raise ConcurrentModificationError(
                f"expected version {expected_version}, current version is {dataset.version}"
            )
        if name is not None:
            dataset.name = name
        if description is not None:
            dataset.description = description
        try:
            await self._session.flush()
        except StaleDataError as exc:
            raise ConcurrentModificationError(str(exc)) from exc
        return dataset

    async def soft_delete(self, dataset_id: int) -> bool:
        dataset = await self.get(dataset_id)
        if dataset is None:
            return False
        dataset.is_deleted = True
        await self._session.flush()
        return True
