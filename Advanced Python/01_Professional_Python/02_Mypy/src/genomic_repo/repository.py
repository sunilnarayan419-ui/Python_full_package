"""Generic, protocol-based repository designed for strict mypy checking.

Shows how to type a SQL-backed implementation against an abstract
interface without leaking connection internals as `Any`.
"""
from __future__ import annotations

import sqlite3
from typing import Iterator, Protocol

from .models import Variant, Zygosity


class VariantRepository(Protocol):
    def find_by_key(self, variant_key: str) -> Variant | None: ...  # noqa: E704
    def save(self, variant: Variant) -> None: ...  # noqa: E704
    def iter_by_chromosome(self, chromosome: str) -> Iterator[Variant]: ...  # noqa: E704


class SqlVariantRepository:
    """SQLite-backed implementation satisfying `VariantRepository` structurally."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._conn = connection
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS variants (
                variant_key TEXT PRIMARY KEY,
                chromosome TEXT NOT NULL,
                position INTEGER NOT NULL,
                reference_allele TEXT NOT NULL,
                alternate_allele TEXT NOT NULL,
                zygosity TEXT NOT NULL,
                quality_score REAL
            )
            """
        )
        self._conn.commit()

    def find_by_key(self, variant_key: str) -> Variant | None:
        row = self._conn.execute(
            "SELECT chromosome, position, reference_allele, alternate_allele, "
            "zygosity, quality_score FROM variants WHERE variant_key = ?",
            (variant_key,),
        ).fetchone()
        if row is None:
            return None
        chromosome, position, ref, alt, zygosity, quality = row
        return Variant(
            chromosome=chromosome,
            position=position,
            reference_allele=ref,
            alternate_allele=alt,
            zygosity=Zygosity(zygosity),
            quality_score=quality,
        )

    def save(self, variant: Variant) -> None:
        self._conn.execute(
            "INSERT OR REPLACE INTO variants VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                variant.variant_key,
                variant.chromosome,
                variant.position,
                variant.reference_allele,
                variant.alternate_allele,
                variant.zygosity.value,
                variant.quality_score,
            ),
        )
        self._conn.commit()

    def iter_by_chromosome(self, chromosome: str) -> Iterator[Variant]:
        cursor = self._conn.execute(
            "SELECT chromosome, position, reference_allele, alternate_allele, "
            "zygosity, quality_score FROM variants WHERE chromosome = ? "
            "ORDER BY position",
            (chromosome,),
        )
        for chrom, position, ref, alt, zygosity, quality in cursor:
            yield Variant(
                chromosome=chrom,
                position=position,
                reference_allele=ref,
                alternate_allele=alt,
                zygosity=Zygosity(zygosity),
                quality_score=quality,
            )
