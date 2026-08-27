from __future__ import annotations

import logging

import pytest

from seqproc.service import InvalidSequenceError, SequenceProcessingService


def test_process_computes_gc_content() -> None:
    service = SequenceProcessingService()
    result = service.process("SAMPLE-1", "GGCCAATT")
    assert result.gc_content == 0.5
    assert result.length == 8


def test_process_rejects_invalid_bases() -> None:
    service = SequenceProcessingService()
    with pytest.raises(InvalidSequenceError):
        service.process("SAMPLE-2", "GGXCAT")


def test_process_logs_exception_on_invalid_sequence(caplog: pytest.LogCaptureFixture) -> None:
    service = SequenceProcessingService()
    with caplog.at_level(logging.ERROR, logger="seqproc.service"):
        with pytest.raises(InvalidSequenceError):
            service.process("SAMPLE-3", "")
    assert any(record.levelno == logging.ERROR for record in caplog.records)
