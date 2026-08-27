from __future__ import annotations

import uuid
from typing import Annotated
from uuid import UUID

from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import JSONResponse

from ..domain.entities import DomainError, ScreeningRunNotFoundError
from ..repositories.screening_run_repository import InMemoryScreeningRunRepository, ScreeningRunRepository
from ..schemas.screening_run_schemas import (
    ErrorDetail,
    ErrorResponse,
    PageMeta,
    ScreeningRunCreateRequest,
    ScreeningRunPage,
    ScreeningRunResponse,
    ScreeningRunTransitionRequest,
)
from ..services.screening_service import ScreeningService

app = FastAPI(title="Screening Platform API", version="1.0.0")

_repository = InMemoryScreeningRunRepository()


def get_repository() -> ScreeningRunRepository:
    return _repository


def get_service(
    repository: Annotated[ScreeningRunRepository, Depends(get_repository)],
) -> ScreeningService:
    return ScreeningService(repository)


@app.middleware("http")
async def attach_correlation_id(request: Request, call_next):
    request.state.request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
    response = await call_next(request)
    response.headers["X-Request-ID"] = request.state.request_id
    return response


@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
    status_code = status.HTTP_404_NOT_FOUND if isinstance(exc, ScreeningRunNotFoundError) else status.HTTP_409_CONFLICT
    request_id = getattr(request.state, "request_id", "unknown")
    body = ErrorResponse(error=ErrorDetail(code=exc.code, message=exc.message, request_id=request_id))
    return JSONResponse(status_code=status_code, content=body.model_dump())


@app.post("/api/v1/screening-runs", response_model=ScreeningRunResponse, status_code=status.HTTP_201_CREATED)
async def submit_screening_run(
    payload: ScreeningRunCreateRequest,
    service: Annotated[ScreeningService, Depends(get_service)],
) -> ScreeningRunResponse:
    run = await service.submit_run(payload.compound_id, payload.assay_type)
    return ScreeningRunResponse.model_validate(run)


@app.get("/api/v1/screening-runs/{run_id}", response_model=ScreeningRunResponse)
async def get_screening_run(
    run_id: UUID,
    service: Annotated[ScreeningService, Depends(get_service)],
) -> ScreeningRunResponse:
    run = await service.get_run(run_id)
    return ScreeningRunResponse.model_validate(run)


@app.patch("/api/v1/screening-runs/{run_id}", response_model=ScreeningRunResponse)
async def transition_screening_run(
    run_id: UUID,
    payload: ScreeningRunTransitionRequest,
    service: Annotated[ScreeningService, Depends(get_service)],
) -> ScreeningRunResponse:
    run = await service.advance_run(run_id, payload.target_status, score=payload.score)
    return ScreeningRunResponse.model_validate(run)


@app.get("/api/v1/compounds/{compound_id}/screening-runs", response_model=ScreeningRunPage)
async def list_screening_runs(
    compound_id: UUID,
    service: Annotated[ScreeningService, Depends(get_service)],
    limit: int = 20,
    offset: int = 0,
) -> ScreeningRunPage:
    runs = await service.list_runs(compound_id, limit=limit, offset=offset)
    return ScreeningRunPage(
        items=[ScreeningRunResponse.model_validate(run) for run in runs],
        meta=PageMeta(limit=limit, offset=offset, count=len(runs)),
    )
