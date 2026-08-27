"""Typed, immutable configuration management for a bioinformatics API
service, with environment-variable overrides, precedence rules, and no
hardcoded secrets.

Precedence (highest to lowest):
  1. Explicit `overrides` dict passed to `load_settings`
  2. Environment variables (prefixed `SVC_`)
  3. `.env` file values (loaded only if present; never required)
  4. Built-in defaults
"""
from __future__ import annotations

import os
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any, Literal

Environment = Literal["development", "test", "production"]

_ENV_PREFIX = "SVC_"


class ConfigurationError(Exception):
    pass


def _parse_dotenv(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


@dataclass(frozen=True, slots=True)
class DatabaseSettings:
    host: str
    port: int
    name: str
    pool_size: int = 10

    @property
    def dsn(self) -> str:
        return f"postgresql://{self.host}:{self.port}/{self.name}"


@dataclass(frozen=True, slots=True)
class AppSettings:
    environment: Environment
    database: DatabaseSettings
    api_key: str
    debug: bool = False
    request_timeout_seconds: float = 30.0

    def __post_init__(self) -> None:
        if self.environment == "production" and self.debug:
            raise ConfigurationError("debug mode must not be enabled in production")
        if not self.api_key:
            raise ConfigurationError("api_key must not be empty")


def _coerce(raw: str, annotation: type[Any]) -> Any:
    if annotation is bool:
        return raw.strip().lower() in {"1", "true", "yes", "on"}
    if annotation is int:
        return int(raw)
    if annotation is float:
        return float(raw)
    return raw


def load_settings(
    *,
    env_file: Path | None = None,
    environ: dict[str, str] | None = None,
    overrides: dict[str, Any] | None = None,
) -> AppSettings:
    """Build immutable `AppSettings` respecting the documented precedence.

    `environ` defaults to `os.environ` but can be injected for tests,
    keeping this function pure and independent of global process state.
    """
    process_environ = environ if environ is not None else dict(os.environ)
    dotenv_values = _parse_dotenv(env_file) if env_file is not None else {}
    merged_env = {**dotenv_values, **process_environ}

    def resolve(key: str, default: Any, annotation: type[Any]) -> Any:
        override_key = key
        if overrides and override_key in overrides:
            return overrides[override_key]
        env_key = f"{_ENV_PREFIX}{key.upper()}"
        if env_key in merged_env:
            return _coerce(merged_env[env_key], annotation)
        return default

    environment: Environment = resolve("environment", "development", str)
    database = DatabaseSettings(
        host=resolve("db_host", "localhost", str),
        port=resolve("db_port", 5432, int),
        name=resolve("db_name", "bioinformatics", str),
        pool_size=resolve("db_pool_size", 10, int),
    )
    api_key = resolve("api_key", "", str)
    if not api_key:
        raise ConfigurationError(
            "SVC_API_KEY must be set via environment variable, .env file, or overrides"
        )

    return AppSettings(
        environment=environment,
        database=database,
        api_key=api_key,
        debug=resolve("debug", False, bool),
        request_timeout_seconds=resolve("request_timeout_seconds", 30.0, float),
    )


def settings_field_names() -> tuple[str, ...]:
    """Introspection helper listing top-level `AppSettings` field names,
    useful for generating documentation or `.env.example` files.
    """
    return tuple(f.name for f in fields(AppSettings))
