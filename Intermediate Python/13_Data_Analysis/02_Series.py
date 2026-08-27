from __future__ import annotations

import pandas as pd


class ChlorophyllSeriesAnalyzer:
    """Analyzes a Series of chlorophyll readings collected across replicates."""

    def __init__(self, readings: pd.Series) -> None:
        self.readings = readings.copy()

    def indexed_by_replicate(self, replicate_ids: list[str]) -> pd.Series:
        """Return the readings re-indexed by replicate identifier."""
        indexed = self.readings.copy()
        indexed.index = pd.Index(replicate_ids, name="replicate_id")
        return indexed

    def normalize_to_baseline(self, baseline: float) -> pd.Series:
        """Return readings expressed as a ratio relative to a baseline value."""
        return self.readings.div(baseline).round(4)

    def flag_outliers(self, z_threshold: float = 2.0) -> pd.Series:
        """Return a boolean Series flagging values beyond a z-score threshold."""
        mean_val = self.readings.mean()
        std_val = self.readings.std()
        z_scores = (self.readings - mean_val) / std_val
        return z_scores.abs() > z_threshold

    def summary_statistics(self) -> pd.Series:
        """Return key aggregation statistics for the readings."""
        return pd.Series(
            {
                "mean": self.readings.mean(),
                "median": self.readings.median(),
                "std": self.readings.std(),
                "min": self.readings.min(),
                "max": self.readings.max(),
                "count_valid": self.readings.count(),
            }
        )

    def impute_missing_with_median(self) -> pd.Series:
        """Return readings with missing values imputed using the median."""
        return self.readings.fillna(self.readings.median())

    @staticmethod
    def run() -> None:
        readings = pd.Series(
            [34.2, 36.8, None, 31.5, 39.1, 33.7, None, 40.2, 35.0, 90.4],
            name="chlorophyll_index",
        )
        replicate_ids = [f"REP-{i:02d}" for i in range(1, len(readings) + 1)]

        analyzer = ChlorophyllSeriesAnalyzer(readings)

        indexed = analyzer.indexed_by_replicate(replicate_ids)
        print(indexed)

        print(analyzer.normalize_to_baseline(baseline=35.0))
        print(analyzer.flag_outliers())
        print(analyzer.summary_statistics())
        print(analyzer.impute_missing_with_median())


if __name__ == "__main__":
    ChlorophyllSeriesAnalyzer.run()
