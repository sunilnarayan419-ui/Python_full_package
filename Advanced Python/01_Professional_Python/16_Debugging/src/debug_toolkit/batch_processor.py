"""Realistic failure scenario: a batch record-processing job where one
malformed record must not silently corrupt results or crash the whole
batch, and failures must be reproducible in isolation.
"""
from __future__ import annotations

from dataclasses import dataclass

from .diagnostics import FailureContext, capture_failure_context


class BatchProcessingError(Exception):
    def __init__(self, message: str, *, failed_records: list["RecordFailure"]) -> None:
        super().__init__(message)
        self.failed_records = failed_records


@dataclass(frozen=True, slots=True)
class RecordFailure:
    index: int
    raw_record: dict[str, object]
    context: FailureContext


def _normalize_dosage(record: dict[str, object]) -> float:
    raw_value = record["dosage_mg"]
    return float(raw_value)  # raises TypeError/ValueError on malformed input


def process_batch(records: list[dict[str, object]]) -> list[float]:
    normalized: list[float] = []
    failures: list[RecordFailure] = []
    for index, record in enumerate(records):
        try:
            normalized.append(_normalize_dosage(record))
        except (KeyError, TypeError, ValueError) as exc:
            failures.append(
                RecordFailure(index=index, raw_record=record, context=capture_failure_context(exc))
            )
    if failures:
        raise BatchProcessingError(
            f"{len(failures)} of {len(records)} records failed normalization",
            failed_records=failures,
        )
    return normalized
