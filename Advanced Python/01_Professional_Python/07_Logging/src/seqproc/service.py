"""Sequence processing service demonstrating library-style logging
practices: module-level `getLogger(__name__)`, no handler configuration
inside library code, structured `extra=` fields, and full exception
logging via `logger.exception`.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class InvalidSequenceError(Exception):
    pass


@dataclass(frozen=True, slots=True)
class ProcessingResult:
    sample_id: str
    gc_content: float
    length: int


_VALID_BASES = frozenset("ACGTN")


class SequenceProcessingService:
    def process(self, sample_id: str, sequence: str) -> ProcessingResult:
        logger.info("processing sequence", extra={"sample_id": sample_id, "length": len(sequence)})
        try:
            self._validate(sequence)
            gc_content = self._gc_content(sequence)
        except InvalidSequenceError:
            logger.exception(
                "sequence validation failed", extra={"sample_id": sample_id}
            )
            raise
        logger.debug(
            "computed gc content", extra={"sample_id": sample_id, "gc_content": gc_content}
        )
        return ProcessingResult(sample_id=sample_id, gc_content=gc_content, length=len(sequence))

    @staticmethod
    def _validate(sequence: str) -> None:
        invalid_chars = set(sequence.upper()) - _VALID_BASES
        if invalid_chars:
            raise InvalidSequenceError(f"invalid bases found: {sorted(invalid_chars)}")
        if not sequence:
            raise InvalidSequenceError("sequence must not be empty")

    @staticmethod
    def _gc_content(sequence: str) -> float:
        upper = sequence.upper()
        gc_count = upper.count("G") + upper.count("C")
        return gc_count / len(upper)
