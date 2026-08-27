"""Single source of truth for the package version, kept independent of
`pyproject.toml` so it can be introspected at runtime without parsing
build metadata (e.g. for `bioseqkit --version`)."""
from __future__ import annotations

__version__ = "1.2.0"
