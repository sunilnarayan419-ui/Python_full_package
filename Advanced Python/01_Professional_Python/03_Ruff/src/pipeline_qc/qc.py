"""Sequencing-run QC evaluation, written to satisfy a strict Ruff rule set
(pycodestyle, pyflakes, isort, pep8-naming, pyupgrade, bugbear,
comprehensions, simplify, bandit-security, pylint subset, pytest style).
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class QcThresholds:
    min_mean_quality: float = 30.0
    min_reads: int = 1_000_000
    max_duplication_rate: float = 0.30


@dataclass(frozen=True, slots=True)
class ReadQualityReport:
    sample_id: str
    mean_quality: float
    read_count: int
    duplication_rate: float

    def failures(self, thresholds: QcThresholds) -> list[str]:
        problems: list[str] = []
        if self.mean_quality < thresholds.min_mean_quality:
            problems.append(
                f"mean_quality {self.mean_quality:.1f} below "
                f"{thresholds.min_mean_quality:.1f}"
            )
        if self.read_count < thresholds.min_reads:
            problems.append(f"read_count {self.read_count} below {thresholds.min_reads}")
        if self.duplication_rate > thresholds.max_duplication_rate:
            problems.append(
                f"duplication_rate {self.duplication_rate:.2f} exceeds "
                f"{thresholds.max_duplication_rate:.2f}"
            )
        return problems


def checksum_for(path: Path) -> str:
    """Compute a non-cryptographic-context checksum for file integrity
    tracking. `usedforsecurity=False` satisfies bandit-style linting
    (S324) since this is an integrity check, not a security control.
    """
    digest = hashlib.sha256(usedforsecurity=False)
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def evaluate_run(
    reports: list[ReadQualityReport], thresholds: QcThresholds | None = None
) -> dict[str, list[str]]:
    active_thresholds = thresholds if thresholds is not None else QcThresholds()
    return {
        report.sample_id: failures
        for report in reports
        if (failures := report.failures(active_thresholds))
    }
