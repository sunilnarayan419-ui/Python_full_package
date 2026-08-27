from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


class GeneExpressionInteractiveVisualizer:
    """Builds interactive Plotly visualizations of gene expression across treatments."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data.copy()

    def build_expression_scatter(self) -> go.Figure:
        """Return an interactive scatter plot of gene expression vs. response."""
        fig = px.scatter(
            self.data,
            x="gene_expression",
            y="response_percent",
            color="treatment",
            symbol="treatment",
            hover_data=["sample_id", "gene_expression", "response_percent"],
            title="Gene Expression vs. Phenotypic Response",
            labels={
                "gene_expression": "Relative Gene Expression (fold change)",
                "response_percent": "Response (%)",
                "treatment": "Treatment",
            },
        )
        fig.update_traces(marker=dict(size=11, opacity=0.8, line=dict(width=1, color="white")))
        fig.update_layout(legend_title_text="Treatment", template="plotly_white")
        return fig

    def build_treatment_bar(self) -> go.Figure:
        """Return an interactive bar chart of mean expression per treatment group."""
        summary = self.data.groupby("treatment", as_index=False)["gene_expression"].mean()
        fig = px.bar(
            summary,
            x="treatment",
            y="gene_expression",
            title="Mean Gene Expression by Treatment",
            labels={"treatment": "Treatment", "gene_expression": "Mean Relative Expression"},
            color="treatment",
        )
        fig.update_layout(showlegend=False, template="plotly_white")
        return fig

    def build_expression_trend(self) -> go.Figure:
        """Return an interactive line chart of expression trend over experimental time points."""
        fig = go.Figure()
        for treatment, group in self.data.groupby("treatment"):
            trend = group.groupby("day", as_index=False)["gene_expression"].mean()
            fig.add_trace(
                go.Scatter(
                    x=trend["day"],
                    y=trend["gene_expression"],
                    mode="lines+markers",
                    name=treatment,
                    hovertemplate="Day %{x}<br>Expression: %{y:.2f}<extra>%{fullData.name}</extra>",
                )
            )

        fig.update_layout(
            title="Gene Expression Trend Over Time",
            xaxis_title="Day Since Treatment",
            yaxis_title="Relative Gene Expression",
            template="plotly_white",
            legend_title_text="Treatment",
        )
        return fig

    @staticmethod
    def run() -> None:
        data = pd.DataFrame(
            [
                {"sample_id": "S001", "day": 0, "treatment": "control", "gene_expression": 1.02, "response_percent": 4.1},
                {"sample_id": "S002", "day": 3, "treatment": "control", "gene_expression": 1.05, "response_percent": 5.0},
                {"sample_id": "S003", "day": 6, "treatment": "control", "gene_expression": 0.98, "response_percent": 4.6},
                {"sample_id": "S004", "day": 0, "treatment": "drought_stress", "gene_expression": 1.10, "response_percent": 6.2},
                {"sample_id": "S005", "day": 3, "treatment": "drought_stress", "gene_expression": 2.45, "response_percent": 28.4},
                {"sample_id": "S006", "day": 6, "treatment": "drought_stress", "gene_expression": 3.87, "response_percent": 51.9},
                {"sample_id": "S007", "day": 0, "treatment": "heat_stress", "gene_expression": 1.08, "response_percent": 5.9},
                {"sample_id": "S008", "day": 3, "treatment": "heat_stress", "gene_expression": 2.90, "response_percent": 33.7},
                {"sample_id": "S009", "day": 6, "treatment": "heat_stress", "gene_expression": 4.52, "response_percent": 60.3},
            ]
        )

        visualizer = GeneExpressionInteractiveVisualizer(data)

        scatter_fig = visualizer.build_expression_scatter()
        bar_fig = visualizer.build_treatment_bar()
        trend_fig = visualizer.build_expression_trend()

        scatter_fig.show()
        bar_fig.show()
        trend_fig.show()


if __name__ == "__main__":
    GeneExpressionInteractiveVisualizer.run()
