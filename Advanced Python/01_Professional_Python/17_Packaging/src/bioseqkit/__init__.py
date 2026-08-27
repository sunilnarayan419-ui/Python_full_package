"""bioseqkit: sequence validation and summarization utilities.

Public API is re-exported here; internal modules (prefixed with `_`)
are not part of the stable interface and may change without a major
version bump.
"""
from __future__ import annotations

from .sequences import SequenceStats, summarize, validate_sequence
from .version import __version__

__all__ = ["SequenceStats", "__version__", "summarize", "validate_sequence"]
