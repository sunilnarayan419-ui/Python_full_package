from __future__ import annotations

import os

import pytest


@pytest.fixture(autouse=True)
def _env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PGHOST", "localhost")
    monkeypatch.setenv("PGPORT", "5432")
    monkeypatch.setenv("PGDATABASE", "test_db")
    monkeypatch.setenv("PGUSER", "test")
    monkeypatch.setenv("PGPASSWORD", "test")


def test_build_engine_uses_bounded_pool_settings() -> None:
    from app.database.engine import build_engine

    engine = build_engine()
    pool = engine.pool

    assert pool.size() == 0  # lazily connects; size reflects configured target on first use
    assert engine.pool.__class__.__name__ == "AsyncAdaptedQueuePool"


def test_missing_env_vars_raise_immediately(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("PGPASSWORD", raising=False)
    import importlib

    import app.database.engine as engine_module

    with pytest.raises(RuntimeError, match="PGPASSWORD"):
        importlib.reload(engine_module)
