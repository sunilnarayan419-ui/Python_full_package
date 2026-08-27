from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PG", extra="ignore")

    host: str = Field(...)
    port: int = Field(default=5432)
    database: str = Field(...)
    user: str = Field(...)
    password: str = Field(...)
    pool_min_size: int = Field(default=5)
    pool_max_size: int = Field(default=20)
    command_timeout_seconds: float = Field(default=30.0)


@lru_cache(maxsize=1)
def get_database_settings() -> DatabaseSettings:
    return DatabaseSettings()  # type: ignore[call-arg]
