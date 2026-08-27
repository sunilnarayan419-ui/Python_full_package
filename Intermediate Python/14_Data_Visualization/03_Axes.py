from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import pandas as pd


class SoilPhAxesController:
    """Demonstrates explicit Axes-level configuration for a soil chemistry profile."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data.copy().sort_values("sample_id")

    def configure_axes(self, ax: Axes) -> Axes:
        """Apply explicit axis limits, ticks, grid, and labels to the given Axes."""
        ax.set_xlim(-0.5, len(self.data) - 0.5)
        ax.set_ylim(4.0, 8.0)
        ax.set_xticks(range(len(self.data)))
        ax.set_xticklabels(self.data["sample_id"], rotation=45, ha="right")
        ax.set_yticks([4.0, 5.0, 6.0, 6.5, 7.0, 8.0])
        ax.set_xlabel("Sample ID")
        ax.set_ylabel("Soil pH")
        ax.grid(True, axis="y", linestyle=":", alpha=0.5)
        return ax

    def plot_ph_with_optimal_band(self, ax: Axes) -> Axes:
        """Plot soil pH readings with a shaded optimal-range band and legend."""
        positions = range(len(self.data))
        ax.axhspan(6.0, 7.0, color="#C6E5C6", alpha=0.6, label="Optimal Range (6.0–7.0)")
        ax.plot(positions, self.data["soil_ph"], marker="o", color="#4C72B0", label="Measured pH")
        ax.legend(loc="lower right")
        return ax

    def render(self) -> None:
        """Create explicit Figure/Axes objects, configure, plot, and display."""
        fig, ax = plt.subplots(figsize=(9, 5))
        ax = self.configure_axes(ax)
        ax = self.plot_ph_with_optimal_band(ax)
        ax.set_title("Soil pH Profile Across Field Samples", fontsize=13, fontweight="bold")
        fig.tight_layout()
        plt.show()

    @staticmethod
    def run() -> None:
        data = pd.DataFrame(
            [
                {"sample_id": "S001", "soil_ph": 6.2},
                {"sample_id": "S002", "soil_ph": 5.7},
                {"sample_id": "S003", "soil_ph": 6.8},
                {"sample_id": "S004", "soil_ph": 7.3},
                {"sample_id": "S005", "soil_ph": 6.5},
                {"sample_id": "S006", "soil_ph": 5.4},
                {"sample_id": "S007", "soil_ph": 6.1},
            ]
        )

        controller = SoilPhAxesController(data)
        controller.render()


if __name__ == "__main__":
    SoilPhAxesController.run()
