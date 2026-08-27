"""Production logging configuration for a sequence-processing service.

Demonstrates: dictConfig-based setup, JSON structured logging, a
rotating file handler for the application logger, a separate (quieter)
policy for third-party library loggers, a redacting filter to avoid
leaking sensitive data, and contextvars-based correlation IDs.
"""
from __future__ import annotations

import contextvars
import json
import logging
import logging.config
import logging.handlers
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_REQUEST_ID: contextvars.ContextVar[str] = contextvars.ContextVar(
    "request_id", default="-"
)

_SENSITIVE_KEYS = frozenset({"api_key", "password", "token", "patient_ssn"})


def bind_request_id(request_id: str) -> None:
    _REQUEST_ID.set(request_id)


class RequestContextFilter(logging.Filter):
    """Injects the current correlation/request ID into every log record."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = _REQUEST_ID.get()
        return True


class RedactingFilter(logging.Filter):
    """Strips known-sensitive keys from any `extra=` mapping attached
    to a record, preventing accidental leakage into log sinks.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        for key in _SENSITIVE_KEYS:
            if hasattr(record, key):
                setattr(record, key, "***REDACTED***")
        return True


class JsonFormatter(logging.Formatter):
    """Emits one JSON object per log line, suitable for log-aggregation
    pipelines (e.g. shipped to Elasticsearch/CloudWatch).
    """

    _RESERVED = frozenset(logging.LogRecord("", 0, "", 0, "", (), None).__dict__) | {
        "message",
        "asctime",
    }

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": getattr(record, "request_id", "-"),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        for key, value in record.__dict__.items():
            if key not in self._RESERVED and not key.startswith("_"):
                payload[key] = value
        return json.dumps(payload, default=str)


def configure_logging(*, log_dir: Path, level: int = logging.INFO) -> None:
    log_dir.mkdir(parents=True, exist_ok=True)
    config: dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "request_context": {"()": RequestContextFilter},
            "redact_sensitive": {"()": RedactingFilter},
        },
        "formatters": {
            "json": {"()": JsonFormatter},
            "console": {
                "format": "%(asctime)s %(levelname)-8s [%(request_id)s] %(name)s: %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "console",
                "filters": ["request_context", "redact_sensitive"],
                "level": level,
            },
            "app_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "json",
                "filters": ["request_context", "redact_sensitive"],
                "filename": str(log_dir / "seqproc.jsonl"),
                "maxBytes": 10 * 1024 * 1024,
                "backupCount": 5,
                "level": level,
            },
        },
        "loggers": {
            "seqproc": {"handlers": ["console", "app_file"], "level": level, "propagate": False},
            # Third-party libraries: keep quiet by default, application
            # code should never configure handlers on *their* loggers,
            # only adjust levels.
            "urllib3": {"level": logging.WARNING},
            "boto3": {"level": logging.WARNING},
        },
        "root": {"handlers": ["console"], "level": logging.WARNING},
    }
    logging.config.dictConfig(config)
