from __future__ import annotations

from uuid import UUID, uuid4

from fastapi import APIRouter, Response, status
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1", tags=["compounds-v1"])

_DEPRECATION_DATE = "2026-12-31"
_SUNSET_HEADER = "Sat, 31 Dec 2026 23:59:59 GMT"


class CompoundV1(BaseModel):
    compound_id: UUID
    name: str
    formula: str


_STORE_V1: dict[UUID, CompoundV1] = {}


@router.get("/compounds/{compound_id}", response_model=CompoundV1)
async def get_compound_v1(compound_id: UUID, response: Response) -> CompoundV1:
    response.headers["Deprecation"] = f"date={_DEPRECATION_DATE}"
    response.headers["Sunset"] = _SUNSET_HEADER
    response.headers["Link"] = f'</api/v2/compounds/{compound_id}>; rel="successor-version"'
    compound = _STORE_V1.get(compound_id) or CompoundV1(compound_id=compound_id, name="Unknown", formula="")
    return compound


@router.post("/compounds", response_model=CompoundV1, status_code=status.HTTP_201_CREATED)
async def create_compound_v1(payload: CompoundV1, response: Response) -> CompoundV1:
    response.headers["Deprecation"] = f"date={_DEPRECATION_DATE}"
    _STORE_V1[payload.compound_id] = payload
    return payload
