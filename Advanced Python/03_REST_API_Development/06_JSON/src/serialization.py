from __future__ import annotations

import json
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Iterator
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_serializer


class AnalysisJobStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class ModelPrediction(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    prediction_id: UUID
    compound_id: UUID
    target_protein: str
    binding_affinity_nm: Decimal = Field(description="Predicted binding affinity in nanomolar units.")
    confidence: float = Field(ge=0.0, le=1.0)
    generated_at: datetime

    @field_serializer("binding_affinity_nm")
    def serialize_affinity(self, value: Decimal) -> str:
        return format(value, "f")


class AnalysisJob(BaseModel):
    job_id: UUID
    status: AnalysisJobStatus
    submitted_on: date
    predictions: list[ModelPrediction] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ScientificJSONEncoder(json.JSONEncoder):
    def default(self, o: object) -> object:
        if isinstance(o, (datetime, date)):
            return o.isoformat()
        if isinstance(o, Decimal):
            return format(o, "f")
        if isinstance(o, UUID):
            return str(o)
        if isinstance(o, Enum):
            return o.value
        return super().default(o)


def serialize_job(job: AnalysisJob) -> str:
    return job.model_dump_json(by_alias=True)


def deserialize_job(payload: str) -> AnalysisJob:
    return AnalysisJob.model_validate_json(payload)


def stream_large_prediction_payload(predictions: list[ModelPrediction], chunk_size: int = 500) -> Iterator[str]:
    yield '{"predictions": ['
    total = len(predictions)
    for index in range(0, total, chunk_size):
        chunk = predictions[index : index + chunk_size]
        serialized_items = ",".join(prediction.model_dump_json() for prediction in chunk)
        yield serialized_items
        if index + chunk_size < total:
            yield ","
    yield "]}"


def safe_parse_json(raw_payload: str, *, max_bytes: int = 5_000_000) -> dict[str, Any]:
    encoded_size = len(raw_payload.encode("utf-8"))
    if encoded_size > max_bytes:
        raise ValueError(f"Payload of {encoded_size} bytes exceeds the {max_bytes} byte limit.")
    try:
        return json.loads(raw_payload)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON payload at line {exc.lineno}, column {exc.colno}.") from exc
