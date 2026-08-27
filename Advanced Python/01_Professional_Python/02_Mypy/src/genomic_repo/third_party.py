"""Demonstrates isolating an untyped/partially-typed third-party boundary
so `Any` does not leak into the rest of a strictly typed codebase.

In `mypy.ini`, `third_party_variant_caller.*` is configured with
`ignore_missing_imports = True`; this module is the single, narrow
seam where that untyped surface is converted into our typed `Variant`.
"""
from __future__ import annotations

from typing import Any, cast

from .models import Variant, Zygosity


def normalize_external_call(raw_result: object) -> Variant:
    """Convert an opaque, loosely typed external caller result into a
    validated `Variant`, isolating `Any`/`cast` usage to this boundary.
    """
    if not isinstance(raw_result, dict):
        raise TypeError(f"expected mapping from external caller, got {type(raw_result)!r}")

    data = cast(dict[str, Any], raw_result)
    try:
        return Variant(
            chromosome=str(data["chrom"]),
            position=int(data["pos"]),
            reference_allele=str(data["ref"]),
            alternate_allele=str(data["alt"]),
            zygosity=Zygosity(str(data.get("zygosity", "heterozygous"))),
            quality_score=(
                float(data["qual"]) if data.get("qual") is not None else None
            ),
        )
    except KeyError as exc:
        raise ValueError(f"external caller result missing required field: {exc}") from exc
