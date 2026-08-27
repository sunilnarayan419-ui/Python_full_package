from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Header, HTTPException, Request, Response, status
from pydantic import BaseModel, ConfigDict, Field

from ..domain.models import Compound, Experiment, ExperimentStatus, InMemoryCompoundStore

router = APIRouter(prefix="/api/v1", tags=["compounds"])
store = InMemoryCompoundStore()

_seed_id = uuid4()
store.add(
    Compound(
        compound_id=_seed_id,
        name="Metformin",
        molecular_formula="C4H11N5",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
)


class CompoundCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    molecular_formula: str = Field(min_length=1, max_length=64)


class CompoundRenameRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)


class Link(BaseModel):
    rel: str
    href: str
    method: str


class CompoundResource(BaseModel):
    compound_id: UUID
    name: str
    molecular_formula: str
    version: int
    updated_at: datetime
    links: list[Link]

    @classmethod
    def from_domain(cls, compound: Compound) -> "CompoundResource":
        base = f"/api/v1/compounds/{compound.compound_id}"
        return cls(
            compound_id=compound.compound_id,
            name=compound.name,
            molecular_formula=compound.molecular_formula,
            version=compound.version,
            updated_at=compound.updated_at,
            links=[
                Link(rel="self", href=base, method="GET"),
                Link(rel="experiments", href=f"{base}/experiments", method="GET"),
                Link(rel="rename", href=base, method="PATCH"),
            ],
        )


class ExperimentResource(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    experiment_id: UUID
    compound_id: UUID
    title: str
    status: ExperimentStatus
    created_at: datetime


def _get_compound_or_404(compound_id: UUID) -> Compound:
    compound = store.get(compound_id)
    if compound is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Compound not found.")
    return compound


@router.post("/compounds", response_model=CompoundResource, status_code=status.HTTP_201_CREATED)
async def create_compound(payload: CompoundCreateRequest, response: Response) -> CompoundResource:
    compound = Compound(
        compound_id=uuid4(),
        name=payload.name,
        molecular_formula=payload.molecular_formula,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    store.add(compound)
    response.headers["Location"] = f"/api/v1/compounds/{compound.compound_id}"
    response.headers["ETag"] = f'"{compound.etag()}"'
    return CompoundResource.from_domain(compound)


@router.get("/compounds/{compound_id}", response_model=CompoundResource)
async def get_compound(compound_id: UUID, response: Response) -> CompoundResource:
    compound = _get_compound_or_404(compound_id)
    response.headers["ETag"] = f'"{compound.etag()}"'
    return CompoundResource.from_domain(compound)


@router.patch("/compounds/{compound_id}", response_model=CompoundResource)
async def rename_compound(
    compound_id: UUID,
    payload: CompoundRenameRequest,
    response: Response,
    if_match: Annotated[str | None, Header(alias="If-Match")] = None,
) -> CompoundResource:
    compound = _get_compound_or_404(compound_id)
    if if_match is None or if_match.strip('"') != compound.etag():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="ETag mismatch. Refetch the compound before retrying the update.",
        )
    compound.rename(payload.name)
    response.headers["ETag"] = f'"{compound.etag()}"'
    return CompoundResource.from_domain(compound)


@router.delete("/compounds/{compound_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_compound(compound_id: UUID) -> Response:
    _get_compound_or_404(compound_id)
    del store._compounds[compound_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/compounds/{compound_id}/experiments", response_model=list[ExperimentResource])
async def list_experiments(compound_id: UUID) -> list[ExperimentResource]:
    _get_compound_or_404(compound_id)
    experiments = store.list_experiments(compound_id)
    return [ExperimentResource.model_validate(exp) for exp in experiments]


class ExperimentCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=255)


@router.post(
    "/compounds/{compound_id}/experiments",
    response_model=ExperimentResource,
    status_code=status.HTTP_201_CREATED,
)
async def schedule_experiment(
    compound_id: UUID, payload: ExperimentCreateRequest, request: Request, response: Response
) -> ExperimentResource:
    _get_compound_or_404(compound_id)
    experiment = Experiment.schedule(compound_id=compound_id, title=payload.title)
    store.add_experiment(experiment)
    response.headers["Location"] = f"/api/v1/experiments/{experiment.experiment_id}"
    return ExperimentResource.model_validate(experiment)
