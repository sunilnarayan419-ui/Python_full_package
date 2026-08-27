"""Reusable diagnostics for reproducing and inspecting production
failures: structured exception context capture and an opt-in
breakpoint hook driven by an environment variable, so debugging can be
enabled in a specific run without editing code.
"""
from __future__ import annotations

import os
import sys
import traceback
from dataclasses import dataclass, field
from types import TracebackType


@dataclass(frozen=True, slots=True)
class FailureContext:
    exception_type: str
    message: str
    stack_summary: tuple[str, ...]
    local_snapshot: dict[str, str] = field(default_factory=dict)


def capture_failure_context(exc: BaseException, *, snapshot_locals: bool = True) -> FailureContext:
    """Builds a structured, loggable snapshot of an exception, including
    a best-effort repr of local variables in the innermost frame —
    invaluable when a failure is reported only via aggregated logs and
    cannot be reproduced interactively with `pdb`.
    """
    tb: TracebackType | None = exc.__traceback__
    stack_summary = tuple(traceback.format_exception(type(exc), exc, tb))
    locals_snapshot: dict[str, str] = {}
    if snapshot_locals and tb is not None:
        innermost = tb
        while innermost.tb_next is not None:
            innermost = innermost.tb_next
        for name, value in innermost.tb_frame.f_locals.items():
            try:
                locals_snapshot[name] = repr(value)
            except Exception:  # noqa: BLE001 - repr() itself must never crash diagnostics
                locals_snapshot[name] = "<unrepresentable>"
    return FailureContext(
        exception_type=type(exc).__name__,
        message=str(exc),
        stack_summary=stack_summary,
        local_snapshot=locals_snapshot,
    )


def debug_breakpoint_if_enabled(*, env_var: str = "PIPELINE_DEBUG") -> None:
    """Drops into `pdb` only when explicitly enabled via environment
    variable, so this can safely live in production code paths without
    ever pausing an unattended process by accident.
    """
    if os.environ.get(env_var) == "1":
        breakpoint()  # noqa: T100 - intentional, gated debugging aid


def assert_invariant(condition: bool, message: str) -> None:
    """Explicit, always-on invariant check (unlike bare `assert`, not
    stripped by `python -O`) for conditions that indicate a genuine
    programming error if violated, distinct from expected user-input
    validation failures which should raise domain exceptions instead.
    """
    if not condition:
        print(f"INVARIANT VIOLATED: {message}", file=sys.stderr)
        raise AssertionError(message)
