from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd


class ExperimentFigureManager:
    """Manages explicit Figure-level configuration for experimental reporting."""

    def __init__(self, data: pd.DataFrame, figsize: tuple[float, float] = (10, 6), dpi: int = 120) -> None:
        self.data = data.copy()
        self.figsize = figsize
        self.dpi = dpi

    def create_figure(self) -> Figure:
        """Construct a Figure object with explicit size, resolution, and title."""
        fig = plt.figure(figsize=self.figsize, dpi=self.dpi)
        fig.suptitle("Biomass Yield Report — Multi-Species Trial", fontsize=14, fontweight="bold")
        return fig

    def populate_figure(self, fig: Figure) -> Figure:
        """Attach a grid of visualization elements to the given Figure."""
        ax1 = fig.add_subplot(1, 2, 1)
        ax2 = fig.add_subplot(1, 2, 2)

        species_means = self.data.groupby("species")["biomass_g"].mean().sort_values(ascending=False)
        ax1.bar(species_means.index, species_means.to_numpy(), color="#4C72B0")
        ax1.set_title("Mean Biomass by Species")
        ax1.set_ylabel("Biomass (g)")
        ax1.tick_params(axis="x", rotation=20)

        yield_totals = self.data.groupby("species")["yield_g"].sum().sort_values(ascending=False)
        ax2.bar(yield_totals.index, yield_totals.to_numpy(), color="#55A868")
        ax2.set_title("Total Yield by Species")
        ax2.set_ylabel("Yield (g)")
        ax2.tick_params(axis="x", rotation=20)

        fig.tight_layout(rect=(0, 0, 1, 0.94))
        return fig

    def render(self) -> None:
        """Execute the full figure lifecycle: create, populate, and display."""
        fig = self.create_figure()
        fig = self.populate_figure(fig)
        plt.show()
        plt.close(fig)

    @staticmethod
    def run() -> None:
        data = pd.DataFrame(
            [
                {"species": "Oryza sativa", "biomass_g": 5.2, "yield_g": 41.0},
                {"species": "Oryza sativa", "biomass_g": 5.8, "yield_g": 44.5},
                {"species": "Zea mays", "biomass_g": 14.1, "yield_g": 88.2},
                {"species": "Zea mays", "biomass_g": 16.9, "yield_g": 97.5},
                {"species": "Glycine max", "biomass_g": 9.3, "yield_g": 62.1},
                {"species": "Glycine max", "biomass_g": 8.7, "yield_g": 58.4},
            ]
        )

        manager = ExperimentFigureManager(data, figsize=(10, 6), dpi=120)
        manager.render()


if __name__ == "__main__":
    ExperimentFigureManager.run()
