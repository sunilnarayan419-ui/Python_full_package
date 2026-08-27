from __future__ import annotations

from pathlib import Path

SCHEMA = (Path(__file__).resolve().parents[1] / "sql" / "full_schema.sql").read_text()


def test_every_project_scoped_table_has_a_project_id_index_or_fk() -> None:
    for table in ("experiments", "compounds", "screening_runs"):
        assert f"idx_{table}" in SCHEMA or "project_id" in SCHEMA


def test_multi_tenant_boundary_column_exists() -> None:
    assert "organization_id" in SCHEMA
    assert "REFERENCES organizations(organization_id)" in SCHEMA


def test_soft_delete_column_present_on_projects() -> None:
    assert "deleted_at" in SCHEMA


def test_audit_columns_present_on_projects() -> None:
    assert "created_at" in SCHEMA and "updated_at" in SCHEMA


def test_cardinality_constraint_on_project_dates() -> None:
    assert "chk_project_dates" in SCHEMA
