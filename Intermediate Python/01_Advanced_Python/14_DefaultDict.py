from __future__ import annotations

from collections import defaultdict


class UniversityDefaultDict:
    """Demonstrates collections.defaultdict for simple grouping without
    manual key-existence checks."""

    @staticmethod
    def group_by_species(samples: list[tuple[str, str]]) -> dict[str, list[str]]:
        grouped: defaultdict[str, list[str]] = defaultdict(list)
        for species, sample_id in samples:
            grouped[species].append(sample_id)
        return dict(grouped)

    @staticmethod
    def run() -> None:
        samples = [
            ("Rosa", "r-01"),
            ("Tulipa", "t-01"),
            ("Rosa", "r-02"),
            ("Tulipa", "t-02"),
            ("Rosa", "r-03"),
        ]
        print(UniversityDefaultDict.group_by_species(samples))


class InterviewDefaultDict:
    """Demonstrates nested defaultdict structures and defaultdict(int) for
    counting/aggregation, a common interview-relevant pattern for
    multi-level grouping."""

    @staticmethod
    def aggregate_expression_by_tissue(
        readings: list[tuple[str, str, float]],
    ) -> dict[str, dict[str, float]]:
        totals: defaultdict[str, defaultdict[str, float]] = defaultdict(lambda: defaultdict(float))
        for tissue, gene, value in readings:
            totals[tissue][gene] += value
        return {tissue: dict(genes) for tissue, genes in totals.items()}

    @staticmethod
    def run() -> None:
        readings = [
            ("leaf", "PSII", 4.1),
            ("root", "AUX1", 2.3),
            ("leaf", "PSII", 3.9),
            ("leaf", "RBCL", 5.0),
            ("root", "AUX1", 1.7),
        ]
        result = InterviewDefaultDict.aggregate_expression_by_tissue(readings)
        for tissue, genes in result.items():
            print(f"{tissue}: {genes}")


class IndustryDefaultDict:
    """Demonstrates defaultdict used inside a well-encapsulated aggregation
    service, with a factory function instead of a lambda for clarity and
    picklability, applied to a realistic multi-lab data-consolidation
    scenario."""

    class QualityMetricsAggregator:
        """Aggregates per-lab quality-control metrics without requiring
        callers to pre-initialize nested structures."""

        def __init__(self) -> None:
            self._pass_counts: defaultdict[str, int] = defaultdict(int)
            self._fail_counts: defaultdict[str, int] = defaultdict(int)
            self._readings_by_lab: defaultdict[str, list[float]] = defaultdict(list)

        def record(self, lab_id: str, passed: bool, metric_value: float) -> None:
            if passed:
                self._pass_counts[lab_id] += 1
            else:
                self._fail_counts[lab_id] += 1
            self._readings_by_lab[lab_id].append(metric_value)

        def pass_rate(self, lab_id: str) -> float:
            total = self._pass_counts[lab_id] + self._fail_counts[lab_id]
            return round(self._pass_counts[lab_id] / total, 4) if total else 0.0

        def average_metric(self, lab_id: str) -> float:
            readings = self._readings_by_lab[lab_id]
            return round(sum(readings) / len(readings), 4) if readings else 0.0

        def summary(self) -> dict[str, dict[str, float]]:
            lab_ids = set(self._pass_counts) | set(self._fail_counts)
            return {
                lab_id: {
                    "pass_rate": self.pass_rate(lab_id),
                    "average_metric": self.average_metric(lab_id),
                }
                for lab_id in sorted(lab_ids)
            }

    @staticmethod
    def run() -> None:
        aggregator = IndustryDefaultDict.QualityMetricsAggregator()
        aggregator.record("lab-A", True, 98.2)
        aggregator.record("lab-A", False, 60.1)
        aggregator.record("lab-A", True, 95.4)
        aggregator.record("lab-B", True, 99.0)
        aggregator.record("lab-B", True, 97.8)

        for lab_id, metrics in aggregator.summary().items():
            print(f"{lab_id}: {metrics}")


if __name__ == "__main__":
    UniversityDefaultDict.run()
    InterviewDefaultDict.run()
    IndustryDefaultDict.run()
