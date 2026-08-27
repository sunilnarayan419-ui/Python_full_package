from __future__ import annotations

import pytest

from internals_lab.mro_inspection import AnnotationLookupService, describe_resolution_order
from internals_lab.plugin_loader import PluginLoadError, load_plugin_class
from internals_lab.rate_limiter import inspect_closure_state, make_rate_limiter


def test_rate_limiter_allows_up_to_burst_then_denies() -> None:
    limiter = make_rate_limiter(max_tokens=2, refill_per_second=0.0)
    assert limiter() is True
    assert limiter() is True
    assert limiter() is False


def test_closure_inspection_exposes_captured_state() -> None:
    limiter = make_rate_limiter(max_tokens=5, refill_per_second=1.0)
    state = inspect_closure_state(limiter)
    assert state["tokens"] == 5.0


def test_mro_places_caching_before_retrying() -> None:
    steps = describe_resolution_order(AnnotationLookupService)
    names = [s.class_name for s in steps]
    assert names.index("CachingMixin") < names.index("RetryingMixin")


def test_caching_mixin_prevents_recomputation_on_hit() -> None:
    service = AnnotationLookupService(max_retries=2)
    calls = 0

    def compute() -> str:
        nonlocal calls
        calls += 1
        return "annotation-result"

    first = service.call("gene:BRCA1", compute)
    second = service.call("gene:BRCA1", compute)
    assert first == second == "annotation-result"
    assert calls == 1


def test_retrying_mixin_retries_transient_failures() -> None:
    service = AnnotationLookupService(max_retries=3)
    attempts = 0

    def flaky() -> str:
        nonlocal attempts
        attempts += 1
        if attempts < 2:
            raise RuntimeError("transient")
        return "ok"

    assert service.call("gene:TP53", flaky) == "ok"
    assert attempts == 2


def test_load_plugin_class_resolves_dotted_path() -> None:
    plugin_class = load_plugin_class("internals_lab.mro_inspection:AnnotationLookupService")
    assert plugin_class is AnnotationLookupService


def test_load_plugin_class_rejects_malformed_path() -> None:
    with pytest.raises(PluginLoadError):
        load_plugin_class("no_colon_in_this_string")


def test_load_plugin_class_reports_missing_attribute() -> None:
    with pytest.raises(PluginLoadError):
        load_plugin_class("internals_lab.mro_inspection:DoesNotExist")
