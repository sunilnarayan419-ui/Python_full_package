from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Mapping

logger = logging.getLogger(__name__)


class DataFormatError(ValueError):
    """Raised when input data does not match the expected format."""


class DataValidationError(ValueError):
    """Raised when parsed data fails scientific validation."""


class FileProcessingError(RuntimeError):
    """Raised when a file-processing operation fails."""


class MeasurementUnit(str, Enum):
    MICROGRAM_PER_ML = "ug/mL"
    NANOGRAM_PER_ML = "ng/mL"
    COUNT = "count"


@dataclass(frozen=True, slots=True)
class Measurement:
    analyte: str
    value: float
    unit: MeasurementUnit


@dataclass(frozen=True, slots=True)
class Sample:
    sample_id: str
    species: str
    measurements: tuple[Measurement, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class Experiment:
    experiment_id: str
    recorded_at: datetime
    samples: tuple[Sample, ...] = field(default_factory=tuple)


class ExperimentJSONEncoder(json.JSONEncoder):
    """Encoder handling domain types not natively supported by json."""

    def default(self, o: Any) -> Any:
        if isinstance(o, datetime):
            return o.astimezone(timezone.utc).isoformat()
        if isinstance(o, Enum):
            return o.value
        if isinstance(o, Measurement):
            return {"analyte": o.analyte, "value": o.value, "unit": o.unit}
        if isinstance(o, Sample):
            return {
                "sample_id": o.sample_id,
                "species": o.species,
                "measurements": list(o.measurements),
            }
        if isinstance(o, Experiment):
            return {
                "experiment_id": o.experiment_id,
                "recorded_at": o.recorded_at,
                "samples": list(o.samples),
            }
        return super().default(o)


def _require_keys(obj: Mapping[str, Any], keys: tuple[str, ...], context: str) -> None:
    missing = [key for key in keys if key not in obj]
    if missing:
        raise DataFormatError(f"{context}: missing required key(s): {missing}")


def _parse_measurement(raw: Mapping[str, Any]) -> Measurement:
    _require_keys(raw, ("analyte", "value", "unit"), "measurement")
    try:
        unit = MeasurementUnit(raw["unit"])
    except ValueError as exc:
        raise DataValidationError(f"unsupported measurement unit: {raw['unit']!r}") from exc

    value = raw["value"]
    if not isinstance(value, (int, float)):
        raise DataFormatError(f"measurement value must be numeric, got {type(value)!r}")

    return Measurement(analyte=str(raw["analyte"]), value=float(value), unit=unit)


def _parse_sample(raw: Mapping[str, Any]) -> Sample:
    _require_keys(raw, ("sample_id", "species"), "sample")
    raw_measurements = raw.get("measurements", [])
    if not isinstance(raw_measurements, list):
        raise DataFormatError("sample.measurements must be a list")

    return Sample(
        sample_id=str(raw["sample_id"]),
        species=str(raw["species"]),
        measurements=tuple(_parse_measurement(m) for m in raw_measurements),
    )


def parse_experiment(raw: Mapping[str, Any]) -> Experiment:
    """Validate and deserialize a JSON-decoded mapping into an Experiment.

    This boundary function is deliberately strict: arbitrary JSON is never
    trusted directly into application dataclasses without structural checks.
    """
    _require_keys(raw, ("experiment_id", "recorded_at", "samples"), "experiment")

    try:
        recorded_at = datetime.fromisoformat(str(raw["recorded_at"]))
    except ValueError as exc:
        raise DataFormatError(
            f"invalid recorded_at timestamp: {raw['recorded_at']!r}"
        ) from exc

    raw_samples = raw["samples"]
    if not isinstance(raw_samples, list):
        raise DataFormatError("experiment.samples must be a list")

    return Experiment(
        experiment_id=str(raw["experiment_id"]),
        recorded_at=recorded_at,
        samples=tuple(_parse_sample(s) for s in raw_samples),
    )


def load_experiment(json_path: Path) -> Experiment:
    """Load and validate an experiment from a JSON file.

    json.load() reads the full document into memory; this is appropriate
    for typical experiment-record documents, but is not a streaming parser.
    For very large JSON documents, an incremental parser such as `ijson`
    should be used instead of a plain json.load() call.
    """
    if not json_path.is_file():
        raise FileProcessingError(f"JSON file not found: {json_path}")

    try:
        with json_path.open("r", encoding="utf-8") as handle:
            raw = json.load(handle)
    except json.JSONDecodeError as exc:
        raise DataFormatError(f"{json_path}: malformed JSON ({exc})") from exc

    if not isinstance(raw, Mapping):
        raise DataFormatError(f"{json_path}: top-level JSON value must be an object")

    experiment = parse_experiment(raw)
    logger.info(
        "loaded experiment %s with %d sample(s)",
        experiment.experiment_id,
        len(experiment.samples),
    )
    return experiment


def write_experiment(json_path: Path, experiment: Experiment) -> None:
    """Serialize an Experiment to JSON with an atomic temp-file replacement."""
    tmp_path = json_path.with_suffix(json_path.suffix + ".tmp")
    try:
        with tmp_path.open("w", encoding="utf-8") as handle:
            json.dump(
                experiment,
                handle,
                cls=ExperimentJSONEncoder,
                indent=2,
                sort_keys=True,
                ensure_ascii=False,
            )
        tmp_path.replace(json_path)
        logger.info("wrote experiment %s to %s", experiment.experiment_id, json_path)
    except Exception:
        tmp_path.unlink(missing_ok=True)
        raise


def _demo() -> None:
    import tempfile

    logging.basicConfig(level=logging.INFO)

    experiment = Experiment(
        experiment_id="EXP-2025-014",
        recorded_at=datetime(2025, 3, 4, 9, 30, tzinfo=timezone.utc),
        samples=(
            Sample(
                sample_id="S-01",
                species="Arabidopsis thaliana",
                measurements=(
                    Measurement("chlorophyll_a", 3.42, MeasurementUnit.MICROGRAM_PER_ML),
                    Measurement("chlorophyll_b", 1.18, MeasurementUnit.MICROGRAM_PER_ML),
                ),
            ),
            Sample(sample_id="S-02", species="Oryza sativa"),
        ),
    )

    with tempfile.TemporaryDirectory() as tmp_dir:
        json_path = Path(tmp_dir) / "experiment.json"
        write_experiment(json_path, experiment)

        loaded = load_experiment(json_path)
        logger.info("round-tripped experiment: %s", loaded.experiment_id)

        malformed_path = Path(tmp_dir) / "experiment_malformed.json"
        malformed_path.write_text('{"experiment_id": "EXP-BAD"', encoding="utf-8")
        try:
            load_experiment(malformed_path)
        except DataFormatError as exc:
            logger.warning("expected failure on malformed JSON: %s", exc)


if __name__ == "__main__":
    _demo()
