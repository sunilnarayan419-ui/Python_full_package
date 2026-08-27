from __future__ import annotations

import pandas as pd


class IndexedExperimentJoiner:
    """Joins indexed experimental datasets by sample identifier."""

    def __init__(self, measurements: pd.DataFrame, environment: pd.DataFrame) -> None:
        self.measurements = measurements.copy().set_index("sample_id")
        self.environment = environment.copy().set_index("sample_id")

    def left_join(self) -> pd.DataFrame:
        """Return measurements joined with environmental data, keeping all measurements."""
        return self.measurements.join(self.environment, how="left")

    def inner_join(self) -> pd.DataFrame:
        """Return only samples present in both indexed datasets."""
        return self.measurements.join(self.environment, how="inner")

    def joined_with_suffix_handling(self, other: pd.DataFrame, other_name: str) -> pd.DataFrame:
        """Return a join against a third dataset with overlapping column suffixes resolved."""
        indexed_other = other.copy().set_index("sample_id")
        return self.measurements.join(
            indexed_other,
            how="left",
            lsuffix="_primary",
            rsuffix=f"_{other_name}",
        )

    @staticmethod
    def run() -> None:
        measurements = pd.DataFrame(
            [
                {"sample_id": "S001", "height_cm": 30.1, "biomass_g": 5.2},
                {"sample_id": "S002", "height_cm": 36.7, "biomass_g": 7.1},
                {"sample_id": "S003", "height_cm": 24.5, "biomass_g": 4.4},
                {"sample_id": "S004", "height_cm": 55.0, "biomass_g": 13.8},
            ]
        )

        environment = pd.DataFrame(
            [
                {"sample_id": "S001", "temperature_c": 24.5, "humidity_percent": 61.0},
                {"sample_id": "S002", "temperature_c": 25.1, "humidity_percent": 58.5},
                {"sample_id": "S004", "temperature_c": 27.9, "humidity_percent": 50.2},
            ]
        )

        soil_data = pd.DataFrame(
            [
                {"sample_id": "S001", "soil_ph": 6.2, "moisture": "normal"},
                {"sample_id": "S002", "soil_ph": 5.9, "moisture": "low"},
                {"sample_id": "S003", "soil_ph": 6.5, "moisture": "normal"},
            ]
        )

        joiner = IndexedExperimentJoiner(measurements, environment)

        print(joiner.left_join())
        print(joiner.inner_join())
        print(joiner.joined_with_suffix_handling(soil_data, "soil"))


if __name__ == "__main__":
    IndexedExperimentJoiner.run()
