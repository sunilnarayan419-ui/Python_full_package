from __future__ import annotations

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


class TreatmentResponseStatisticalVisualizer:
    """Builds a statistical visualization workflow comparing treatment response profiles."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data.copy()
        sns.set_theme(style="whitegrid")

    def plot_biomass_distribution(self, ax: plt.Axes) -> None:
        """Show biomass distribution per treatment using a boxplot."""
        sns.boxplot(data=self.data, x="treatment", y="biomass_g", ax=ax, hue="treatment", legend=False)
        ax.set_title("Biomass Distribution by Treatment")
        ax.set_xlabel("Treatment")
        ax.set_ylabel("Biomass (g)")
        ax.tick_params(axis="x", rotation=15)

    def plot_height_density(self, ax: plt.Axes) -> None:
        """Show the full shape of the height distribution per treatment using a violin plot."""
        sns.violinplot(data=self.data, x="treatment", y="height_cm", ax=ax, hue="treatment", legend=False)
        ax.set_title("Height Density by Treatment")
        ax.set_xlabel("Treatment")
        ax.set_ylabel("Height (cm)")
        ax.tick_params(axis="x", rotation=15)

    def plot_growth_trend(self, ax: plt.Axes) -> None:
        """Show mean growth trend over time with a bootstrapped confidence interval."""
        sns.lineplot(data=self.data, x="day", y="height_cm", hue="treatment", marker="o", ax=ax)
        ax.set_title("Growth Trend with Confidence Interval")
        ax.set_xlabel("Day Since Planting")
        ax.set_ylabel("Height (cm)")

    def plot_correlation_heatmap(self, ax: plt.Axes) -> None:
        """Show correlation structure among key numeric measurements."""
        numeric_cols = ["height_cm", "biomass_g", "leaf_count", "chlorophyll"]
        correlation_matrix = self.data[numeric_cols].corr()
        sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="vlag", center=0, ax=ax)
        ax.set_title("Measurement Correlation Matrix")

    def render_dashboard(self) -> None:
        """Assemble the statistical panels into a coherent reporting figure."""
        fig, axes = plt.subplots(2, 2, figsize=(12, 9))

        self.plot_biomass_distribution(axes[0, 0])
        self.plot_height_density(axes[0, 1])
        self.plot_growth_trend(axes[1, 0])
        self.plot_correlation_heatmap(axes[1, 1])

        fig.suptitle("Treatment Response — Statistical Overview", fontsize=15, fontweight="bold")
        fig.tight_layout(rect=(0, 0, 1, 0.95))
        plt.show()

    @staticmethod
    def run() -> None:
        data = pd.DataFrame(
            [
                {"day": 0, "treatment": "control", "height_cm": 5.0, "biomass_g": 0.8, "leaf_count": 3, "chlorophyll": 28.1},
                {"day": 7, "treatment": "control", "height_cm": 9.4, "biomass_g": 1.9, "leaf_count": 5, "chlorophyll": 29.8},
                {"day": 14, "treatment": "control", "height_cm": 13.1, "biomass_g": 2.9, "leaf_count": 6, "chlorophyll": 31.4},
                {"day": 0, "treatment": "nitrogen_high", "height_cm": 5.2, "biomass_g": 0.9, "leaf_count": 3, "chlorophyll": 30.2},
                {"day": 7, "treatment": "nitrogen_high", "height_cm": 11.6, "biomass_g": 2.7, "leaf_count": 7, "chlorophyll": 34.9},
                {"day": 14, "treatment": "nitrogen_high", "height_cm": 18.0, "biomass_g": 4.5, "leaf_count": 9, "chlorophyll": 38.7},
                {"day": 0, "treatment": "drought_stress", "height_cm": 4.9, "biomass_g": 0.7, "leaf_count": 3, "chlorophyll": 25.6},
                {"day": 7, "treatment": "drought_stress", "height_cm": 6.8, "biomass_g": 1.1, "leaf_count": 4, "chlorophyll": 23.1},
                {"day": 14, "treatment": "drought_stress", "height_cm": 8.9, "biomass_g": 1.6, "leaf_count": 5, "chlorophyll": 21.3},
            ]
        )

        visualizer = TreatmentResponseStatisticalVisualizer(data)
        visualizer.render_dashboard()


if __name__ == "__main__":
    TreatmentResponseStatisticalVisualizer.run()
