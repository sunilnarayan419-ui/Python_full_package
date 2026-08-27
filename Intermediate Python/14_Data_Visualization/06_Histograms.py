from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd


class BiomassDistributionVisualizer:
    """Visualizes the distribution of biomass measurements across a trial population."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data.copy()

    def compute_summary_statistics(self) -> dict[str, float]:
        """Return mean and median biomass for reference-line annotation."""
        return {
            "mean": float(self.data["biomass_g"].mean()),
            "median": float(self.data["biomass_g"].median()),
        }

    def create_visualization(self) -> None:
        """Render a histogram of biomass with mean and median reference lines."""
        stats = self.compute_summary_statistics()

        fig, ax = plt.subplots(figsize=(9, 5.5))

        ax.hist(
            self.data["biomass_g"],
            bins=12,
            color="#4C72B0",
            edgecolor="white",
            alpha=0.85,
        )

        ax.axvline(stats["mean"], color="#C44E52", linestyle="--", linewidth=2,
                   label=f"Mean = {stats['mean']:.2f} g")
        ax.axvline(stats["median"], color="#55A868", linestyle=":", linewidth=2,
                   label=f"Median = {stats['median']:.2f} g")

        ax.set_title("Distribution of Biomass Across Trial Samples", fontsize=13, fontweight="bold")
        ax.set_xlabel("Biomass (g)")
        ax.set_ylabel("Number of Samples")
        ax.legend()
        ax.grid(True, axis="y", linestyle="--", alpha=0.4)

        fig.tight_layout()
        plt.show()

    @staticmethod
    def run() -> None:
        data = pd.DataFrame(
            {
                "sample_id": [f"S{i:03d}" for i in range(1, 41)],
                "biomass_g": [
                    4.1, 4.8, 5.2, 5.5, 5.9, 6.1, 6.3, 6.4, 6.6, 6.8,
                    6.9, 7.0, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8,
                    7.9, 8.0, 8.1, 8.2, 8.4, 8.5, 8.7, 8.9, 9.1, 9.3,
                    9.6, 9.9, 10.2, 10.6, 11.0, 11.5, 12.1, 12.8, 13.6, 14.5,
                ],
            }
        )

        visualizer = BiomassDistributionVisualizer(data)
        visualizer.create_visualization()


if __name__ == "__main__":
    BiomassDistributionVisualizer.run()
