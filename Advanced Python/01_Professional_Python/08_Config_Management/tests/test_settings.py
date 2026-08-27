from __future__ import annotations

from pathlib import Path

import pytest

from svcconfig.settings import ConfigurationError, load_settings


def test_load_settings_uses_defaults_when_only_required_field_given() -> None:
    settings = load_settings(environ={}, overrides={"api_key": "test-key"})
    assert settings.environment == "development"
    assert settings.database.host == "localhost"
    assert settings.database.dsn == "postgresql://localhost:5432/bioinformatics"


def test_load_settings_requires_api_key() -> None:
    with pytest.raises(ConfigurationError):
        load_settings(environ={})


def test_env_vars_override_dotenv_and_defaults(tmp_path: Path) -> None:
    dotenv = tmp_path / ".env"
    dotenv.write_text("SVC_API_KEY=from-dotenv\nSVC_DB_HOST=dotenv-host\n")
    settings = load_settings(
        env_file=dotenv,
        environ={"SVC_DB_HOST": "env-host"},
    )
    assert settings.api_key == "from-dotenv"
    assert settings.database.host == "env-host"


def test_explicit_overrides_win_over_everything(tmp_path: Path) -> None:
    dotenv = tmp_path / ".env"
    dotenv.write_text("SVC_API_KEY=from-dotenv\n")
    settings = load_settings(
        env_file=dotenv,
        environ={"SVC_API_KEY": "from-env"},
        overrides={"api_key": "from-overrides"},
    )
    assert settings.api_key == "from-overrides"


def test_production_with_debug_is_rejected() -> None:
    with pytest.raises(ConfigurationError):
        load_settings(
            environ={},
            overrides={"api_key": "k", "environment": "production", "debug": True},
        )


def test_boolean_coercion_from_environment() -> None:
    settings = load_settings(environ={"SVC_API_KEY": "k", "SVC_DEBUG": "true"})
    assert settings.debug is True
