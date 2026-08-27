"""Object-model and MRO (method resolution order) inspection applied
to a realistic multiple-inheritance scenario: a service class composed
from a caching mixin and a retrying mixin, where MRO order determines
which mixin's `call` runs first.
"""
from __future__ import annotations

import inspect
from dataclasses import dataclass
from typing import Any, Callable


class CachingMixin:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._cache: dict[Any, Any] = {}
        super().__init__(*args, **kwargs)

    def call(self, key: Any, compute: Callable[[], Any]) -> Any:
        if key in self._cache:
            return self._cache[key]
        value = super().call(key, compute)  # type: ignore[misc]
        self._cache[key] = value
        return value


class RetryingMixin:
    def __init__(self, *args: Any, max_retries: int = 3, **kwargs: Any) -> None:
        self._max_retries = max_retries
        super().__init__(*args, **kwargs)

    def call(self, key: Any, compute: Callable[[], Any]) -> Any:
        last_error: Exception | None = None
        for _ in range(self._max_retries):
            try:
                return compute()
            except RuntimeError as exc:
                last_error = exc
        assert last_error is not None
        raise last_error


class AnnotationLookupService(CachingMixin, RetryingMixin):
    """MRO is [AnnotationLookupService, CachingMixin, RetryingMixin,
    object]: `CachingMixin.call` runs first and only falls through to
    `RetryingMixin.call` (via `super()`) on a cache miss, so retries
    never re-execute for an already-cached key.
    """


@dataclass(frozen=True, slots=True)
class ResolutionStep:
    class_name: str
    module: str


def describe_resolution_order(cls: type) -> tuple[ResolutionStep, ...]:
    return tuple(ResolutionStep(class_name=c.__name__, module=c.__module__) for c in cls.__mro__)


def signature_of(func: Callable[..., Any]) -> inspect.Signature:
    """Wraps `inspect.signature` — used across the codebase to validate
    plugin callables match an expected shape before registration.
    """
    return inspect.signature(func)
