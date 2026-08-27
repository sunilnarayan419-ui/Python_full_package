"""Reference-counting behavior made concrete via `sys.getrefcount`,
applied to a real question: does passing a large read-only lookup
table into many worker closures increase its refcount (and therefore
signal shared, safely-read-only ownership) as expected, with no
accidental extra copies.
"""
from __future__ import annotations

import sys


def refcount_of(obj: object) -> int:
    """`sys.getrefcount` itself creates one temporary reference via its
    own argument-passing, so the true 'external' refcount is one less
    than the raw return value; callers should treat this function's
    return value as already adjusted for that.
    """
    return sys.getrefcount(obj) - 1


def build_shared_lookup_closures(lookup_table: dict[str, float], keys: list[str]):
    """Returns closures that each reference the *same* `lookup_table`
    object (via CPython's reference-counted object model) rather than
    copying it — verified by callers using `refcount_of` to confirm no
    accidental duplication occurred during closure construction.
    """
    closures = []
    for key in keys:
        def lookup(k: str = key) -> float:
            return lookup_table[k]
        closures.append(lookup)
    return closures
