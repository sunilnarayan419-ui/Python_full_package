from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from .cursor import DatasetCursor, InvalidCursorError
from .models import Dataset

router = APIRouter(prefix="/api/v1", tags=["datasets"])


class DatasetResponse(BaseModel):
    dataset_id: UUID
    name: str
    source: str
    quality_score: float


class DatasetPage(BaseModel):
    items: list[DatasetResponse]
    next_cursor: str | None
    has_more: bool


async def get_db_session() -> AsyncSession:  # pragma: no cover - wired at app startup
    raise NotImplementedError("Overridden by dependency_overrides in application startup.")


@router.get("/datasets", response_model=DatasetPage)
async def list_datasets(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    cursor: str | None = Query(default=None),
    page_size: int = Query(default=50, ge=1, le=500),
) -> DatasetPage:
    stmt = select(Dataset).order_by(Dataset.created_at.desc(), Dataset.dataset_id.desc()).limit(page_size + 1)

    if cursor is not None:
        try:
            decoded = DatasetCursor.decode(cursor)
        except InvalidCursorError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

        stmt = stmt.where(
            or_(
                Dataset.created_at < decoded.created_at,
                and_(Dataset.created_at == decoded.created_at, Dataset.dataset_id < decoded.dataset_id),
            )
        )

    result = await session.execute(stmt)
    rows = list(result.scalars().all())

    has_more = len(rows) > page_size
    page_rows = rows[:page_size]

    next_cursor = None
    if has_more and page_rows:
        last = page_rows[-1]
        next_cursor = DatasetCursor(created_at=last.created_at, dataset_id=last.dataset_id).encode()

    return DatasetPage(
        items=[DatasetResponse.model_validate(row, from_attributes=True) for row in page_rows],
        next_cursor=next_cursor,
        has_more=has_more,
    )
