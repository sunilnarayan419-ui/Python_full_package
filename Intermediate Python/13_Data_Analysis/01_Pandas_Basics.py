from __future__ import annotations

import pandas as pd


class ExperimentDatasetInspector:
    """Performs a standard initial inspection workflow on an experimental dataset."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data.copy()

    def structural_summary(self) -> dict[str, object]:
        """Return shape, column names, and dtypes for the dataset."""
        return {
            "shape": self.data.shape,
            "columns": list(self.data.columns),
            "dtypes": self.data.dtypes.to_dict(),
        }

    def preview(self, n: int = 3) -> pd.DataFrame:
        """Return the first and last n rows concatenated for a quick preview."""
        return pd.concat([self.data.head(n), self.data.tail(n)])

    def numeric_summary(self) -> pd.DataFrame:
        """Return descriptive statistics for numeric columns."""
        numeric_data = self.data.select_dtypes(include="number")
        return numeric_data.describe()

    def categorical_summary(self) -> pd.DataFrame:
        """Return frequency counts for object/categorical columns."""
        categorical_cols = self.data.select_dtypes(exclude="number").columns
        summaries = {col: self.data[col].value_counts() for col in categorical_cols}
        return pd.DataFrame(summaries).fillna(0).astype(int)

    def missing_value_report(self) -> pd.Series:
        """Return count of missing values per column."""
        return self.data.isna().sum().sort_values(ascending=False)

    @staticmethod
    def run() -> None:
        data = pd.DataFrame(
            [
                {"sample_id": "S001", "species": "Arabidopsis thaliana", "treatment": "control",
                 "height_cm": 12.4, "leaf_count": 8, "biomass_g": 1.9, "soil_ph": 6.5},
                {"sample_id": "S002", "species": "Arabidopsis thaliana", "treatment": "nitrogen_high",
                 "height_cm": 15.7, "leaf_count": 10, "biomass_g": 2.6, "soil_ph": 6.7},
                {"sample_id": "S003", "species": "Oryza sativa", "treatment": "control",
                 "height_cm": 34.2, "leaf_count": 14, "biomass_g": 5.1, "soil_ph": 5.9},
                {"sample_id": "S004", "species": "Oryza sativa", "treatment": "drought_stress",
                 "height_cm": 27.8, "leaf_count": 11, "biomass_g": 3.3, "soil_ph": None},
                {"sample_id": "S005", "species": "Zea mays", "treatment": "nitrogen_high",
                 "height_cm": 58.6, "leaf_count": 9, "biomass_g": 12.4, "soil_ph": 6.1},
            ]
        )

        inspector = ExperimentDatasetInspector(data)

        print(inspector.structural_summary())
        print(inspector.preview())
        print(inspector.numeric_summary())
        print(inspector.categorical_summary())
        print(inspector.missing_value_report())


if __name__ == "__main__":
    ExperimentDatasetInspector.run()
