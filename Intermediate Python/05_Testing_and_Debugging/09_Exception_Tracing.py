"""Production-grade exception diagnostics for an experiment processing
pipeline: custom exceptions, chaining, and controlled error reporting.
"""

from __future__ import annotations

import logging
import traceback
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class InvalidSampleError(ValueError):
    """Expected domain validation failure: the sample data itself is bad."""


class ExperimentProcessingError(RuntimeError):
    """Unexpected failure while processing an otherwise valid sample."""


class InfrastructureError(RuntimeError):
    """Failure originating from an external system (storage, network, etc.)."""


@dataclass(frozen=True, slots=True)
class Sample:
    sample_id: str
    raw_reading: str  # intentionally a string: may contain malformed data


def parse_reading(sample: Sample) -> float:
    """Parses a raw instrument reading, raising a domain-specific error
    with the original cause preserved for diagnostics.
    """
    try:
        return float(sample.raw_reading)
    except ValueError as exc:
        # Domain validation failure: the input itself is invalid. The
        # original ValueError is preserved via `from exc` so the full
        # chain remains inspectable, without leaking raw instrument
        # payloads beyond what is needed to identify the sample.
        raise InvalidSampleError(
            f"sample {sample.sample_id} has a non-numeric reading"
        ) from exc


def analyze_reading(sample: Sample, reading: float) -> float:
    """Performs analysis that may fail for reasons unrelated to input
    validity (e.g. an internal precondition is violated).
    """
    try:
        if reading == 0:
            # Deliberate internal invariant violation, not a user input
            # problem -- classified as a processing error rather than a
            # validation error.
            raise ZeroDivisionError("normalization factor collapsed to zero")
        return 100.0 / reading
    except ZeroDivisionError as exc:
        raise ExperimentProcessingError(
            f"analysis failed for sample {sample.sample_id}: unstable normalization"
        ) from exc


def persist_result(sample: Sample, value: float) -> None:
    """Simulates a storage boundary that can fail independently of the
    scientific logic above it.
    """
    if sample.sample_id.startswith("OFFLINE-"):
        raise InfrastructureError(
            f"storage backend unreachable while persisting sample {sample.sample_id}"
        )


def process_sample(sample: Sample) -> float:
    """Top-level orchestration distinguishing the three failure classes:
    domain validation, internal processing, and infrastructure.
    """
    reading = parse_reading(sample)
    analyzed = analyze_reading(sample, reading)
    persist_result(sample, analyzed)
    return analyzed


def process_sample_with_diagnostics(sample: Sample) -> float | None:
    """Controlled error reporting: logs full diagnostics for unexpected
    failures while re-raising expected domain errors for the caller to
    handle explicitly.
    """
    try:
        return process_sample(sample)
    except InvalidSampleError:
        # Expected, caller-actionable: do not log as an error-level
        # incident, just propagate for upstream handling.
        raise
    except (ExperimentProcessingError, InfrastructureError):
        # Unexpected but classified failure: capture full traceback for
        # diagnostics without exposing internals to the caller.
        logger.exception("Processing failed for sample %s", sample.sample_id)
        raise
    except Exception:
        # Truly unanticipated: still logged with full context, then
        # re-raised rather than swallowed.
        logger.exception(
            "Unclassified failure while processing sample %s", sample.sample_id
        )
        raise


def _inspect_exception_chain(exc: BaseException) -> list[str]:
    """Walks the __cause__ chain, useful for structured error reporting
    or tests asserting that root causes were preserved.
    """
    messages = []
    current: BaseException | None = exc
    while current is not None:
        messages.append(f"{type(current).__name__}: {current}")
        current = current.__cause__
    return messages


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    samples = [
        Sample(sample_id="S-500", raw_reading="12.5"),
        Sample(sample_id="S-501", raw_reading="not-a-number"),
        Sample(sample_id="S-502", raw_reading="0"),
        Sample(sample_id="OFFLINE-503", raw_reading="8.0"),
    ]

    for sample in samples:
        try:
            result = process_sample_with_diagnostics(sample)
            print(f"{sample.sample_id}: result={result:.3f}")
        except InvalidSampleError as exc:
            print(f"{sample.sample_id}: rejected -> {exc}")
        except (ExperimentProcessingError, InfrastructureError) as exc:
            chain = _inspect_exception_chain(exc)
            print(f"{sample.sample_id}: failed -> chain={chain}")
            # traceback.format_exc() is only meaningful inside an active
            # except block, where sys.exc_info() is populated.
            _ = traceback.format_exc()
