from __future__ import annotations

import math

import pandas as pd


class TrialFeatureEngineer:
    """Derives analytical features from raw plant growth trial measurements."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data.copy()

    def add_ratio_features(self) -> pd.DataFrame:
        """Add height-to-leaf and biomass-to-height ratio features."""
        enriched = self.data.copy()
        enriched["height_to_leaf_ratio"] = (enriched["height_cm"] / enriched["leaf_count"]).round(3)
        enriched["biomass_to_height_ratio"] = (enriched["biomass_g"] / enriched["height_cm"]).round(3)
        return enriched

    def add_growth_rate(self) -> pd.DataFrame:
        """Add a per-day growth-rate feature based on days since planting."""
        enriched = self.data.copy()
        enriched["growth_rate_cm_per_day"] = (
            enriched["height_cm"] / enriched["days_since_planting"]
        ).round(3)
        return enriched

    def add_environmental_indicator(self) -> pd.DataFrame:
        """Add a composite environmental stress indicator from temperature and humidity."""
        enriched = self.data.copy()
        temp_deviation = (enriched["temperature_c"] - 25.0).abs()
        humidity_deficit = (60.0 - enriched["humidity_percent"]).clip(lower=0)
        enriched["stress_indicator"] = (temp_deviation + humidity_deficit / 10).round(3)
        return enriched

    def add_biomass_bins(self) -> pd.DataFrame:
        """Bin continuous biomass measurements into descriptive categories."""
        enriched = self.data.copy()
        enriched["biomass_class"] = pd.cut(
            enriched["biomass_g"],
            bins=[0, 3, 8, float("inf")],
            labels=["low_biomass", "moderate_biomass", "high_biomass"],
        )
        return enriched

    def add_log_transformed_yield(self) -> pd.DataFrame:
        """Add a log-transformed yield feature to reduce right-skew for modeling."""
        enriched = self.data.copy()
        enriched["log_yield"] = enriched["yield_g"].apply(math.log1p).round(4)
        return enriched

    def add_treatment_derived_flags(self) -> pd.DataFrame:
        """Add boolean features derived from the treatment label."""
        enriched = self.data.copy()
        enriched["is_stress_treatment"] = enriched["treatment"].isin(["drought_stress", "heat_stress"])
        enriched["is_nutrient_treatment"] = enriched["treatment"].str.contains("nitrogen", na=False)
        return enriched

    def build_full_feature_set(self) -> pd.DataFrame:
        """Return the dataset enriched with all engineered features."""
        engineer = TrialFeatureEngineer(self.data)
        result = engineer.add_ratio_features()

        engineer = TrialFeatureEngineer(result)
        result = engineer.add_growth_rate()

        engineer = TrialFeatureEngineer(result)
        result = engineer.add_environmental_indicator()

        engineer = TrialFeatureEngineer(result)
        result = engineer.add_biomass_bins()

        engineer = TrialFeatureEngineer(result)
        result = engineer.add_log_transformed_yield()

        engineer = TrialFeatureEngineer(result)
        result = engineer.add_treatment_derived_flags()

        return result

    @staticmethod
    def run() -> None:
        data = pd.DataFrame(
            [
                {"sample_id": "S001", "treatment": "control", "height_cm": 22.1, "leaf_count": 8,
                 "biomass_g": 4.0, "yield_g": 41.0, "days_since_planting": 21,
                 "temperature_c": 24.8, "humidity_percent": 62.0},
                {"sample_id": "S002", "treatment": "nitrogen_high", "height_cm": 33.1, "leaf_count": 11,
                 "biomass_g": 7.2, "yield_g": 68.4, "days_since_planting": 21,
                 "temperature_c": 25.5, "humidity_percent": 58.0},
                {"sample_id": "S003", "treatment": "drought_stress", "height_cm": 15.9, "leaf_count": 6,
                 "biomass_g": 2.1, "yield_g": 19.2, "days_since_planting": 21,
                 "temperature_c": 31.2, "humidity_percent": 35.0},
                {"sample_id": "S004", "treatment": "heat_stress", "height_cm": 18.4, "leaf_count": 7,
                 "biomass_g": 2.8, "yield_g": 24.6, "days_since_planting": 21,
                 "temperature_c": 34.0, "humidity_percent": 40.0},
            ]
        )

        engineer = TrialFeatureEngineer(data)
        result = engineer.build_full_feature_set()

        print(result)


if __name__ == "__main__":
    TrialFeatureEngineer.run()
