from __future__ import annotations

import pandas as pd


class TrialSampleFilter:
    """Applies realistic research-driven filtering rules to a trial sample dataset."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data.copy()

    def eligible_for_analysis(self) -> pd.DataFrame:
        """Return samples with non-missing biomass and disease_score below threshold."""
        condition = self.data["biomass_g"].notna() & (self.data["disease_score"] < 3)
        return self.data[condition]

    def high_stress_or_low_ph(self) -> pd.DataFrame:
        """Return samples that are drought/heat stressed or have low soil pH."""
        stressed = self.data["treatment"].isin(["drought_stress", "heat_stress"])
        low_ph = self.data["soil_ph"] < 5.8
        return self.data[stressed | low_ph]

    def non_control_within_ph_range(self, low: float, high: float) -> pd.DataFrame:
        """Return non-control samples whose soil pH falls within a numeric range."""
        not_control = ~(self.data["treatment"] == "control")
        in_range = self.data["soil_ph"].between(low, high)
        return self.data[not_control & in_range]

    def species_subset(self, species_list: list[str]) -> pd.DataFrame:
        """Return rows whose species is present in the provided list."""
        return self.data[self.data["species"].isin(species_list)]

    def matching_variety_prefix(self, prefix: str) -> pd.DataFrame:
        """Return samples whose variety name starts with a given prefix."""
        return self.data[self.data["variety"].str.startswith(prefix, na=False)]

    def complete_records(self) -> pd.DataFrame:
        """Return only rows with no missing values across analytical columns."""
        analytical_cols = ["height_cm", "biomass_g", "soil_ph", "disease_score"]
        return self.data.dropna(subset=analytical_cols)

    @staticmethod
    def run() -> None:
        data = pd.DataFrame(
            [
                {"sample_id": "S001", "species": "Oryza sativa", "variety": "IR64-A", "treatment": "control",
                 "height_cm": 30.1, "biomass_g": 5.2, "soil_ph": 6.2, "disease_score": 1},
                {"sample_id": "S002", "species": "Oryza sativa", "variety": "IR64-B", "treatment": "drought_stress",
                 "height_cm": 24.5, "biomass_g": None, "soil_ph": 5.4, "disease_score": 4},
                {"sample_id": "S003", "species": "Zea mays", "variety": "DKC-90", "treatment": "heat_stress",
                 "height_cm": 55.3, "biomass_g": 14.1, "soil_ph": 6.8, "disease_score": 2},
                {"sample_id": "S004", "species": "Zea mays", "variety": "DKC-95", "treatment": "nitrogen_high",
                 "height_cm": 61.2, "biomass_g": 16.9, "soil_ph": 5.7, "disease_score": 1},
                {"sample_id": "S005", "species": "Glycine max", "variety": "PI-548", "treatment": "control",
                 "height_cm": 40.0, "biomass_g": 9.3, "soil_ph": 6.0, "disease_score": 5},
            ]
        )

        sample_filter = TrialSampleFilter(data)

        print(sample_filter.eligible_for_analysis())
        print(sample_filter.high_stress_or_low_ph())
        print(sample_filter.non_control_within_ph_range(5.5, 6.5))
        print(sample_filter.species_subset(["Oryza sativa", "Glycine max"]))
        print(sample_filter.matching_variety_prefix("DKC"))
        print(sample_filter.complete_records())


if __name__ == "__main__":
    TrialSampleFilter.run()
