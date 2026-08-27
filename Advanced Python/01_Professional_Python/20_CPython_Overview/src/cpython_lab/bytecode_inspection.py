"""Practical bytecode-level inspection used to justify a real
optimization decision: choosing a set-membership check over repeated
`in` checks against a list, verified via `dis` rather than assumed.
"""
from __future__ import annotations

import dis
import io
from typing import Callable


def disassemble_hot_path(func: Callable[..., object]) -> str:
    """Captures `dis.dis` output as a string for inclusion in code
    review / perf-investigation notes, rather than only printing to
    stdout — used in this codebase's profiling reports.
    """
    buffer = io.StringIO()
    dis.dis(func, file=buffer)
    return buffer.getvalue()


def contains_via_list(item: str, collection: list[str]) -> bool:
    return item in collection


def contains_via_set(item: str, collection: frozenset[str]) -> bool:
    return item in collection


def count_load_fast_ops(func: Callable[..., object]) -> int:
    """Counts LOAD_FAST bytecode instructions — a concrete, measurable
    proxy for local-variable access pressure in a hot function, used
    when deciding whether to hoist repeated attribute lookups into
    locals before a tight loop.
    """
    return sum(1 for instr in dis.get_instructions(func) if instr.opname == "LOAD_FAST")
