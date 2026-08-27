from __future__ import annotations

import pandas as pd


class SampleMeasurementMerger:
    """Merges sample metadata with experimental measurement records."""

    def __init__(self, metadata: pd.DataFrame, measurements: pd.DataFrame) -> None:
        self.metadata = metadata.copy()
        self.measurements = measurements.copy()

    def validate_key_uniqueness(self) -> None:
        """Ensure sample_id is unique in metadata before merging."""
        if self.metadata["sample_id"].duplicated().any():
            raise ValueError("Duplicate sample_id values found in metadata; merge key must be unique.")

    def inner_merge(self) -> pd.DataFrame:
        """Return an inner merge, keeping only samples present in both datasets."""
        self.validate_key_uniqueness()
        return pd.merge(
            self.measurements,
            self.metadata,
            on="sample_id",
            how="inner",
            validate="many_to_one",
        )

    def left_merge_with_indicator(self) -> pd.DataFrame:
        """Return a left merge retaining all measurements and flagging match source."""
        self.validate_key_uniqueness()
        return pd.merge(
            self.measurements,
            self.metadata,
            on="sample_id",
            how="left",
            indicator="merge_status",
        )

    def unmatched_measurements(self) -> pd.DataFrame:
        """Return measurement rows that have no corresponding metadata record."""
        merged = self.left_merge_with_indicator()
        return merged[merged["merge_status"] == "left_only"].drop(columns=["merge_status"])

    @staticmethod
    def run() -> None:
        metadata = pd.DataFrame(
            [
                {"sample_id": "S001", "species": "Oryza sativa", "variety": "IR64", "treatment": "control"},
                {"sample_id": "S002", "species": "Oryza sativa", "variety": "IR64", "treatment": "nitrogen_high"},
                {"sample_id": "S003", "species": "Zea mays", "variety": "DKC-90", "treatment": "drought_stress"},
                {"sample_id": "S004", "species": "Zea mays", "variety": "DKC-95", "treatment": "control"},
            ]
        )

        measurements = pd.DataFrame(
            [
                {"sample_id": "S001", "height_cm": 30.1, "biomass_g": 5.2},
                {"sample_id": "S002", "height_cm": 36.7, "biomass_g": 7.1},
                {"sample_id": "S003", "height_cm": 24.5, "biomass_g": 4.4},
                {"sample_id": "S005", "height_cm": 41.0, "biomass_g": 8.9},
            ]
        )

        merger = SampleMeasurementMerger(metadata, measurements)

        print(merger.inner_merge())
        print(merger.left_merge_with_indicator())
        print(merger.unmatched_measurements())


if __name__ == "__main__":
    SampleMeasurementMerger.run()
