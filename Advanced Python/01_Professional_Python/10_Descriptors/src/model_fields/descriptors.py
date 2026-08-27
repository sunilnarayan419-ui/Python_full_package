"""Descriptor-based field validation and lazy/cached attributes for
scientific domain models.

Descriptors are justified here because the same validation/caching
behavior (range checks, regex validation, expensive lazy computation)
is reused across many model fields; a plain `@property` per field
would duplicate this logic dozens of times across the codebase.
"""
from __future__ import annotations

import re
import time
from typing import Any, Callable, Generic, TypeVar

T = TypeVar("T")
InstanceT = TypeVar("InstanceT")


class BoundedFloat:
    """Numeric field descriptor enforcing an inclusive [min, max] range,
    used for clinical measurements (e.g. blood pressure, dosage).
    """

    def __init__(self, *, minimum: float, maximum: float) -> None:
        self._minimum = minimum
        self._maximum = maximum
        self._name = ""

    def __set_name__(self, owner: type, name: str) -> None:
        self._name = name

    def __get__(self, instance: object | None, owner: type) -> float:
        if instance is None:
            return self  # type: ignore[return-value]
        value = instance.__dict__.get(self._name)
        if value is None:
            raise AttributeError(f"{self._name!r} has not been set")
        return value

    def __set__(self, instance: object, value: float) -> None:
        if not (self._minimum <= value <= self._maximum):
            raise ValueError(
                f"{self._name} must be within [{self._minimum}, {self._maximum}], got {value}"
            )
        instance.__dict__[self._name] = value


class ValidatedString:
    """String field descriptor enforcing a compiled regex pattern, used
    for identifiers like MRNs (medical record numbers) that must match
    a strict institutional format.
    """

    def __init__(self, *, pattern: str) -> None:
        self._pattern = re.compile(pattern)
        self._name = ""

    def __set_name__(self, owner: type, name: str) -> None:
        self._name = name

    def __get__(self, instance: object | None, owner: type) -> str:
        if instance is None:
            return self  # type: ignore[return-value]
        return instance.__dict__[self._name]

    def __set__(self, instance: object, value: str) -> None:
        if not self._pattern.fullmatch(value):
            raise ValueError(f"{self._name} value {value!r} does not match required format")
        instance.__dict__[self._name] = value


class CachedProperty(Generic[InstanceT, T]):
    """Computes an expensive derived value once per instance and caches
    it in the instance `__dict__`, shadowing the descriptor on
    subsequent lookups (the standard non-data-descriptor caching idiom).
    """

    def __init__(self, func: Callable[[InstanceT], T]) -> None:
        self._func = func
        self._name = func.__name__
        self.__doc__ = func.__doc__

    def __set_name__(self, owner: type, name: str) -> None:
        self._name = name

    def __get__(self, instance: InstanceT | None, owner: type) -> T | "CachedProperty[InstanceT, T]":
        if instance is None:
            return self
        value = self._func(instance)
        instance.__dict__[self._name] = value
        return value


class LazyLoaded(Generic[T]):
    """Data descriptor that defers an expensive load (e.g. fetching a
    large reference genome region from disk/network) until first
    access, then caches it with a TTL for staleness control.
    """

    def __init__(self, loader: Callable[[Any], T], *, ttl_seconds: float = 300.0) -> None:
        self._loader = loader
        self._ttl_seconds = ttl_seconds
        self._cache_attr = f"_lazy_{id(self)}"

    def __set_name__(self, owner: type, name: str) -> None:
        self._cache_attr = f"_lazy_{name}"

    def __get__(self, instance: object | None, owner: type) -> T:
        if instance is None:
            return self  # type: ignore[return-value]
        cached = instance.__dict__.get(self._cache_attr)
        now = time.monotonic()
        if cached is not None:
            value, expires_at = cached
            if now < expires_at:
                return value
        value = self._loader(instance)
        instance.__dict__[self._cache_attr] = (value, now + self._ttl_seconds)
        return value

    def __set__(self, instance: object, value: T) -> None:
        instance.__dict__[self._cache_attr] = (value, time.monotonic() + self._ttl_seconds)
