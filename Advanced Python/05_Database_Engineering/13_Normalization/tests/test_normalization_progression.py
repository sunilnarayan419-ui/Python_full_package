from __future__ import annotations

from pathlib import Path

SQL_DIR = Path(__file__).resolve().parents[1] / "sql"


def test_poor_schema_repeats_researcher_and_target_columns() -> None:
    content = (SQL_DIR / "01_poor_schema.sql").read_text()
    assert "researcher_name" in content
    assert "target_gene_symbol" in content


def test_normalized_schema_extracts_researcher_and_target_entities() -> None:
    content = (SQL_DIR / "02_normalized_schema.sql").read_text()
    assert "CREATE TABLE researchers" in content
    assert "CREATE TABLE molecular_targets" in content
    assert "REFERENCES molecular_targets(target_id)" in content
    assert "REFERENCES researchers(researcher_id)" in content


def test_normalized_results_table_has_no_researcher_or_target_columns() -> None:
    content = (SQL_DIR / "02_normalized_schema.sql").read_text()
    results_table = content.split("CREATE TABLE screening_results (")[1]
    assert "researcher_name" not in results_table
    assert "gene_symbol" not in results_table


def test_denormalized_summary_table_is_rebuildable_from_normalized_data() -> None:
    content = (SQL_DIR / "03_controlled_denormalization.sql").read_text()
    assert "TRUNCATE target_hit_rate_summary" in content
    assert "REFERENCES molecular_targets(target_id)" in content
