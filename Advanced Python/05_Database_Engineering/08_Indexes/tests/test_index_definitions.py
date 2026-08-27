from __future__ import annotations

import re
from pathlib import Path

SQL_DIR = Path(__file__).resolve().parents[1] / "sql"


def _read(name: str) -> str:
    return (SQL_DIR / name).read_text()


def test_every_index_statement_targets_the_compounds_table() -> None:
    content = _read("index_strategies.sql")
    statements = re.findall(r"CREATE(?:\s+UNIQUE)?\s+INDEX.*?;", content, re.DOTALL)
    assert len(statements) >= 6
    for stmt in statements:
        assert "ON compounds" in stmt


def test_partial_index_has_a_where_clause() -> None:
    content = _read("index_strategies.sql")
    partial = re.search(r"idx_compounds_active.*?;", content, re.DOTALL)
    assert partial is not None
    assert "WHERE is_archived = FALSE" in partial.group(0)


def test_gin_indexes_declared_for_array_and_jsonb_columns() -> None:
    content = _read("index_strategies.sql")
    assert "USING GIN (tags)" in content
    assert "USING GIN (metadata jsonb_path_ops)" in content


def test_covering_index_uses_include_clause() -> None:
    content = _read("index_strategies.sql")
    assert "INCLUDE (molecular_weight, inchi_key)" in content
