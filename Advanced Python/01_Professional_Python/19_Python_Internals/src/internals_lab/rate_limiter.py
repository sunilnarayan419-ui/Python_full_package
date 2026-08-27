"""Closures and function-object internals applied to a real production
primitive: a token-bucket rate limiter for outbound calls to an
external variant-annotation API.

Demonstrates: closures capturing mutable state via `nonlocal`,
inspecting a closure's captured cells through `__closure__` and
`__code__.co_freevars` for diagnostics/testing, and why closures (not
classes) are sometimes the leaner choice for small stateful callables.
"""
from __future__ import annotations

import time
from typing import Callable


def make_rate_limiter(*, max_tokens: int, refill_per_second: float) -> Callable[[], bool]:
    tokens = float(max_tokens)
    last_refill = time.monotonic()

    def try_acquire() -> bool:
        nonlocal tokens, last_refill
        now = time.monotonic()
        elapsed = now - last_refill
        tokens = min(max_tokens, tokens + elapsed * refill_per_second)
        last_refill = now
        if tokens >= 1.0:
            tokens -= 1.0
            return True
        return False

    return try_acquire


def inspect_closure_state(func: Callable[..., object]) -> dict[str, object]:
    """Introspects a closure's free variables and their current captured
    values via `__code__.co_freevars` and `__closure__` — useful for
    unit-testing rate-limiter internals without exposing a public API
    surface just for test observability.
    """
    code = func.__code__
    closure = func.__closure__
    if closure is None:
        return {}
    return {
        name: cell.cell_contents
        for name, cell in zip(code.co_freevars, closure)
    }
