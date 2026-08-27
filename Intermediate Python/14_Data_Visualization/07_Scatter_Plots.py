from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class DoseResponseScatterVisualizer:
    """Visualizes the relationship between drug concentration and cellular response."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data.copy()

    def fit_trend_line(self) -> tuple[float, float]:
        """Fit a simple linear trend (slope, intercept) across all observations."""
        slope, intercept = np.polyfit(self.data["concentration_mg_l"], self.data["response_percent"], deg=1)
        return float(slope), float(intercept)

    def create_visualization(self) -> None:
        """Render a grouped scatter plot with an overall linear trend line."""
        fig, ax = plt.subplots(figsize=(9, 5.5))

        cell_lines = sorted(self.data["cell_line"].unique())
        markers = {"HeLa": "o", "MCF-7": "s", "A549": "^"}

        for cell_line in cell_lines:
            subset = self.data[self.data["cell_line"] == cell_line]
            ax.scatter(
                subset["concentration_mg_l"],
                subset["response_percent"],
                marker=markers.get(cell_line, "o"),
                s=60,
                alpha=0.75,
                label=cell_line,
            )

        slope, intercept = self.fit_trend_line()
        x_range = np.linspace(self.data["concentration_mg_l"].min(), self.data["concentration_mg_l"].max(), 100)
        ax.plot(x_range, slope * x_range + intercept, color="black", linestyle="--", linewidth=1.5,
                label="Linear Trend")

        ax.set_title("Drug Concentration vs. Cellular Response", fontsize=13, fontweight="bold")
        ax.set_xlabel("Concentration (mg/L)")
        ax.set_ylabel("Response (%)")
        ax.legend(title="Cell Line")
        ax.grid(True, linestyle="--", alpha=0.4)

        fig.tight_layout()
        plt.show()

    @staticmethod
    def run() -> None:
        data = pd.DataFrame(
            [
                {"cell_line": "HeLa", "concentration_mg_l": 1.0, "response_percent": 8.2},
                {"cell_line": "HeLa", "concentration_mg_l": 5.0, "response_percent": 22.5},
                {"cell_line": "HeLa", "concentration_mg_l": 10.0, "response_percent": 41.0},
                {"cell_line": "HeLa", "concentration_mg_l": 20.0, "response_percent": 68.3},
                {"cell_line": "HeLa", "concentration_mg_l": 40.0, "response_percent": 89.1},
                {"cell_line": "MCF-7", "concentration_mg_l": 1.0, "response_percent": 5.6},
                {"cell_line": "MCF-7", "concentration_mg_l": 5.0, "response_percent": 18.4},
                {"cell_line": "MCF-7", "concentration_mg_l": 10.0, "response_percent": 35.7},
                {"cell_line": "MCF-7", "concentration_mg_l": 20.0, "response_percent": 60.2},
                {"cell_line": "MCF-7", "concentration_mg_l": 40.0, "response_percent": 84.9},
                {"cell_line": "A549", "concentration_mg_l": 1.0, "response_percent": 9.8},
                {"cell_line": "A549", "concentration_mg_l": 5.0, "response_percent": 26.1},
                {"cell_line": "A549", "concentration_mg_l": 10.0, "response_percent": 46.5},
                {"cell_line": "A549", "concentration_mg_l": 20.0, "response_percent": 71.7},
                {"cell_line": "A549", "concentration_mg_l": 40.0, "response_percent": 92.4},
            ]
        )

        visualizer = DoseResponseScatterVisualizer(data)
        visualizer.create_visualization()


if __name__ == "__main__":
    DoseResponseScatterVisualizer.run()
