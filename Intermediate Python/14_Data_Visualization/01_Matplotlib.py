from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd


class PlantGrowthTrendVisualizer:
    """Visualizes plant height progression across treatment groups using core Matplotlib."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data.copy()
        self.data["measurement_date"] = pd.to_datetime(self.data["measurement_date"])

    def prepare_treatment_series(self) -> dict[str, pd.DataFrame]:
        """Split the dataset into per-treatment time-ordered growth series."""
        series: dict[str, pd.DataFrame] = {}
        for treatment, group in self.data.groupby("treatment"):
            series[treatment] = group.sort_values("measurement_date")
        return series

    def create_visualization(self) -> None:
        """Render a labeled, multi-series growth chart with title, legend, and grid."""
        treatment_series = self.prepare_treatment_series()

        fig = plt.figure(figsize=(9, 5.5))
        ax = fig.add_subplot(111)

        markers = {"control": "o", "nitrogen_high": "s", "drought_stress": "^"}
        for treatment, series in treatment_series.items():
            ax.plot(
                series["measurement_date"],
                series["height_cm"],
                marker=markers.get(treatment, "o"),
                linewidth=2,
                label=treatment.replace("_", " ").title(),
            )

        ax.set_title("Plant Height Progression by Treatment Group", fontsize=13, fontweight="bold")
        ax.set_xlabel("Measurement Date")
        ax.set_ylabel("Height (cm)")
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.legend(title="Treatment", loc="upper left")

        fig.autofmt_xdate()
        fig.tight_layout()
        plt.show()

    @staticmethod
    def run() -> None:
        data = pd.DataFrame(
            [
                {"measurement_date": "2024-03-01", "treatment": "control", "height_cm": 5.0},
                {"measurement_date": "2024-03-08", "treatment": "control", "height_cm": 9.2},
                {"measurement_date": "2024-03-15", "treatment": "control", "height_cm": 13.1},
                {"measurement_date": "2024-03-22", "treatment": "control", "height_cm": 16.8},
                {"measurement_date": "2024-03-01", "treatment": "nitrogen_high", "height_cm": 5.2},
                {"measurement_date": "2024-03-08", "treatment": "nitrogen_high", "height_cm": 11.4},
                {"measurement_date": "2024-03-15", "treatment": "nitrogen_high", "height_cm": 18.0},
                {"measurement_date": "2024-03-22", "treatment": "nitrogen_high", "height_cm": 24.6},
                {"measurement_date": "2024-03-01", "treatment": "drought_stress", "height_cm": 4.9},
                {"measurement_date": "2024-03-08", "treatment": "drought_stress", "height_cm": 7.1},
                {"measurement_date": "2024-03-15", "treatment": "drought_stress", "height_cm": 8.9},
                {"measurement_date": "2024-03-22", "treatment": "drought_stress", "height_cm": 10.2},
            ]
        )

        visualizer = PlantGrowthTrendVisualizer(data)
        visualizer.create_visualization()


if __name__ == "__main__":
    PlantGrowthTrendVisualizer.run()
