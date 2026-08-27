from __future__ import annotations

import pytest

from debug_toolkit import BatchProcessingError, capture_failure_context, process_batch, run_async_pipeline
from debug_toolkit.diagnostics import assert_invariant


def test_process_batch_succeeds_on_clean_records() -> None:
    records = [{"dosage_mg": "10.5"}, {"dosage_mg": "2.0"}]
    assert process_batch(records) == [10.5, 2.0]


def test_process_batch_reports_all_malformed_records_reproducibly() -> None:
    records = [{"dosage_mg": "10.5"}, {"dosage_mg": "not-a-number"}, {"dosage_mg": "3.0"}]
    with pytest.raises(BatchProcessingError) as exc_info:
        process_batch(records)
    failures = exc_info.value.failed_records
    assert len(failures) == 1
    assert failures[0].index == 1
    assert failures[0].context.exception_type == "ValueError"


def test_capture_failure_context_snapshots_locals() -> None:
    def trigger() -> None:
        sample_id = "S-42"
        raise RuntimeError("boom")

    try:
        trigger()
    except RuntimeError as exc:
        context = capture_failure_context(exc)
        assert context.exception_type == "RuntimeError"
        assert any("S-42" in value for value in context.local_snapshot.values())


def test_assert_invariant_raises_with_clear_message() -> None:
    with pytest.raises(AssertionError, match="pool must not be empty"):
        assert_invariant(False, "pool must not be empty")


@pytest.mark.asyncio
async def test_async_pipeline_isolates_per_task_failures() -> None:
    samples = [("S1", 0.0, 5.0), ("S2", 0.0, -1.0), ("S3", 0.0, 3.0)]
    outcomes = await run_async_pipeline(samples)
    by_id = {o.task_id: o for o in outcomes}
    assert by_id["S1"].value == 5.0
    assert by_id["S2"].failure is not None
    assert by_id["S2"].failure.exception_type == "ValueError"
    assert by_id["S3"].value == 3.0
