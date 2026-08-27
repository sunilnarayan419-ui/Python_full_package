from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session
from app.repositories.dataset_repository import ConcurrentModificationError
from app.schemas.dataset_schemas import DatasetCreateRequest, DatasetResponse, DatasetUpdateRequest, Page
from app.services.dataset_service import DatasetNotFoundError, DatasetService

router = APIRouter(prefix="/datasets", tags=["datasets"])


async def _service(session: AsyncSession = Depends(get_session)) -> DatasetService:
    return DatasetService(session)


@router.post("", response_model=DatasetResponse, status_code=status.HTTP_201_CREATED)
async def create_dataset(payload: DatasetCreateRequest, service: DatasetService = Depends(_service)):
    dataset = await service.create_dataset(payload)
    return DatasetResponse.model_validate(dataset)


@router.get("/{dataset_id}", response_model=DatasetResponse)
async def get_dataset(dataset_id: int, service: DatasetService = Depends(_service)):
    try:
        dataset = await service.get_dataset(dataset_id)
    except DatasetNotFoundError:
        raise HTTPException(status_code=404, detail="dataset not found")
    return DatasetResponse.model_validate(dataset)


@router.get("", response_model=Page)
async def list_datasets(
    page: int = 1,
    page_size: int = 25,
    name: str | None = None,
    service: DatasetService = Depends(_service),
):
    return await service.list_datasets(page=page, page_size=page_size, name_filter=name)


@router.patch("/{dataset_id}", response_model=DatasetResponse)
async def update_dataset(
    dataset_id: int, payload: DatasetUpdateRequest, service: DatasetService = Depends(_service)
):
    try:
        dataset = await service.update_dataset(dataset_id, payload)
    except DatasetNotFoundError:
        raise HTTPException(status_code=404, detail="dataset not found")
    except ConcurrentModificationError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    return DatasetResponse.model_validate(dataset)


@router.delete("/{dataset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dataset(dataset_id: int, service: DatasetService = Depends(_service)):
    try:
        await service.delete_dataset(dataset_id)
    except DatasetNotFoundError:
        raise HTTPException(status_code=404, detail="dataset not found")
