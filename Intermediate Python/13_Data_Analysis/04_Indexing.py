from __future__ import annotations

import pandas as pd


class SampleIndexingWorkflow:
    """Demonstrates safe, readable indexing practices on an experimental sample set."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data.copy().set_index("sample_id")

    def select_by_label(self, sample_id: str, columns: list[str]) -> pd.Series:
        """Return specific columns for a sample identified by label."""
        return self.data.loc[sample_id, columns]

    def select_label_range(self, start_id: str, end_id: str) -> pd.DataFrame:
        """Return a contiguous label-based range of samples (index must be sorted)."""
        return self.data.sort_index().loc[start_id:end_id]

    def select_by_position(self, row_positions: list[int], col_positions: list[int]) -> pd.DataFrame:
        """Return a positional selection of rows and columns."""
        return self.data.iloc[row_positions, col_positions]

    def select_high_yield_samples(self, threshold: float) -> pd.DataFrame:
        """Return samples with yield above a threshold using boolean indexing."""
        return self.data.loc[self.data["yield_g"] > threshold]

    def select_treatment_height_pair(self) -> pd.DataFrame:
        """Return only treatment and height columns for all samples."""
        return self.data.loc[:, ["treatment", "height_cm"]]

    @staticmethod
    def run() -> None:
        data = pd.DataFrame(
            [
                {"sample_id": "S001", "treatment": "control", "height_cm": 22.1, "yield_g": 41.2},
                {"sample_id": "S002", "treatment": "nitrogen_high", "height_cm": 29.4, "yield_g": 58.7},
                {"sample_id": "S003", "treatment": "drought_stress", "height_cm": 15.8, "yield_g": 21.3},
                {"sample_id": "S004", "treatment": "nitrogen_high", "height_cm": 33.0, "yield_g": 64.9},
                {"sample_id": "S005", "treatment": "control", "height_cm": 20.5, "yield_g": 38.6},
            ]
        )

        workflow = SampleIndexingWorkflow(data)

        print(workflow.select_by_label("S002", ["treatment", "yield_g"]))
        print(workflow.select_label_range("S001", "S003"))
        print(workflow.select_by_position([0, 2, 4], [0, 2]))
        print(workflow.select_high_yield_samples(threshold=40.0))
        print(workflow.select_treatment_height_pair())


if __name__ == "__main__":
    SampleIndexingWorkflow.run()
