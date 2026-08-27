from __future__ import annotations

import json
import logging
from pathlib import Path

from seqproc.logging_config import bind_request_id, configure_logging


def test_json_log_lines_include_request_id(tmp_path: Path) -> None:
    configure_logging(log_dir=tmp_path)
    bind_request_id("req-123")
    logger = logging.getLogger("seqproc.test")
    logger.info("hello world", extra={"sample_id": "S1"})
    for handler in logging.getLogger("seqproc").handlers:
        handler.flush()
    log_file = tmp_path / "seqproc.jsonl"
    lines = [line for line in log_file.read_text().splitlines() if line.strip()]
    assert lines
    record = json.loads(lines[-1])
    assert record["request_id"] == "req-123"
    assert record["sample_id"] == "S1"


def test_redacting_filter_masks_sensitive_extra(tmp_path: Path) -> None:
    configure_logging(log_dir=tmp_path)
    logger = logging.getLogger("seqproc.test.redact")
    logger.info("auth attempt", extra={"api_key": "sk-super-secret"})
    for handler in logging.getLogger("seqproc").handlers:
        handler.flush()
    log_file = tmp_path / "seqproc.jsonl"
    content = log_file.read_text()
    assert "sk-super-secret" not in content
    assert "REDACTED" in content
