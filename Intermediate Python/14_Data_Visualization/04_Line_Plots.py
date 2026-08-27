from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd


class DrugResponseTimeCourseVisualizer:
    """Visualizes cell viability response over time across drug concentrations."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data.copy()
        self.data["measurement_date"] = pd.to_datetime(self.data["measurement_date"])

    def prepare_concentration_series(self) -> dict[str, pd.DataFrame]:
        """Return time-ordered viability series grouped by drug concentration."""
        return {
            concentration: group.sort_values("measurement_date")
            for concentration, group in self.data.groupby("concentration_mg_l")
        }

    def create_visualization(self) -> None:
        """Render a multi-series line chart with distinct markers and line styles."""
        concentration_series = self.prepare_concentration_series()

        fig, ax = plt.subplots(figsize=(9, 5.5))

        line_styles = ["-", "--", "-.", ":"]
        markers = ["o", "s", "^", "D"]

        for idx, (concentration, series) in enumerate(sorted(concentration_series.items())):
            ax.plot(
                series["measurement_date"],
                series["cell_viability"],
                linestyle=line_styles[idx % len(line_styles)],
                marker=markers[idx % len(markers)],
                linewidth=2,
                label=f"{concentration} mg/L",
            )

        ax.set_title("Cell Viability Time Course by Drug Concentration", fontsize=13, fontweight="bold")
        ax.set_xlabel("Measurement Date")
        ax.set_ylabel("Cell Viability (%)")
        ax.set_ylim(0, 105)
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.legend(title="Concentration", loc="lower left")

        fig.autofmt_xdate()
        fig.tight_layout()
        plt.show()

    @staticmethod
    def run() -> None:
        data = pd.DataFrame(
            [
                {"measurement_date": "2024-05-01", "concentration_mg_l": 0.0, "cell_viability": 98.5},
                {"measurement_date": "2024-05-02", "concentration_mg_l": 0.0, "cell_viability": 97.9},
                {"measurement_date": "2024-05-03", "concentration_mg_l": 0.0, "cell_viability": 98.1},
                {"measurement_date": "2024-05-01", "concentration_mg_l": 5.0, "cell_viability": 91.2},
                {"measurement_date": "2024-05-02", "concentration_mg_l": 5.0, "cell_viability": 85.6},
                {"measurement_date": "2024-05-03", "concentration_mg_l": 5.0, "cell_viability": 79.8},
                {"measurement_date": "2024-05-01", "concentration_mg_l": 20.0, "cell_viability": 74.3},
                {"measurement_date": "2024-05-02", "concentration_mg_l": 20.0, "cell_viability": 58.1},
                {"measurement_date": "2024-05-03", "concentration_mg_l": 20.0, "cell_viability": 41.7},
                {"measurement_date": "2024-05-01", "concentration_mg_l": 50.0, "cell_viability": 52.0},
                {"measurement_date": "2024-05-02", "concentration_mg_l": 50.0, "cell_viability": 28.4},
                {"measurement_date": "2024-05-03", "concentration_mg_l": 50.0, "cell_viability": 12.6},
            ]
        )

        visualizer = DrugResponseTimeCourseVisualizer(data)
        visualizer.create_visualization()


if __name__ == "__main__":
    DrugResponseTimeCourseVisualizer.run()
