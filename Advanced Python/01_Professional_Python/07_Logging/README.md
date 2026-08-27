# 07_Logging

Production logging setup for a sequence-processing service: JSON
structured logging via `dictConfig`, rotating file handler, a
correlation-ID filter backed by `contextvars`, a redacting filter for
sensitive `extra=` fields, and a clear separation between library-style
logging (`service.py`, no handlers configured) and application-level
sink configuration (`logging_config.py`).

Run: `pytest tests/`
