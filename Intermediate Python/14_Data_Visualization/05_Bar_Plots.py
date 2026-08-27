from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class SpeciesTreatmentBarVisualizer:
    """Compares mean yield across species and treatment groups using grouped bars."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data.copy()

    def aggregate_yield_statistics(self) -> pd.DataFrame:
        """Compute mean and standard deviation of yield per species/treatment combination."""
        return (
            self.data.groupby(["species", "treatment"])["yield_g"]
            .agg(["mean", "std"])
            .reset_index()
        )

    def create_visualization(self) -> None:
        """Render a grouped bar chart with error bars derived from replicate variability."""
        stats = self.aggregate_yield_statistics()
        species_list = sorted(stats["species"].unique())
        treatment_list = sorted(stats["treatment"].unique())

        fig, ax = plt.subplots(figsize=(9.5, 5.5))

        bar_width = 0.8 / len(treatment_list)
        x_positions = np.arange(len(species_list))

        for idx, treatment in enumerate(treatment_list):
            subset = stats[stats["treatment"] == treatment].set_index("species").reindex(species_list)
            offsets = x_positions + idx * bar_width - (0.8 - bar_width) / 2
            ax.bar(
                offsets,
                subset["mean"],
                width=bar_width,
                yerr=subset["std"],
                capsize=4,
                label=treatment.replace("_", " ").title(),
            )

        ax.set_title("Mean Yield by Species and Treatment", fontsize=13, fontweight="bold")
        ax.set_xlabel("Species")
        ax.set_ylabel("Yield (g)")
        ax.set_xticks(x_positions)
        ax.set_xticklabels(species_list)
        ax.legend(title="Treatment")
        ax.grid(True, axis="y", linestyle="--", alpha=0.4)

        fig.tight_layout()
        plt.show()

    @staticmethod
    def run() -> None:
        data = pd.DataFrame(
            [
                {"species": "Oryza sativa", "treatment": "control", "yield_g": 40.1},
                {"species": "Oryza sativa", "treatment": "control", "yield_g": 38.7},
                {"species": "Oryza sativa", "treatment": "nitrogen_high", "yield_g": 52.8},
                {"species": "Oryza sativa", "treatment": "nitrogen_high", "yield_g": 55.4},
                {"species": "Zea mays", "treatment": "control", "yield_g": 88.2},
                {"species": "Zea mays", "treatment": "control", "yield_g": 85.0},
                {"species": "Zea mays", "treatment": "nitrogen_high", "yield_g": 97.5},
                {"species": "Zea mays", "treatment": "nitrogen_high", "yield_g": 101.2},
                {"species": "Glycine max", "treatment": "control", "yield_g": 60.4},
                {"species": "Glycine max", "treatment": "control", "yield_g": 58.9},
                {"species": "Glycine max", "treatment": "nitrogen_high", "yield_g": 66.1},
                {"species": "Glycine max", "treatment": "nitrogen_high", "yield_g": 68.8},
            ]
        )

        visualizer = SpeciesTreatmentBarVisualizer(data)
        visualizer.create_visualization()


if __name__ == "__main__":
    SpeciesTreatmentBarVisualizer.run()
