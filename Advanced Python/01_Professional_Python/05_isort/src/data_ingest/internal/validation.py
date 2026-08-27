"""Internal validation helpers, imported only within `data_ingest`."""
from __future__ import annotations

import re

_SAMPLE_ID_PATTERN = re.compile(r"^S\d{3,}$")


def validate_sample_ids(sample_ids: tuple[str, ...]) -> None:
    invalid = [sid for sid in sample_ids if not _SAMPLE_ID_PATTERN.match(sid)]
    if invalid:
        raise ValueError(f"invalid sample identifiers: {invalid}")
