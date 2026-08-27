from __future__ import annotations

from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool, Legend
from bokeh.palettes import Category10
from bokeh.layouts import column
import pandas as pd


class RootBiomassInteractiveVisualizer:
    """Builds an interactive Bokeh visualization of root length vs. biomass by species."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data.copy()

    def build_data_source(self, species: str) -> ColumnDataSource:
        """Return a ColumnDataSource filtered to a single species."""
        subset = self.data[self.data["species"] == species]
        return ColumnDataSource(subset)

    def build_scatter_figure(self):
        """Construct the Bokeh figure with hover tooltips, legend, and scientific axis labels."""
        plot = figure(
            title="Root Length vs. Biomass by Species",
            x_axis_label="Root Length (cm)",
            y_axis_label="Biomass (g)",
            width=800,
            height=500,
            tools="pan,wheel_zoom,box_zoom,reset,save",
        )

        hover = HoverTool(
            tooltips=[
                ("Sample", "@sample_id"),
                ("Root Length", "@root_length_cm cm"),
                ("Biomass", "@biomass_g g"),
                ("Species", "@species"),
            ]
        )
        plot.add_tools(hover)

        species_list = sorted(self.data["species"].unique())
        colors = Category10[max(3, len(species_list))]

        legend_items = []
        for idx, species in enumerate(species_list):
            source = self.build_data_source(species)
            renderer = plot.scatter(
                "root_length_cm",
                "biomass_g",
                source=source,
                size=10,
                color=colors[idx],
                alpha=0.75,
            )
            legend_items.append((species, [renderer]))

        legend = Legend(items=legend_items, title="Species")
        plot.add_layout(legend, "right")
        plot.legend.click_policy = "hide"

        return plot

    def render(self) -> None:
        """Assemble and display the interactive Bokeh visualization."""
        plot = self.build_scatter_figure()
        show(column(plot))

    @staticmethod
    def run() -> None:
        data = pd.DataFrame(
            [
                {"sample_id": "S001", "species": "Oryza sativa", "root_length_cm": 12.4, "biomass_g": 5.2},
                {"sample_id": "S002", "species": "Oryza sativa", "root_length_cm": 14.1, "biomass_g": 6.0},
                {"sample_id": "S003", "species": "Oryza sativa", "root_length_cm": 10.8, "biomass_g": 4.5},
                {"sample_id": "S004", "species": "Zea mays", "root_length_cm": 22.6, "biomass_g": 14.1},
                {"sample_id": "S005", "species": "Zea mays", "root_length_cm": 25.3, "biomass_g": 16.9},
                {"sample_id": "S006", "species": "Zea mays", "root_length_cm": 20.1, "biomass_g": 12.8},
                {"sample_id": "S007", "species": "Glycine max", "root_length_cm": 17.9, "biomass_g": 9.3},
                {"sample_id": "S008", "species": "Glycine max", "root_length_cm": 16.2, "biomass_g": 8.4},
                {"sample_id": "S009", "species": "Glycine max", "root_length_cm": 19.0, "biomass_g": 10.1},
            ]
        )

        visualizer = RootBiomassInteractiveVisualizer(data)
        visualizer.render()


if __name__ == "__main__":
    RootBiomassInteractiveVisualizer.run()
