from __future__ import annotations

import pandas as pd


class GrowthTrialDataFrameManager:
    """Manages construction and manipulation of a plant growth trial DataFrame."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data.copy()

    def select_measurement_columns(self) -> pd.DataFrame:
        """Return only sample identifiers and measurement columns."""
        return self.data.loc[:, ["sample_id", "height_cm", "leaf_count", "biomass_g"]]

    def select_treated_samples(self) -> pd.DataFrame:
        """Return rows where treatment is not the control group."""
        return self.data[self.data["treatment"] != "control"]

    def add_derived_columns(self) -> pd.DataFrame:
        """Add biomass-per-leaf and height categorization columns."""
        enriched = self.data.copy()
        enriched["biomass_per_leaf"] = (enriched["biomass_g"] / enriched["leaf_count"]).round(3)
        enriched["height_category"] = pd.cut(
            enriched["height_cm"],
            bins=[0, 20, 40, float("inf")],
            labels=["short", "medium", "tall"],
        )
        return enriched

    def drop_administrative_columns(self, columns: list[str]) -> pd.DataFrame:
        """Return the DataFrame with specified non-analytical columns removed."""
        return self.data.drop(columns=columns, errors="ignore")

    def sorted_by_biomass(self, ascending: bool = False) -> pd.DataFrame:
        """Return the DataFrame sorted by biomass, descending by default."""
        return self.data.sort_values(by="biomass_g", ascending=ascending).reset_index(drop=True)

    @staticmethod
    def run() -> None:
        data = pd.DataFrame(
            [
                {"sample_id": "S001", "recorded_by": "lab_tech_1", "treatment": "control",
                 "height_cm": 18.2, "leaf_count": 7, "biomass_g": 2.1},
                {"sample_id": "S002", "recorded_by": "lab_tech_2", "treatment": "nitrogen_high",
                 "height_cm": 25.6, "leaf_count": 9, "biomass_g": 3.8},
                {"sample_id": "S003", "recorded_by": "lab_tech_1", "treatment": "drought_stress",
                 "height_cm": 14.9, "leaf_count": 6, "biomass_g": 1.5},
                {"sample_id": "S004", "recorded_by": "lab_tech_3", "treatment": "nitrogen_high",
                 "height_cm": 41.3, "leaf_count": 12, "biomass_g": 6.7},
            ]
        )

        manager = GrowthTrialDataFrameManager(data)

        print(manager.select_measurement_columns())
        print(manager.select_treated_samples())

        enriched = manager.add_derived_columns()
        print(enriched)

        print(manager.drop_administrative_columns(["recorded_by"]))
        print(manager.sorted_by_biomass())


if __name__ == "__main__":
    GrowthTrialDataFrameManager.run()
