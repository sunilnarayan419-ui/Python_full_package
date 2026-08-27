from __future__ import annotations

import pandas as pd


class GrowthTrendAnalyzer:
    """Analyzes time-indexed biological/environmental measurements for trends."""

    def __init__(self, data: pd.DataFrame) -> None:
        prepared = data.copy()
        prepared["measurement_date"] = pd.to_datetime(prepared["measurement_date"])
        self.data = prepared.sort_values("measurement_date").reset_index(drop=True)

    def as_time_indexed(self) -> pd.DataFrame:
        """Return the dataset indexed by measurement date."""
        return self.data.set_index("measurement_date")

    def weekly_mean_height(self) -> pd.Series:
        """Return weekly resampled mean height."""
        return self.as_time_indexed()["height_cm"].resample("W").mean().round(2)

    def rolling_growth_trend(self, window: int = 3) -> pd.DataFrame:
        """Return a rolling mean of height and biomass to smooth measurement noise."""
        indexed = self.as_time_indexed()
        rolling = indexed[["height_cm", "biomass_g"]].rolling(window=window, min_periods=1).mean()
        return rolling.round(2)

    def measurements_within_range(self, start: str, end: str) -> pd.DataFrame:
        """Return measurements recorded within an inclusive date range."""
        indexed = self.as_time_indexed()
        return indexed.loc[start:end]

    def daily_growth_rate(self) -> pd.Series:
        """Return day-over-day change in height, useful for growth-rate tracking."""
        indexed = self.as_time_indexed()
        return indexed["height_cm"].diff().round(3)

    @staticmethod
    def run() -> None:
        data = pd.DataFrame(
            [
                {"measurement_date": "2024-03-01", "height_cm": 5.0, "biomass_g": 0.8},
                {"measurement_date": "2024-03-04", "height_cm": 6.8, "biomass_g": 1.1},
                {"measurement_date": "2024-03-08", "height_cm": 9.1, "biomass_g": 1.7},
                {"measurement_date": "2024-03-11", "height_cm": 11.4, "biomass_g": 2.3},
                {"measurement_date": "2024-03-15", "height_cm": 14.0, "biomass_g": 3.0},
                {"measurement_date": "2024-03-19", "height_cm": 16.9, "biomass_g": 3.8},
                {"measurement_date": "2024-03-22", "height_cm": 19.2, "biomass_g": 4.4},
            ]
        )

        analyzer = GrowthTrendAnalyzer(data)

        print(analyzer.weekly_mean_height())
        print(analyzer.rolling_growth_trend())
        print(analyzer.measurements_within_range("2024-03-08", "2024-03-19"))
        print(analyzer.daily_growth_rate())


if __name__ == "__main__":
    GrowthTrendAnalyzer.run()
