from __future__ import annotations

from pipeline_qc import QcThresholds, ReadQualityReport, evaluate_run


def test_evaluate_run_flags_only_failing_samples() -> None:
    good = ReadQualityReport("S1", mean_quality=35.0, read_count=2_000_000, duplication_rate=0.1)
    bad = ReadQualityReport("S2", mean_quality=20.0, read_count=500_000, duplication_rate=0.5)
    failures = evaluate_run([good, bad])
    assert "S1" not in failures
    assert "S2" in failures
    assert len(failures["S2"]) == 3


def test_custom_thresholds_are_respected() -> None:
    report = ReadQualityReport("S3", mean_quality=25.0, read_count=1_500_000, duplication_rate=0.1)
    lenient = QcThresholds(min_mean_quality=20.0)
    assert evaluate_run([report], lenient) == {}
