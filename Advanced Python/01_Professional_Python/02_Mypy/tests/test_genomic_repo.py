from __future__ import annotations

import sqlite3

import pytest

from genomic_repo import SqlVariantRepository, Variant, Zygosity
from genomic_repo.third_party import normalize_external_call


@pytest.fixture()
def repository() -> SqlVariantRepository:
    connection = sqlite3.connect(":memory:")
    return SqlVariantRepository(connection)


def test_save_and_find_round_trip(repository: SqlVariantRepository) -> None:
    variant = Variant(
        chromosome="chr7",
        position=140453136,
        reference_allele="A",
        alternate_allele="T",
        zygosity=Zygosity.HETEROZYGOUS,
        quality_score=99.5,
    )
    repository.save(variant)
    found = repository.find_by_key(variant.variant_key)
    assert found == variant


def test_find_missing_returns_none(repository: SqlVariantRepository) -> None:
    assert repository.find_by_key("chr1:1:A>T") is None


def test_iter_by_chromosome_orders_by_position(repository: SqlVariantRepository) -> None:
    for position in (300, 100, 200):
        repository.save(
            Variant(
                chromosome="chr1",
                position=position,
                reference_allele="G",
                alternate_allele="C",
                zygosity=Zygosity.HOMOZYGOUS,
            )
        )
    positions = [v.position for v in repository.iter_by_chromosome("chr1")]
    assert positions == [100, 200, 300]


def test_passes_quality_narrows_optional() -> None:
    variant = Variant(
        chromosome="chrX",
        position=1,
        reference_allele="A",
        alternate_allele="G",
        zygosity=Zygosity.HEMIZYGOUS,
        quality_score=30.0,
    )
    assert variant.passes_quality(min_quality=20.0)
    assert not variant.passes_quality(min_quality=40.0)


def test_normalize_external_call_converts_untyped_payload() -> None:
    raw = {"chrom": "chr2", "pos": "500", "ref": "C", "alt": "G", "qual": "40.0"}
    variant = normalize_external_call(raw)
    assert variant.chromosome == "chr2"
    assert variant.quality_score == 40.0


def test_normalize_external_call_rejects_non_mapping() -> None:
    with pytest.raises(TypeError):
        normalize_external_call(["not", "a", "mapping"])
