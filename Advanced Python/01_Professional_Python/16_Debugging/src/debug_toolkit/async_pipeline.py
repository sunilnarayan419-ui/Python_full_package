"""Debugging asynchronous code: demonstrates capturing exceptions from
concurrently running tasks (which `pdb` alone cannot step through
naturally) with full per-task context via `asyncio.gather`'s
`return_exceptions=True`, avoiding losing sibling-task failures when
one task raises first.
"""
from __future__ import annotations

import asyncio
from dataclasses import dataclass

from .diagnostics import FailureContext, capture_failure_context


@dataclass(frozen=True, slots=True)
class TaskOutcome:
    task_id: str
    value: float | None
    failure: FailureContext | None


async def _process_sample(task_id: str, delay: float, dosage: float) -> float:
    await asyncio.sleep(delay)
    if dosage < 0:
        raise ValueError(f"dosage must be non-negative, got {dosage}")
    return dosage * 1.0


async def run_async_pipeline(samples: list[tuple[str, float, float]]) -> list[TaskOutcome]:
    tasks = [_process_sample(task_id, delay, dosage) for task_id, delay, dosage in samples]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    outcomes: list[TaskOutcome] = []
    for (task_id, _, _), result in zip(samples, results):
        if isinstance(result, BaseException):
            outcomes.append(
                TaskOutcome(task_id=task_id, value=None, failure=capture_failure_context(result))
            )
        else:
            outcomes.append(TaskOutcome(task_id=task_id, value=result, failure=None))
    return outcomes
