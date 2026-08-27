"""Demonstrates clean environment-variable handling: a single loading
boundary that converts raw environment strings into a typed
ApplicationConfig, so business logic never calls os.getenv() directly.

Boundary:

    Environment -> Configuration Loader -> Typed ApplicationConfig -> Services
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from enum import Enum


class ConfigurationError(ValueError):
    """Raised when required environment configuration is missing or invalid."""


class ScientificEnvironment(Enum):
    LOCAL = "local"
    STAGING = "staging"
    PRODUCTION = "production"


@dataclass(frozen=True, slots=True)
class ApplicationConfig:
    environment: ScientificEnvironment
    data_directory: str
    max_workers: int
    log_level: str


def _require(env: dict[str, str], name: str) -> str:
    value = env.get(name)
    if value is None or value.strip() == "":
        raise ConfigurationError(f"required environment variable '{name}' is not set")
    return value


def _optional(env: dict[str, str], name: str, default: str) -> str:
    value = env.get(name)
    return value if value not in (None, "") else default


def _parse_environment(raw_value: str) -> ScientificEnvironment:
    try:
        return ScientificEnvironment(raw_value.lower())
    except ValueError as exc:
        valid = [e.value for e in ScientificEnvironment]
        raise ConfigurationError(
            f"invalid SCIENTIFIC_ENV '{raw_value}', expected one of {valid}"
        ) from exc


def _parse_positive_int(name: str, raw_value: str) -> int:
    try:
        parsed = int(raw_value)
    except ValueError as exc:
        raise ConfigurationError(f"{name} must be an integer, got '{raw_value}'") from exc
    if parsed < 1:
        raise ConfigurationError(f"{name} must be a positive integer, got {parsed}")
    return parsed


def load_config(env: dict[str, str] | None = None) -> ApplicationConfig:
    """Loads and validates configuration from environment variables.

    This is the ONLY function in the application permitted to call
    os.getenv() / read from the environment mapping directly. Everything
    downstream receives a typed, already-validated ApplicationConfig.

    Raises:
        ConfigurationError: if a required variable is missing or a
            provided value cannot be parsed into its expected type.
    """
    source = env if env is not None else dict(os.environ)

    environment = _parse_environment(_require(source, "SCIENTIFIC_ENV"))
    data_directory = _require(source, "DATA_DIRECTORY")
    max_workers = _parse_positive_int(
        "MAX_WORKERS", _optional(source, "MAX_WORKERS", "4")
    )
    log_level = _optional(source, "LOG_LEVEL", "INFO").upper()

    return ApplicationConfig(
        environment=environment,
        data_directory=data_directory,
        max_workers=max_workers,
        log_level=log_level,
    )


if __name__ == "__main__":
    simulated_environment = {
        "SCIENTIFIC_ENV": "staging",
        "DATA_DIRECTORY": "/var/data/scientific_platform",
        "MAX_WORKERS": "8",
        # LOG_LEVEL intentionally omitted to demonstrate the default.
    }

    config = load_config(simulated_environment)
    print(
        f"Loaded config: environment={config.environment.value} "
        f"data_directory={config.data_directory} "
        f"max_workers={config.max_workers} "
        f"log_level={config.log_level}"
    )

    try:
        load_config({"SCIENTIFIC_ENV": "staging"})  # missing DATA_DIRECTORY
    except ConfigurationError as exc:
        print(f"Correctly rejected incomplete environment: {exc}")
