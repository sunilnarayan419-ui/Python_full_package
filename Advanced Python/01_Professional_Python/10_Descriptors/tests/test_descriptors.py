from __future__ import annotations

import pytest

from model_fields import PatientRecord
from model_fields.descriptors import CachedProperty, LazyLoaded


def test_validated_string_accepts_matching_format() -> None:
    record = PatientRecord("MRN-123456", 120.0, 80.0)
    assert record.medical_record_number == "MRN-123456"


def test_validated_string_rejects_bad_format() -> None:
    with pytest.raises(ValueError):
        PatientRecord("bad-id", 120.0, 80.0)


def test_bounded_float_rejects_out_of_range() -> None:
    with pytest.raises(ValueError):
        PatientRecord("MRN-123456", 500.0, 80.0)


def test_cached_property_computes_once() -> None:
    call_count = 0

    class Metric:
        value = 10

        @CachedProperty
        def doubled(self) -> int:
            nonlocal call_count
            call_count += 1
            return self.value * 2

    metric = Metric()
    assert metric.doubled == 20
    assert metric.doubled == 20
    assert call_count == 1


def test_lazy_loaded_respects_ttl() -> None:
    calls: list[int] = []

    class Holder:
        region = LazyLoaded(lambda self: calls.append(1) or len(calls), ttl_seconds=1000.0)

    holder = Holder()
    first = holder.region
    second = holder.region
    assert first == second == 1
    assert len(calls) == 1
