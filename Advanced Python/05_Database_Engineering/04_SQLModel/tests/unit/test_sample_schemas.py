from __future__ import annotations

from datetime import datetime

import pytest
from pydantic import ValidationError

from app.schemas.sample_schemas import SampleCreateRequest


def test_sample_create_request_rejects_empty_subject_code() -> None:
    with pytest.raises(ValidationError):
        SampleCreateRequest(subject_code="", collected_at=datetime.utcnow())


def test_sample_create_request_accepts_valid_payload() -> None:
    payload = SampleCreateRequest(subject_code="SUBJ-042", collected_at=datetime(2025, 6, 1))
    assert payload.subject_code == "SUBJ-042"
