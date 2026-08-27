"""Release gate that a pre-commit `pre-push` stage (or CI) can invoke to
verify a scientific-pipeline release is safe to publish.

Kept deliberately small and dependency-free so pre-commit hooks that
import it (e.g. a local `python -m release_gate.checks` hook) stay fast.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

CheckFunc = Callable[[], tuple[bool, str]]


@dataclass(frozen=True, slots=True)
class GateResult:
    passed: bool
    failures: tuple[str, ...] = field(default_factory=tuple)


class ReleaseGate:
    """Runs a registered set of pre-release checks and aggregates results."""

    def __init__(self) -> None:
        self._checks: dict[str, CheckFunc] = {}

    def register(self, name: str, check: CheckFunc) -> None:
        if name in self._checks:
            raise ValueError(f"check {name!r} already registered")
        self._checks[name] = check

    def run(self) -> GateResult:
        failures: list[str] = []
        for name, check in self._checks.items():
            ok, message = check()
            if not ok:
                failures.append(f"{name}: {message}")
        return GateResult(passed=not failures, failures=tuple(failures))
