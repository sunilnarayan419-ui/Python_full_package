from __future__ import annotations

import pandas as pd


class MissingMeasurementHandler:
    """Detects and safely handles missing values in experimental measurements."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data.copy()

    def missing_value_matrix(self) -> pd.DataFrame:
        """Return a boolean matrix indicating missing values."""
        return self.data.isna()

    def complete_rows_only(self) -> pd.DataFrame:
        """Return rows containing no missing values at all."""
        return self.data[self.data.notna().all(axis=1)]

    def drop_rows_missing_critical_fields(self, critical_fields: list[str]) -> pd.DataFrame:
        """Return rows dropped only where critical analytical fields are missing."""
        return self.data.dropna(subset=critical_fields)

    def impute_numeric_with_group_median(self, group_col: str, target_col: str) -> pd.DataFrame:
        """Return data with missing numeric values filled using group-wise medians."""
        imputed = self.data.copy()
        imputed[target_col] = imputed.groupby(group_col)[target_col].transform(
            lambda series: series.fillna(series.median())
        )
        return imputed

    def flag_incomplete_samples(self) -> pd.DataFrame:
        """Return the dataset with an added flag column indicating incomplete records."""
        flagged = self.data.copy()
        flagged["is_incomplete"] = flagged.isna().any(axis=1)
        return flagged

    @staticmethod
    def run() -> None:
        data = pd.DataFrame(
            [
                {"sample_id": "S001", "treatment": "control", "height_cm": 22.1, "biomass_g": 4.0, "soil_ph": 6.2},
                {"sample_id": "S002", "treatment": "control", "height_cm": None, "biomass_g": 3.8, "soil_ph": 6.1},
                {"sample_id": "S003", "treatment": "nitrogen_high", "height_cm": 30.4, "biomass_g": None, "soil_ph": 6.4},
                {"sample_id": "S004", "treatment": "nitrogen_high", "height_cm": 33.1, "biomass_g": 7.2, "soil_ph": None},
                {"sample_id": "S005", "treatment": "drought_stress", "height_cm": 15.9, "biomass_g": 2.1, "soil_ph": 5.8},
            ]
        )

        handler = MissingMeasurementHandler(data)

        print(handler.missing_value_matrix())
        print(handler.complete_rows_only())
        print(handler.drop_rows_missing_critical_fields(["height_cm"]))
        print(handler.impute_numeric_with_group_median("treatment", "biomass_g"))
        print(handler.flag_incomplete_samples())


if __name__ == "__main__":
    MissingMeasurementHandler.run()
