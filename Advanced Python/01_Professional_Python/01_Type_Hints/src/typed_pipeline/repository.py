"""Generic, type-safe repository interfaces.

Demonstrates Protocol-based structural typing, TypeVar-bound generics,
and a concrete in-memory implementation suitable for tests and small
services alike.
"""
from __future__ import annotations

from typing import Iterable, Iterator, Protocol, TypeVar, runtime_checkable

from .models import CompoundRecord

T = TypeVar("T")
K = TypeVar("K")


@runtime_checkable
class Identifiable(Protocol[K]):
    """Structural contract for any entity addressable by a stable key."""

    @property
    def compound_id(self) -> K: ...  # noqa: E704


class Repository(Protocol[K, T]):
    """Generic repository contract, independent of storage backend."""

    def get(self, key: K) -> T | None: ...  # noqa: E704
    def add(self, entity: T) -> None: ...  # noqa: E704
    def all(self) -> Iterator[T]: ...  # noqa: E704
    def __len__(self) -> int: ...  # noqa: E704


class InMemoryRepository:
    """In-memory repository for CompoundRecord, keyed by compound_id.

    Suitable as a fast test double or for small batch jobs; production
    services typically swap this for a SQL- or document-store-backed
    implementation that satisfies the same Repository protocol.
    """

    def __init__(self, seed: Iterable[CompoundRecord] = ()) -> None:
        self._store: dict[str, CompoundRecord] = {c.compound_id: c for c in seed}

    def get(self, key: str) -> CompoundRecord | None:
        return self._store.get(key)

    def add(self, entity: CompoundRecord) -> None:
        self._store[entity.compound_id] = entity

    def all(self) -> Iterator[CompoundRecord]:
        return iter(self._store.values())

    def __len__(self) -> int:
        return len(self._store)
