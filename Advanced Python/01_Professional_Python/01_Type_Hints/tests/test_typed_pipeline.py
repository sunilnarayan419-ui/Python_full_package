from __future__ import annotations

import pytest

from typed_pipeline import (
    AssayResult,
    CompoundRecord,
    InMemoryRepository,
    ScoringService,
)
from typed_pipeline.services import lipinski_penalty_score, potency_score


def make_compound(compound_id: str, ic50_nm: float, mw: float = 350.0) -> CompoundRecord:
    result = AssayResult(target_id="EGFR", ic50_nm=ic50_nm)
    return CompoundRecord(
        compound_id=compound_id, smiles="CCO", molecular_weight=mw
    ).with_assay_result(result)


def test_assay_result_rejects_non_positive_potency() -> None:
    with pytest.raises(ValueError):
        AssayResult(target_id="EGFR", ic50_nm=0.0)


def test_compound_record_is_immutable_on_status_update() -> None:
    original = make_compound("CMP-001", ic50_nm=25.0)
    updated = original.with_status("running")
    assert original.status == "pending"
    assert updated.status == "running"
    assert original is not updated


def test_best_potency_selects_lowest_ic50() -> None:
    compound = make_compound("CMP-002", ic50_nm=50.0)
    compound = compound.with_assay_result(AssayResult(target_id="EGFR", ic50_nm=10.0))
    best = compound.best_potency()
    assert best is not None
    assert best.ic50_nm == 10.0


def test_scoring_service_ranks_by_potency() -> None:
    compounds = [
        make_compound("CMP-A", ic50_nm=100.0),
        make_compound("CMP-B", ic50_nm=5.0),
        make_compound("CMP-C", ic50_nm=50.0),
    ]
    service = ScoringService(strategy=potency_score)
    ranked = service.rank(compounds)
    assert [c.compound_id for c in ranked] == ["CMP-B", "CMP-C", "CMP-A"]


def test_lipinski_penalty_score_penalizes_heavy_compounds() -> None:
    light = make_compound("CMP-LIGHT", ic50_nm=20.0, mw=300.0)
    heavy = make_compound("CMP-HEAVY", ic50_nm=20.0, mw=700.0)
    service = ScoringService(strategy=lipinski_penalty_score)
    assert service.score_of(heavy) > service.score_of(light)


def test_repository_round_trip() -> None:
    repo = InMemoryRepository()
    compound = make_compound("CMP-003", ic50_nm=15.0)
    repo.add(compound)
    assert repo.get("CMP-003") is compound
    assert len(repo) == 1
    assert list(repo.all()) == [compound]
