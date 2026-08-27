from __future__ import annotations

import pandas as pd


class TrialReportPivoter:
    """Reshapes long-format trial measurements into analytical reporting tables."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data.copy()

    def species_treatment_pivot(self) -> pd.DataFrame:
        """Return a pivot table of mean biomass by species and treatment."""
        return pd.pivot_table(
            self.data,
            values="biomass_g",
            index="species",
            columns="treatment",
            aggfunc="mean",
        ).round(2)

    def multi_metric_pivot(self) -> pd.DataFrame:
        """Return a pivot table with multiple aggregated metrics."""
        return pd.pivot_table(
            self.data,
            values=["height_cm", "biomass_g"],
            index="species",
            columns="treatment",
            aggfunc="mean",
        ).round(2)

    def replicate_wide_format(self) -> pd.DataFrame:
        """Return a strict pivot of single replicate-level biomass readings by sample."""
        single_replicate = self.data.drop_duplicates(subset=["species", "treatment"])
        return single_replicate.pivot(index="species", columns="treatment", values="height_cm")

    def sample_count_pivot(self) -> pd.DataFrame:
        """Return a pivot table counting samples per species/treatment combination."""
        return pd.pivot_table(
            self.data,
            values="sample_id",
            index="species",
            columns="treatment",
            aggfunc="count",
            fill_value=0,
        )

    @staticmethod
    def run() -> None:
        data = pd.DataFrame(
            [
                {"sample_id": "S001", "species": "Oryza sativa", "treatment": "control", "height_cm": 30.1, "biomass_g": 5.2},
                {"sample_id": "S002", "species": "Oryza sativa", "treatment": "nitrogen_high", "height_cm": 36.7, "biomass_g": 7.1},
                {"sample_id": "S003", "species": "Oryza sativa", "treatment": "control", "height_cm": 29.0, "biomass_g": 5.0},
                {"sample_id": "S004", "species": "Zea mays", "treatment": "control", "height_cm": 55.3, "biomass_g": 14.1},
                {"sample_id": "S005", "species": "Zea mays", "treatment": "nitrogen_high", "height_cm": 61.2, "biomass_g": 16.9},
                {"sample_id": "S006", "species": "Zea mays", "treatment": "drought_stress", "height_cm": 44.8, "biomass_g": 10.2},
            ]
        )

        pivoter = TrialReportPivoter(data)

        print(pivoter.species_treatment_pivot())
        print(pivoter.multi_metric_pivot())
        print(pivoter.replicate_wide_format())
        print(pivoter.sample_count_pivot())


if __name__ == "__main__":
    TrialReportPivoter.run()
