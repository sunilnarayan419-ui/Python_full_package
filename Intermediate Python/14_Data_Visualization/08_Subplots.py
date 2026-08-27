from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd


class TrialOverviewDashboard:
    """Builds a coherent multi-panel overview of a plant growth trial."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data.copy()
        self.data["measurement_date"] = pd.to_datetime(self.data["measurement_date"])

    def plot_height_over_time(self, ax: plt.Axes) -> None:
        """Plot mean height progression over time, one line per treatment."""
        for treatment, group in self.data.groupby("treatment"):
            trend = group.groupby("measurement_date")["height_cm"].mean().sort_index()
            ax.plot(trend.index, trend.to_numpy(), marker="o", label=treatment.replace("_", " ").title())
        ax.set_title("Height Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Height (cm)")
        ax.legend(fontsize=8)
        ax.tick_params(axis="x", rotation=30)

    def plot_biomass_by_treatment(self, ax: plt.Axes) -> None:
        """Plot mean biomass per treatment as a bar chart."""
        means = self.data.groupby("treatment")["biomass_g"].mean().sort_values(ascending=False)
        ax.bar(means.index, means.to_numpy(), color="#55A868")
        ax.set_title("Mean Biomass by Treatment")
        ax.set_ylabel("Biomass (g)")
        ax.tick_params(axis="x", rotation=20)

    def plot_leaf_count_distribution(self, ax: plt.Axes) -> None:
        """Plot the distribution of leaf counts across all samples."""
        ax.hist(self.data["leaf_count"], bins=8, color="#C44E52", edgecolor="white")
        ax.set_title("Leaf Count Distribution")
        ax.set_xlabel("Leaf Count")
        ax.set_ylabel("Frequency")

    def plot_chlorophyll_response(self, ax: plt.Axes) -> None:
        """Plot chlorophyll index against biomass to reveal a physiological relationship."""
        ax.scatter(self.data["chlorophyll"], self.data["biomass_g"], alpha=0.7, color="#4C72B0")
        ax.set_title("Chlorophyll vs. Biomass")
        ax.set_xlabel("Chlorophyll Index")
        ax.set_ylabel("Biomass (g)")

    def render_dashboard(self) -> None:
        """Assemble all four panels into a single coherent trial-overview figure."""
        fig, axes = plt.subplots(2, 2, figsize=(11, 8))

        self.plot_height_over_time(axes[0, 0])
        self.plot_biomass_by_treatment(axes[0, 1])
        self.plot_leaf_count_distribution(axes[1, 0])
        self.plot_chlorophyll_response(axes[1, 1])

        fig.suptitle("Plant Growth Trial — Analytical Overview", fontsize=15, fontweight="bold")
        fig.tight_layout(rect=(0, 0, 1, 0.95))
        plt.show()

    @staticmethod
    def run() -> None:
        data = pd.DataFrame(
            [
                {"measurement_date": "2024-03-01", "treatment": "control", "height_cm": 5.0, "biomass_g": 0.8, "leaf_count": 3, "chlorophyll": 28.1},
                {"measurement_date": "2024-03-15", "treatment": "control", "height_cm": 13.1, "biomass_g": 2.9, "leaf_count": 6, "chlorophyll": 31.4},
                {"measurement_date": "2024-03-01", "treatment": "nitrogen_high", "height_cm": 5.2, "biomass_g": 0.9, "leaf_count": 3, "chlorophyll": 30.2},
                {"measurement_date": "2024-03-15", "treatment": "nitrogen_high", "height_cm": 18.0, "biomass_g": 4.5, "leaf_count": 9, "chlorophyll": 38.7},
                {"measurement_date": "2024-03-01", "treatment": "drought_stress", "height_cm": 4.9, "biomass_g": 0.7, "leaf_count": 3, "chlorophyll": 25.6},
                {"measurement_date": "2024-03-15", "treatment": "drought_stress", "height_cm": 8.9, "biomass_g": 1.6, "leaf_count": 5, "chlorophyll": 21.3},
            ]
        )

        dashboard = TrialOverviewDashboard(data)
        dashboard.render_dashboard()


if __name__ == "__main__":
    TrialOverviewDashboard.run()
