from __future__ import annotations

import pandas as pd


class TreatmentGroupAnalyzer:
    """Produces group-level biological summaries across treatments and species."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data.copy()

    def mean_by_treatment(self) -> pd.DataFrame:
        """Return mean measurements grouped by treatment."""
        return self.data.groupby("treatment", as_index=True)[["height_cm", "biomass_g"]].mean().round(2)

    def summary_by_species_and_treatment(self) -> pd.DataFrame:
        """Return grouped summaries across species and treatment combinations."""
        return (
            self.data.groupby(["species", "treatment"])
            .agg(
                mean_height_cm=("height_cm", "mean"),
                mean_biomass_g=("biomass_g", "mean"),
                sample_count=("sample_id", "count"),
            )
            .round(2)
        )

    def multi_metric_aggregation(self) -> pd.DataFrame:
        """Return multiple aggregations per treatment for biomass."""
        return self.data.groupby("treatment")["biomass_g"].agg(["mean", "std", "min", "max"]).round(2)

    def top_species_by_yield(self, n: int = 2) -> pd.DataFrame:
        """Return the top-n highest mean-yield species."""
        species_yield = self.data.groupby("species")["yield_g"].mean().round(2)
        return species_yield.sort_values(ascending=False).head(n).to_frame(name="mean_yield_g")

    def replicate_variability(self) -> pd.DataFrame:
        """Return within-treatment replicate variability (coefficient of variation)."""
        grouped = self.data.groupby("treatment")["biomass_g"]
        cv = (grouped.std() / grouped.mean()).round(3)
        return cv.to_frame(name="coefficient_of_variation")

    @staticmethod
    def run() -> None:
        data = pd.DataFrame(
            [
                {"sample_id": "S001", "species": "Oryza sativa", "treatment": "control",
                 "replicate": 1, "height_cm": 30.1, "biomass_g": 5.2, "yield_g": 40.1},
                {"sample_id": "S002", "species": "Oryza sativa", "treatment": "control",
                 "replicate": 2, "height_cm": 29.4, "biomass_g": 5.0, "yield_g": 39.4},
                {"sample_id": "S003", "species": "Oryza sativa", "treatment": "nitrogen_high",
                 "replicate": 1, "height_cm": 36.7, "biomass_g": 7.1, "yield_g": 52.8},
                {"sample_id": "S004", "species": "Zea mays", "treatment": "control",
                 "replicate": 1, "height_cm": 55.3, "biomass_g": 14.1, "yield_g": 88.2},
                {"sample_id": "S005", "species": "Zea mays", "treatment": "nitrogen_high",
                 "replicate": 1, "height_cm": 61.2, "biomass_g": 16.9, "yield_g": 97.5},
                {"sample_id": "S006", "species": "Zea mays", "treatment": "nitrogen_high",
                 "replicate": 2, "height_cm": 59.8, "biomass_g": 16.1, "yield_g": 94.0},
            ]
        )

        analyzer = TreatmentGroupAnalyzer(data)

        print(analyzer.mean_by_treatment())
        print(analyzer.summary_by_species_and_treatment())
        print(analyzer.multi_metric_aggregation())
        print(analyzer.top_species_by_yield())
        print(analyzer.replicate_variability())


if __name__ == "__main__":
    TreatmentGroupAnalyzer.run()
