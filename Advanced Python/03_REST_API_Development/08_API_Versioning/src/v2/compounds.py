from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, Response, status
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v2", tags=["compounds-v2"])


class MolecularProperties(BaseModel):
    molecular_formula: str
    molecular_weight_daltons: float = Field(gt=0)


class CompoundV2(BaseModel):
    compound_id: UUID
    name: str
    properties: MolecularProperties
    created_at: datetime


class CompoundCreateV2(BaseModel):
    name: str
    properties: MolecularProperties


_STORE_V2: dict[UUID, CompoundV2] = {}


def migrate_v1_payload_to_v2(name: str, formula: str) -> CompoundCreateV2:
    return CompoundCreateV2(
        name=name,
        properties=MolecularProperties(molecular_formula=formula, molecular_weight_daltons=0.0),
    )


@router.get("/compounds/{compound_id}", response_model=CompoundV2)
async def get_compound_v2(compound_id: UUID) -> CompoundV2:
    compound = _STORE_V2.get(compound_id)
    if compound is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Compound not found.")
    return compound


@router.post("/compounds", response_model=CompoundV2, status_code=status.HTTP_201_CREATED)
async def create_compound_v2(payload: CompoundCreateV2, response: Response) -> CompoundV2:
    compound = CompoundV2(
        compound_id=uuid4(),
        name=payload.name,
        properties=payload.properties,
        created_at=datetime.now(timezone.utc),
    )
    _STORE_V2[compound.compound_id] = compound
    response.headers["Location"] = f"/api/v2/compounds/{compound.compound_id}"
    return compound
