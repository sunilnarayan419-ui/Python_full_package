from __future__ import annotations

from pathlib import Path

import pytest

from data_ingest import IngestPipeline
from data_ingest.internal.validation import validate_sample_ids


def test_validate_sample_ids_accepts_well_formed_ids() -> None:
    validate_sample_ids(("S001", "S002", "S1234"))


def test_validate_sample_ids_rejects_malformed_ids() -> None:
    with pytest.raises(ValueError):
        validate_sample_ids(("S001", "bad_id"))


def test_pipeline_rejects_matrix_with_missing_values(tmp_path: Path) -> None:
    csv_path = tmp_path / "matrix.csv"
    csv_path.write_text("gene,S001,S002\nGENE1,1.0,\nGENE2,2.0,3.0\n")
    pipeline = IngestPipeline(csv_path)
    with pytest.raises(ValueError):
        pipeline.run()


def test_pipeline_loads_valid_matrix(tmp_path: Path) -> None:
    csv_path = tmp_path / "matrix.csv"
    csv_path.write_text("gene,S001,S002\nGENE1,1.0,2.0\nGENE2,3.0,4.0\n")
    pipeline = IngestPipeline(csv_path)
    matrix = pipeline.run()
    assert matrix.gene_ids == ("GENE1", "GENE2")
    assert matrix.values.shape == (2, 2)
