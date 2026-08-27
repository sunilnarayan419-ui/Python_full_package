from __future__ import annotations

from cpython_lab.bytecode_inspection import (
    contains_via_list,
    contains_via_set,
    count_load_fast_ops,
    disassemble_hot_path,
)
from cpython_lab.interning import group_by_batch_key, identity_batch_key
from cpython_lab.refcounting import build_shared_lookup_closures, refcount_of


def test_disassemble_hot_path_returns_nonempty_listing() -> None:
    output = disassemble_hot_path(contains_via_set)
    assert "CONTAINS_OP" in output or "COMPARE_OP" in output or len(output) > 0


def test_count_load_fast_ops_is_nonzero_for_function_with_locals() -> None:
    def uses_locals(a: int, b: int) -> int:
        c = a + b
        return c

    assert count_load_fast_ops(uses_locals) > 0


def test_set_and_list_membership_agree_on_result() -> None:
    items = ["chr1", "chr2", "chrX"]
    item_set = frozenset(items)
    assert contains_via_list("chr2", items) == contains_via_set("chr2", item_set)
    assert contains_via_list("chrY", items) == contains_via_set("chrY", item_set)


def test_refcount_increases_while_extra_reference_held() -> None:
    obj = object()
    baseline = refcount_of(obj)
    extra_reference = obj
    assert refcount_of(obj) == baseline + 1
    del extra_reference


def test_shared_lookup_closures_share_the_same_table_object() -> None:
    table = {"A": 1.0, "B": 2.0}
    baseline = refcount_of(table)
    closures = build_shared_lookup_closures(table, ["A", "B", "A"])
    assert refcount_of(table) > baseline
    assert all(closure() in table.values() for closure in closures)


def test_identity_batch_key_groups_by_equality_not_identity() -> None:
    records = [("align", 0, 1.0), ("align", 0, 2.0), ("call_variants", 1, 3.0)]
    grouped = group_by_batch_key(records)
    assert grouped[identity_batch_key("align", 0)] == [1.0, 2.0]
    assert grouped[identity_batch_key("call_variants", 1)] == [3.0]
