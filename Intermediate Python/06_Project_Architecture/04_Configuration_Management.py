"""Demonstrates production-grade configuration management: typed,
immutable configuration objects, validated eagerly, passed explicitly
to services rather than read ad-hoc throughout business logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class ConfigurationError(ValueError):
    """Raised when application configuration is invalid or incomplete."""


class Environment(Enum):
    LOCAL = "local"
    STAGING = "staging"
    PRODUCTION = "production"


@dataclass(frozen=True, slots=True)
class DatabaseConfig:
    """Connection parameters only -- never a raw connection string with
    embedded credentials. Credentials are expected to arrive via a
    secrets manager or environment variable, not this object.
    """

    host: str
    port: int
    database_name: str

    def __post_init__(self) -> None:
        if not (1 <= self.port <= 65535):
            raise ConfigurationError(f"invalid database port: {self.port}")
        if not self.host:
            raise ConfigurationError("database host must not be empty")


@dataclass(frozen=True, slots=True)
class ScientificProcessingConfig:
    """Parameters governing how scientific data is analyzed."""

    max_workers: int
    batch_size: int
    data_directory: Path

    def __post_init__(self) -> None:
        if self.max_workers < 1:
            raise ConfigurationError("max_workers must be at least 1")
        if self.batch_size < 1:
            raise ConfigurationError("batch_size must be at least 1")


@dataclass(frozen=True, slots=True)
class LoggingConfig:
    level: str
    json_format: bool = False

    def __post_init__(self) -> None:
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if self.level not in valid_levels:
            raise ConfigurationError(
                f"invalid log level '{self.level}', expected one of {valid_levels}"
            )


@dataclass(frozen=True, slots=True)
class ApplicationConfig:
    """Root configuration object. Immutable once constructed: a service
    that receives this object can trust it will not change underneath
    it during a request or processing run.
    """

    environment: Environment
    database: DatabaseConfig
    processing: ScientificProcessingConfig
    logging: LoggingConfig
    feature_flags: frozenset[str] = field(default_factory=frozenset)

    def is_production(self) -> bool:
        return self.environment is Environment.PRODUCTION


def default_local_config() -> ApplicationConfig:
    """Sensible defaults for local development -- never used as-is in
    staging or production.
    """
    return ApplicationConfig(
        environment=Environment.LOCAL,
        database=DatabaseConfig(host="localhost", port=5432, database_name="scientific_dev"),
        processing=ScientificProcessingConfig(
            max_workers=2, batch_size=50, data_directory=Path("./data")
        ),
        logging=LoggingConfig(level="DEBUG"),
    )


class ExperimentBatchService:
    """Example service that RECEIVES configuration rather than reading
    it from the environment itself, keeping the service testable and
    the configuration source swappable.
    """

    def __init__(self, config: ApplicationConfig) -> None:
        self._config = config

    def describe_run(self) -> str:
        return (
            f"environment={self._config.environment.value} "
            f"workers={self._config.processing.max_workers} "
            f"batch_size={self._config.processing.batch_size} "
            f"log_level={self._config.logging.level}"
        )


if __name__ == "__main__":
    config = default_local_config()
    service = ExperimentBatchService(config)
    print(service.describe_run())

    try:
        DatabaseConfig(host="db.internal", port=70000, database_name="prod")
    except ConfigurationError as exc:
        print(f"Rejected invalid configuration as expected: {exc}")
