"""
04_Coroutines.py

Industry-standard demonstration of coroutine-based architecture: a
scientific data pipeline built by composing coroutines/async
generators rather than by fanning out with asyncio.gather().

Pipeline shape
--------------
    raw sample source
        -> validator      (drops malformed samples)
        -> transformer     (normalizes measurement units)
        -> aggregator      (folds the stream into summary statistics)

Coroutine vs thread vs process
-------------------------------
- A COROUTINE is a single function's suspended execution state. It
  runs on whichever thread drives it (here, the event loop thread) and
  only yields control at explicit `await` points. There is exactly one
  call stack in flight per driving thread at a time -- cooperative,
  not preemptive.
- A THREAD is an OS-scheduled unit that can be preempted at any
  bytecode boundary by the interpreter/OS. Under CPython's GIL, only
  one thread executes Python bytecode at a time, but the OS can switch
  between threads without their consent (see 01_Threading.py).
- A PROCESS has its own memory space and its own GIL/interpreter, and
  can run Python bytecode in true CPU parallel with other processes
  (see 02_Multiprocessing.py).

This file uses ONLY coroutines: no threads, no processes. Each stage
is an async generator that pulls one item at a time from the stage
before it, does a small amount of async work, and yields downstream.
Execution is cooperative and single-flow -- a deliberate contrast to
gather-based fan-out, which is covered in 03_Asyncio.py.
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import AsyncIterator
from dataclasses import dataclass

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")


@dataclass(frozen=True, slots=True)
class RawSample:
    sample_id: str
    raw_value: float | None
    unit: str


@dataclass(frozen=True, slots=True)
class ValidatedSample:
    sample_id: str
    value: float
    unit: str


@dataclass(frozen=True, slots=True)
class TransformedSample:
    sample_id: str
    value_micromolar: float


@dataclass(frozen=True, slots=True)
class AggregateResult:
    sample_count: int
    mean_micromolar: float
    max_micromolar: float


_UNIT_TO_MICROMOLAR: dict[str, float] = {
    "uM": 1.0,
    "mM": 1_000.0,
    "nM": 0.001,
}


async def sample_source() -> AsyncIterator[RawSample]:
    """
    The pipeline's origin coroutine (an async generator). Each yield
    stands in for reading the next record from an async source such as
    a streaming file reader or a paginated API -- represented here by
    an awaited micro-delay so it cooperates with the event loop.
    """
    raw_records = [
        RawSample("S-001", 12.4, "uM"),
        RawSample("S-002", None, "uM"),  # malformed: missing measurement
        RawSample("S-003", 0.0087, "mM"),
        RawSample("S-004", 340.0, "nM"),
        RawSample("S-005", -2.1, "uM"),  # malformed: physically invalid
        RawSample("S-006", 5.6, "unknown-unit"),  # malformed: unrecognized unit
        RawSample("S-007", 9.9, "uM"),
    ]
    for record in raw_records:
        await asyncio.sleep(0)  # cooperative yield point; simulates async source I/O
        yield record


async def validator(upstream: AsyncIterator[RawSample]) -> AsyncIterator[ValidatedSample]:
    """Consumes the upstream async generator one item at a time and drops invalid samples."""
    async for raw in upstream:
        if raw.raw_value is None:
            logger.warning("sample=%s dropped: missing value", raw.sample_id)
            continue
        if raw.raw_value < 0:
            logger.warning("sample=%s dropped: negative concentration", raw.sample_id)
            continue
        if raw.unit not in _UNIT_TO_MICROMOLAR:
            logger.warning("sample=%s dropped: unrecognized unit '%s'", raw.sample_id, raw.unit)
            continue
        yield ValidatedSample(raw.sample_id, raw.raw_value, raw.unit)


async def transformer(upstream: AsyncIterator[ValidatedSample]) -> AsyncIterator[TransformedSample]:
    """Normalizes every validated sample to a common unit (micromolar)."""
    async for sample in upstream:
        factor = _UNIT_TO_MICROMOLAR[sample.unit]
        normalized = sample.value * factor
        yield TransformedSample(sample.sample_id, normalized)


async def aggregator(upstream: AsyncIterator[TransformedSample]) -> AggregateResult:
    """
    A plain coroutine (not a generator) that fully drains the upstream
    stream and folds it into a summary. This is the pipeline's sink.
    """
    count = 0
    total = 0.0
    peak = float("-inf")
    async for sample in upstream:
        count += 1
        total += sample.value_micromolar
        peak = max(peak, sample.value_micromolar)
        logger.info("sample=%s normalized=%.4f uM", sample.sample_id, sample.value_micromolar)

    if count == 0:
        return AggregateResult(sample_count=0, mean_micromolar=0.0, max_micromolar=0.0)
    return AggregateResult(sample_count=count, mean_micromolar=total / count, max_micromolar=peak)


async def run_pipeline() -> AggregateResult:
    """
    Coroutine composition: each stage wraps the previous stage's async
    generator. Nothing runs until `aggregator` starts pulling -- the
    whole pipeline is pull-driven and lazy, one sample flowing through
    all three stages before the next sample is even read from the
    source. This is the essence of coroutine cooperation: control
    passes explicitly from stage to stage at each `await`/`yield`,
    never preemptively.
    """
    pipeline = aggregator(transformer(validator(sample_source())))
    return await pipeline


async def async_main() -> None:
    result = await run_pipeline()
    logger.info(
        "aggregate: %d valid samples, mean=%.4f uM, max=%.4f uM",
        result.sample_count,
        result.mean_micromolar,
        result.max_micromolar,
    )


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
