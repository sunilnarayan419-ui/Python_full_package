from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Annotated

from fastapi import FastAPI, Header, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI(
    title="Compound Registry HTTP Service",
    description="Reference HTTP semantics for a pharmaceutical compound registry.",
    version="1.0.0",
)


@dataclass(slots=True)
class CompoundRecord:
    compound_id: str
    name: str
    molecular_formula: str
    updated_at: datetime
    etag: str = field(init=False)

    def __post_init__(self) -> None:
        self.etag = self._compute_etag()

    def _compute_etag(self) -> str:
        payload = f"{self.compound_id}:{self.name}:{self.molecular_formula}:{self.updated_at.isoformat()}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


class CompoundResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    compound_id: str
    name: str
    molecular_formula: str
    updated_at: datetime


_REGISTRY: dict[str, CompoundRecord] = {
    "CMP-0001": CompoundRecord(
        compound_id="CMP-0001",
        name="Ibuprofen",
        molecular_formula="C13H18O2",
        updated_at=datetime(2026, 1, 10, tzinfo=timezone.utc),
    )
}

_IDEMPOTENCY_CACHE: dict[str, tuple[int, dict]] = {}
_RATE_WINDOW_SECONDS = 60
_RATE_MAX_REQUESTS = 120
_RATE_STATE: dict[str, list[float]] = {}


def _enforce_rate_limit(client_id: str) -> tuple[int, int]:
    now = time.monotonic()
    window_start = now - _RATE_WINDOW_SECONDS
    history = _RATE_STATE.setdefault(client_id, [])
    history[:] = [timestamp for timestamp in history if timestamp > window_start]
    if len(history) >= _RATE_MAX_REQUESTS:
        retry_after = int(_RATE_WINDOW_SECONDS - (now - history[0]))
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded for compound registry API.",
            headers={"Retry-After": str(max(retry_after, 1))},
        )
    history.append(now)
    return len(history), _RATE_MAX_REQUESTS - len(history)


@app.middleware("http")
async def apply_standard_headers(request: Request, call_next):
    client_id = request.headers.get("x-api-key", request.client.host if request.client else "anonymous")
    used, remaining = _enforce_rate_limit(client_id)
    response: Response = await call_next(request)
    response.headers["X-RateLimit-Limit"] = str(_RATE_MAX_REQUESTS)
    response.headers["X-RateLimit-Remaining"] = str(max(remaining, 0))
    response.headers["X-RateLimit-Used"] = str(used)
    response.headers["Cache-Control"] = "no-store"
    return response


@app.get(
    "/api/v1/compounds/{compound_id}",
    response_model=CompoundResponse,
    responses={
        304: {"description": "Not Modified"},
        404: {"description": "Compound not found"},
    },
)
async def get_compound(
    compound_id: str,
    response: Response,
    if_none_match: Annotated[str | None, Header(alias="If-None-Match")] = None,
) -> CompoundResponse | Response:
    record = _REGISTRY.get(compound_id)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Compound not found.")

    if if_none_match is not None and if_none_match.strip('"') == record.etag:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED, headers={"ETag": f'"{record.etag}"'})

    response.headers["ETag"] = f'"{record.etag}"'
    response.headers["Last-Modified"] = record.updated_at.strftime("%a, %d %b %Y %H:%M:%S GMT")
    return CompoundResponse.model_validate(record)


class CompoundUpdateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    molecular_formula: str = Field(min_length=1, max_length=64)


@app.put(
    "/api/v1/compounds/{compound_id}",
    response_model=CompoundResponse,
    responses={
        409: {"description": "ETag mismatch - concurrent modification"},
        412: {"description": "Precondition failed"},
    },
)
async def replace_compound(
    compound_id: str,
    payload: CompoundUpdateRequest,
    response: Response,
    if_match: Annotated[str | None, Header(alias="If-Match")] = None,
) -> CompoundResponse:
    record = _REGISTRY.get(compound_id)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Compound not found.")

    if if_match is None:
        raise HTTPException(
            status_code=status.HTTP_428_PRECONDITION_REQUIRED,
            detail="If-Match header is required for optimistic concurrency control.",
        )
    if if_match.strip('"') != record.etag:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Compound was modified by another client. Refetch and retry.",
        )

    updated = CompoundRecord(
        compound_id=record.compound_id,
        name=payload.name,
        molecular_formula=payload.molecular_formula,
        updated_at=datetime.now(timezone.utc),
    )
    _REGISTRY[compound_id] = updated
    response.headers["ETag"] = f'"{updated.etag}"'
    return CompoundResponse.model_validate(updated)


class ScreeningRunRequest(BaseModel):
    compound_id: str
    assay_type: str
    requested_by: str


@app.post(
    "/api/v1/screening-runs",
    status_code=status.HTTP_201_CREATED,
    responses={200: {"description": "Existing run returned via idempotency key"}},
)
async def create_screening_run(
    payload: ScreeningRunRequest,
    response: Response,
    idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
) -> dict:
    if idempotency_key is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Idempotency-Key header is required for screening run creation.",
        )

    cached = _IDEMPOTENCY_CACHE.get(idempotency_key)
    if cached is not None:
        cached_status, cached_body = cached
        response.status_code = status.HTTP_200_OK
        response.headers["Idempotency-Replayed"] = "true"
        return cached_body

    run_id = f"RUN-{abs(hash((payload.compound_id, payload.assay_type, idempotency_key))) % 10**8:08d}"
    body = {
        "run_id": run_id,
        "compound_id": payload.compound_id,
        "assay_type": payload.assay_type,
        "status": "queued",
    }
    _IDEMPOTENCY_CACHE[idempotency_key] = (status.HTTP_201_CREATED, body)
    response.headers["Location"] = f"/api/v1/screening-runs/{run_id}"
    return body


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": exc.detail,
                "request_id": request.headers.get("x-request-id", "unknown"),
            }
        },
        headers=exc.headers or {},
    )
