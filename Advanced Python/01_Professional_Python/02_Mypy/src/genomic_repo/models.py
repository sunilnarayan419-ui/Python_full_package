"""Strictly typed domain models for a variant-calling repository.

Designed to pass `mypy --strict`: no implicit Any, complete annotations,
narrowed Optional handling, and overloaded constructors.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import overload


class Zygosity(str, Enum):
    HOMOZYGOUS = "homozygous"
    HETEROZYGOUS = "heterozygous"
    HEMIZYGOUS = "hemizygous"


@dataclass(frozen=True, slots=True)
class Variant:
    chromosome: str
    position: int
    reference_allele: str
    alternate_allele: str
    zygosity: Zygosity
    quality_score: float | None = None

    @property
    def variant_key(self) -> str:
        return f"{self.chromosome}:{self.position}:{self.reference_allele}>{self.alternate_allele}"

    def passes_quality(self, *, min_quality: float) -> bool:
        """Type-narrowing example: mypy proves `quality_score` is `float`
        (not `float | None`) inside the truthy branch below.
        """
        if self.quality_score is None:
            return False
        return self.quality_score >= min_quality


class VariantBuilder:
    """Demonstrates `@overload` for a constructor-like factory whose
    return type depends on the shape of the input.
    """

    @overload
    @staticmethod
    def from_vcf_fields(fields: tuple[str, str, str, str]) -> Variant: ...

    @overload
    @staticmethod
    def from_vcf_fields(
        fields: tuple[str, str, str, str, float]
    ) -> Variant: ...

    @staticmethod
    def from_vcf_fields(
        fields: tuple[str, str, str, str] | tuple[str, str, str, str, float],
    ) -> Variant:
        chrom, pos, ref, alt = fields[0], fields[1], fields[2], fields[3]
        quality = fields[4] if len(fields) == 5 else None
        return Variant(
            chromosome=chrom,
            position=int(pos),
            reference_allele=ref,
            alternate_allele=alt,
            zygosity=Zygosity.HETEROZYGOUS,
            quality_score=quality,
        )
