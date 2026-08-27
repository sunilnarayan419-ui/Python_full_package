from __future__ import annotations

import pytest

from model_registry.registry import (
    AnalysisModel,
    ModelRegistrationError,
    ModelRegistry,
)


def test_concrete_subclass_is_auto_registered() -> None:
    class GcContentModel(AnalysisModel):
        model_id = "gc_content_v1"

        def score(self, sequence: str) -> float:
            return (sequence.count("G") + sequence.count("C")) / len(sequence)

    retrieved = ModelRegistry.get("gc_content_v1")
    assert retrieved is GcContentModel
    assert "gc_content_v1" in ModelRegistry.available()


def test_missing_model_id_raises_at_definition_time() -> None:
    with pytest.raises(ModelRegistrationError):

        class BrokenModel(AnalysisModel):
            def score(self, sequence: str) -> float:
                return 0.0


def test_duplicate_model_id_is_rejected() -> None:
    class FirstModel(AnalysisModel):
        model_id = "duplicate_id_test"

        def score(self, sequence: str) -> float:
            return 1.0

    with pytest.raises(ModelRegistrationError):

        class SecondModel(AnalysisModel):
            model_id = "duplicate_id_test"

            def score(self, sequence: str) -> float:
                return 2.0


def test_abstract_subclass_without_model_id_is_not_registered() -> None:
    class IntermediateAbstract(AnalysisModel):
        """Still abstract: does not implement `score`, so no `model_id`
        is required and it must not be registered.
        """

    assert "IntermediateAbstract" not in ModelRegistry.available()
