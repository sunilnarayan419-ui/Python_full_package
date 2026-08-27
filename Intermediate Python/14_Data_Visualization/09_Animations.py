from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D
import pandas as pd


class GrowthProgressionAnimator:
    """Animates plant height progression over the course of an experiment."""

    def __init__(self, data: pd.DataFrame, interval_ms: int = 400) -> None:
        self.data = data.copy().sort_values("day")
        self.interval_ms = interval_ms
        self.fig, self.ax = plt.subplots(figsize=(8, 5))
        self.line: Line2D | None = None

    def initialize_axes(self) -> tuple[Line2D]:
        """Configure static axis properties and create the initial empty line artist."""
        self.ax.set_xlim(self.data["day"].min(), self.data["day"].max())
        self.ax.set_ylim(0, self.data["height_cm"].max() * 1.1)
        self.ax.set_title("Plant Growth Progression Over Time", fontsize=13, fontweight="bold")
        self.ax.set_xlabel("Day Since Planting")
        self.ax.set_ylabel("Height (cm)")
        self.ax.grid(True, linestyle="--", alpha=0.4)

        (self.line,) = self.ax.plot([], [], marker="o", color="#4C72B0", linewidth=2)
        return (self.line,)

    def update_frame(self, frame_index: int) -> tuple[Line2D]:
        """Update the line artist to reveal data up through the given frame index."""
        subset = self.data.iloc[: frame_index + 1]
        self.line.set_data(subset["day"].to_numpy(), subset["height_cm"].to_numpy())
        return (self.line,)

    def build_animation(self) -> FuncAnimation:
        """Construct a deterministic FuncAnimation over the full measurement sequence."""
        return FuncAnimation(
            self.fig,
            self.update_frame,
            frames=len(self.data),
            init_func=self.initialize_axes,
            interval=self.interval_ms,
            blit=True,
            repeat=False,
        )

    def render(self) -> None:
        """Build and display the growth-progression animation."""
        animation = self.build_animation()
        self.fig.tight_layout()
        plt.show()
        del animation

    @staticmethod
    def run() -> None:
        data = pd.DataFrame(
            {
                "day": list(range(0, 22, 3)),
                "height_cm": [2.0, 4.8, 8.1, 12.4, 17.0, 21.9, 26.5, 30.8],
            }
        )

        animator = GrowthProgressionAnimator(data, interval_ms=350)
        animator.render()


if __name__ == "__main__":
    GrowthProgressionAnimator.run()
