"""Scoring services demonstrating Callable typing, ParamSpec, and Protocols
for pluggable, type-safe business-logic strategies.
"""
from __future__ import annotations

from typing import Callable, ParamSpec, Protocol, TypeVar

from .models import CompoundRecord

P = ParamSpec("P")
R = TypeVar("R")


def log_calls(func: Callable[P, R]) -> Callable[P, R]:
    """Type-preserving decorator using ParamSpec to keep the wrapped
    callable's signature intact for static analysis and IDE tooling.
    """

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        result = func(*args, **kwargs)
        return result

    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper


class ScoringStrategy(Protocol):
    """Pluggable scoring contract: lower score is better (drug-like)."""

    def __call__(self, compound: CompoundRecord) -> float: ...  # noqa: E704


def potency_score(compound: CompoundRecord) -> float:
    """Score dominated by best (lowest) measured IC50 in nanomolar."""
    best = compound.best_potency()
    if best is None:
        return float("inf")
    return best.ic50_nm


def lipinski_penalty_score(compound: CompoundRecord) -> float:
    """Penalize compounds violating a simplified Lipinski MW cutoff."""
    penalty = 0.0
    if compound.molecular_weight > 500:
        penalty += (compound.molecular_weight - 500) * 2
    best = compound.best_potency()
    base = best.ic50_nm if best is not None else float("inf")
    return base + penalty


class ScoringService:
    """Ranks compounds using an injected, type-checked scoring strategy."""

    def __init__(self, strategy: ScoringStrategy) -> None:
        self._strategy = strategy

    @log_calls
    def rank(self, compounds: list[CompoundRecord]) -> list[CompoundRecord]:
        return sorted(compounds, key=self._strategy)

    def score_of(self, compound: CompoundRecord) -> float:
        return self._strategy(compound)
