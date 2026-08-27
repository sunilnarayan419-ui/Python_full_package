from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DatasetCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=256)
    description: str = Field(default="", max_length=2000)


class DatasetUpdateRequest(BaseModel):
    """Partial update — only provided fields are applied."""

    name: str | None = Field(default=None, min_length=1, max_length=256)
    description: str | None = Field(default=None, max_length=2000)
    expected_version: int = Field(description="Client's last-known version, for optimistic concurrency")


class DatasetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    dataset_id: int
    name: str
    description: str
    version: int
    created_at: datetime
    updated_at: datetime


class Page(BaseModel):
    items: list[DatasetResponse]
    total: int
    page: int
    page_size: int
