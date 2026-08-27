"""
03_JSON.py

Production JSON serialization/deserialization for scientific data, using
explicit schemas rather than blindly serializing arbitrary Python objects.

Demonstrates:
    Python object -> JSON       (encoding: dataclasses, datetime, enum)
    JSON -> Python object       (decoding: validation at the boundary)

Never uses pickle. Never dumps arbitrary __dict__ contents. Never exposes
internal fields that were not explicitly whitelisted for the wire format.
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass, field, fields
from datetime import date, datetime, UTC
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class AssayType(str, Enum):
    """Enum serializes to its string value, not its Python name, so the
    wire format stays stable even if members are reordered."""

    ELISA = "elisa"
    PCR = "pcr"
    SEQUENCING = "sequencing"
    MASS_SPEC = "mass_spec"


class MalformedJSONError(ValueError):
    """Raised when inbound JSON cannot be parsed at all."""


class SchemaValidationError(ValueError):
    """Raised when parsed JSON does not match the expected schema."""


@dataclass(slots=True)
class Measurement:
    """Domain object for a single scientific measurement."""

    sample_id: str
    assay_type: AssayType
    value: float
    unit: str
    recorded_at: datetime
    replicate: int = 1
    notes: str | None = None


class ScientificJSONEncoder(json.JSONEncoder):
    """Custom encoder covering the types that appear in this domain and
    that `json` does not support natively: datetime/date and Enum."""

    def default(self, o: Any) -> Any:
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, date):
            return o.isoformat()
        if isinstance(o, Enum):
            return o.value
        return super().default(o)


def measurement_to_json(measurement: Measurement) -> str:
    """Python object -> JSON.

    Uses an explicit dict rather than dumping `__dict__`/`asdict` blindly,
    so the wire schema is a deliberate contract, not an accident of the
    internal representation.
    """
    payload = {
        "sample_id": measurement.sample_id,
        "assay_type": measurement.assay_type,  # Enum, handled by encoder
        "value": measurement.value,
        "unit": measurement.unit,
        "recorded_at": measurement.recorded_at,  # datetime, handled by encoder
        "replicate": measurement.replicate,
        "notes": measurement.notes,
    }
    return json.dumps(payload, cls=ScientificJSONEncoder, separators=(",", ":"))


def measurements_to_json(measurements: list[Measurement]) -> str:
    return json.dumps(
        [json.loads(measurement_to_json(m)) for m in measurements],
        separators=(",", ":"),
    )


_REQUIRED_FIELDS = {"sample_id", "assay_type", "value", "unit", "recorded_at"}


def json_to_measurement(raw: str | bytes) -> Measurement:
    """JSON -> Python object, with explicit validation at the boundary.

    Any malformed or non-conforming input raises a typed exception rather
    than propagating a raw json.JSONDecodeError or KeyError to the caller.
    """
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise MalformedJSONError(f"invalid JSON payload: {exc}") from exc

    if not isinstance(data, dict):
        raise SchemaValidationError("expected a JSON object at the top level")

    missing = _REQUIRED_FIELDS - data.keys()
    if missing:
        raise SchemaValidationError(f"missing required fields: {sorted(missing)}")

    try:
        assay_type = AssayType(data["assay_type"])
    except ValueError as exc:
        valid = [a.value for a in AssayType]
        raise SchemaValidationError(
            f"invalid assay_type '{data['assay_type']}', expected one of {valid}"
        ) from exc

    try:
        value = float(data["value"])
    except (TypeError, ValueError) as exc:
        raise SchemaValidationError("value must be numeric") from exc

    try:
        recorded_at = datetime.fromisoformat(str(data["recorded_at"]))
    except ValueError as exc:
        raise SchemaValidationError("recorded_at must be ISO 8601") from exc

    replicate = data.get("replicate", 1)
    if not isinstance(replicate, int) or replicate < 1:
        raise SchemaValidationError("replicate must be a positive integer")

    notes = data.get("notes")
    if notes is not None and not isinstance(notes, str):
        raise SchemaValidationError("notes must be a string or null")

    return Measurement(
        sample_id=str(data["sample_id"]),
        assay_type=assay_type,
        value=value,
        unit=str(data["unit"]),
        recorded_at=recorded_at,
        replicate=replicate,
        notes=notes,
    )


def _demo() -> None:
    logging.basicConfig(level=logging.INFO)

    measurement = Measurement(
        sample_id="SMP-001",
        assay_type=AssayType.PCR,
        value=34.2,
        unit="Ct",
        recorded_at=datetime.now(UTC),
        replicate=2,
        notes="Repeat run after reagent swap",
    )

    encoded = measurement_to_json(measurement)
    logger.info("encoded: %s", encoded)

    decoded = json_to_measurement(encoded)
    assert decoded.sample_id == measurement.sample_id
    assert decoded.assay_type == AssayType.PCR

    try:
        json_to_measurement("{not valid json")
    except MalformedJSONError as exc:
        logger.info("correctly rejected malformed JSON: %s", exc)

    try:
        json_to_measurement(json.dumps({"sample_id": "SMP-002"}))
    except SchemaValidationError as exc:
        logger.info("correctly rejected incomplete schema: %s", exc)

    logger.info("JSON encode/decode demo completed successfully")


if __name__ == "__main__":
    _demo()
