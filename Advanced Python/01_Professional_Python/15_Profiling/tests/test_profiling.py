from __future__ import annotations

from profiling_demo import (
    naive_edit_distance,
    optimized_edit_distance,
    profile_call,
    time_call,
    trace_peak_memory,
)


def test_implementations_agree_on_edit_distance() -> None:
    assert naive_edit_distance("kitten", "sitting") == optimized_edit_distance("kitten", "sitting")
    assert naive_edit_distance("", "abc") == 3
    assert optimized_edit_distance("abc", "abc") == 0


def test_optimized_is_faster_than_naive_on_moderate_input() -> None:
    a, b = "ACGTACGTAC" * 2, "ACGTACGTAG" * 2
    naive_timing = time_call(lambda: naive_edit_distance(a, b), runs=3)
    optimized_timing = time_call(lambda: optimized_edit_distance(a, b), runs=3)
    assert optimized_timing.best_seconds <= naive_timing.best_seconds


def test_profile_call_captures_stats_and_result() -> None:
    report = profile_call(optimized_edit_distance, "GATTACA", "GATCACA")
    assert report.result == 1
    assert "function calls" in report.stats_text or "cumulative" in report.stats_text


def test_trace_peak_memory_reports_positive_peak() -> None:
    def allocate() -> list[int]:
        return [i for i in range(100_000)]

    result, memory_report = trace_peak_memory(allocate)
    assert len(result) == 100_000
    assert memory_report.peak_bytes > 0
