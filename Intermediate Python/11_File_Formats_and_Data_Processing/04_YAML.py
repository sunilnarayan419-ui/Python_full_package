from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

try:
    import yaml
except ImportError as exc:  # pragma: no cover - depends on environment
    raise ImportError(
        "PyYAML is required for YAML processing. Install it with: "
        "pip install pyyaml"
    ) from exc

logger = logging.getLogger(__name__)


class DataFormatError(ValueError):
    """Raised when input data does not match the expected format."""


class DataValidationError(ValueError):
    """Raised when parsed data fails scientific validation."""


class FileProcessingError(RuntimeError):
    """Raised when a file-processing operation fails."""


@dataclass(frozen=True, slots=True)
class ProcessingConfig:
    batch_size: int = 100
    max_workers: int = 4


@dataclass(frozen=True, slots=True)
class ExperimentConfig:
    species: str
    measurement_unit: str


@dataclass(frozen=True, slots=True)
class LoggingConfig:
    level: str = "INFO"


@dataclass(frozen=True, slots=True)
class AppConfig:
    processing: ProcessingConfig
    experiment: ExperimentConfig
    logging: LoggingConfig


_VALID_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


def _require_keys(obj: Mapping[str, Any], keys: tuple[str, ...], context: str) -> None:
    missing = [key for key in keys if key not in obj]
    if missing:
        raise DataFormatError(f"{context}: missing required key(s): {missing}")


def _build_processing_config(raw: Mapping[str, Any]) -> ProcessingConfig:
    batch_size = int(raw.get("batch_size", 100))
    max_workers = int(raw.get("max_workers", 4))

    if batch_size <= 0:
        raise DataValidationError("processing.batch_size must be positive")
    if max_workers <= 0:
        raise DataValidationError("processing.max_workers must be positive")

    return ProcessingConfig(batch_size=batch_size, max_workers=max_workers)


def _build_experiment_config(raw: Mapping[str, Any]) -> ExperimentConfig:
    _require_keys(raw, ("species", "measurement_unit"), "experiment")
    return ExperimentConfig(
        species=str(raw["species"]),
        measurement_unit=str(raw["measurement_unit"]),
    )


def _build_logging_config(raw: Mapping[str, Any]) -> LoggingConfig:
    level = str(raw.get("level", "INFO")).upper()
    if level not in _VALID_LOG_LEVELS:
        raise DataValidationError(
            f"logging.level must be one of {sorted(_VALID_LOG_LEVELS)}, got {level!r}"
        )
    return LoggingConfig(level=level)


def parse_app_config(raw: Mapping[str, Any]) -> AppConfig:
    """Validate and build a typed AppConfig from a YAML-decoded mapping."""
    _require_keys(raw, ("processing", "experiment"), "config")

    processing_raw = raw.get("processing", {})
    experiment_raw = raw["experiment"]
    logging_raw = raw.get("logging", {})

    if not isinstance(processing_raw, Mapping):
        raise DataFormatError("processing section must be a mapping")
    if not isinstance(experiment_raw, Mapping):
        raise DataFormatError("experiment section must be a mapping")
    if not isinstance(logging_raw, Mapping):
        raise DataFormatError("logging section must be a mapping")

    return AppConfig(
        processing=_build_processing_config(processing_raw),
        experiment=_build_experiment_config(experiment_raw),
        logging=_build_logging_config(logging_raw),
    )


def load_app_config(yaml_path: Path) -> AppConfig:
    """Load and validate application configuration from a YAML file.

    yaml.safe_load() is used deliberately: it deserializes only basic YAML
    types (mappings, sequences, scalars) and never constructs arbitrary
    Python objects, which the unsafe yaml.load() default loader can do.
    """
    if not yaml_path.is_file():
        raise FileProcessingError(f"YAML config file not found: {yaml_path}")

    try:
        with yaml_path.open("r", encoding="utf-8") as handle:
            raw = yaml.safe_load(handle)
    except yaml.YAMLError as exc:
        raise DataFormatError(f"{yaml_path}: malformed YAML ({exc})") from exc

    if raw is None:
        raise DataFormatError(f"{yaml_path}: file is empty")
    if not isinstance(raw, Mapping):
        raise DataFormatError(f"{yaml_path}: top-level YAML value must be a mapping")

    config = parse_app_config(raw)
    logger.info(
        "loaded config: batch_size=%d max_workers=%d species=%s",
        config.processing.batch_size,
        config.processing.max_workers,
        config.experiment.species,
    )
    return config


def write_app_config(yaml_path: Path, config: AppConfig) -> None:
    """Serialize AppConfig to YAML with an atomic temp-file replacement.

    yaml.safe_dump() is used to guarantee only standard YAML tags are
    emitted, keeping the resulting file safe to reload with safe_load().
    """
    payload: dict[str, Any] = {
        "processing": {
            "batch_size": config.processing.batch_size,
            "max_workers": config.processing.max_workers,
        },
        "experiment": {
            "species": config.experiment.species,
            "measurement_unit": config.experiment.measurement_unit,
        },
        "logging": {"level": config.logging.level},
    }

    tmp_path = yaml_path.with_suffix(yaml_path.suffix + ".tmp")
    try:
        with tmp_path.open("w", encoding="utf-8") as handle:
            yaml.safe_dump(payload, handle, sort_keys=True, default_flow_style=False)
        tmp_path.replace(yaml_path)
        logger.info("wrote config to %s", yaml_path)
    except Exception:
        tmp_path.unlink(missing_ok=True)
        raise


def _demo() -> None:
    import tempfile

    logging.basicConfig(level=logging.INFO)

    config = AppConfig(
        processing=ProcessingConfig(batch_size=250, max_workers=8),
        experiment=ExperimentConfig(species="Arabidopsis thaliana", measurement_unit="cm"),
        logging=LoggingConfig(level="INFO"),
    )

    with tempfile.TemporaryDirectory() as tmp_dir:
        yaml_path = Path(tmp_dir) / "app_config.yaml"
        write_app_config(yaml_path, config)

        loaded = load_app_config(yaml_path)
        logger.info(
            "round-tripped config for species=%s", loaded.experiment.species
        )

        bad_path = Path(tmp_dir) / "bad_config.yaml"
        bad_path.write_text("processing:\n  batch_size: -5\nexperiment:\n  species: X\n  measurement_unit: cm\n", encoding="utf-8")
        try:
            load_app_config(bad_path)
        except DataValidationError as exc:
            logger.warning("expected validation failure: %s", exc)


if __name__ == "__main__":
    _demo()
