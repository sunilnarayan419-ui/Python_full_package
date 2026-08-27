from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import date, timedelta

import numpy as np
import pandas as pd
import streamlit as st

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")


class DashboardDataError(Exception):
    """Raised when dashboard input data fails validation."""


@dataclass(frozen=True, slots=True)
class DashboardFilters:
    species: str
    treatment: str
    date_range: tuple[date, date]


class ExperimentDataProvider:
    """Generates and validates deterministic experimental data for the dashboard."""

    REQUIRED_COLUMNS = ("date", "species", "treatment", "growth_rate", "biomass_g", "leaf_count")

    def load(self) -> pd.DataFrame:
        rng = np.random.default_rng(7)
        species_options = ["Arabidopsis thaliana", "Zea mays", "Glycine max"]
        treatment_options = ["control", "drought", "high_nitrogen"]

        start = date(2024, 1, 1)
        rows = []
        for day_offset in range(90):
            current_date = start + timedelta(days=day_offset)
            for species in species_options:
                for treatment in treatment_options:
                    rows.append(
                        {
                            "date": current_date,
                            "species": species,
                            "treatment": treatment,
                            "growth_rate": round(float(rng.normal(1.2, 0.3)), 3),
                            "biomass_g": round(float(rng.normal(10, 2.5)), 2),
                            "leaf_count": int(rng.integers(4, 22)),
                        }
                    )
        df = pd.DataFrame(rows)
        self._validate(df)
        return df

    def _validate(self, df: pd.DataFrame) -> None:
        missing = [col for col in self.REQUIRED_COLUMNS if col not in df.columns]
        if missing:
            raise DashboardDataError(f"Dataset missing required columns: {missing}")


class DashboardDataProcessor:
    """Applies filters and computes summary metrics, independent of UI code."""

    def apply_filters(self, df: pd.DataFrame, filters: DashboardFilters) -> pd.DataFrame:
        mask = (
            (df["species"] == filters.species)
            & (df["treatment"] == filters.treatment)
            & (df["date"] >= filters.date_range[0])
            & (df["date"] <= filters.date_range[1])
        )
        return df.loc[mask].sort_values("date").reset_index(drop=True)

    def summary_metrics(self, df: pd.DataFrame) -> dict[str, float]:
        if df.empty:
            return {"mean_growth_rate": 0.0, "mean_biomass_g": 0.0, "mean_leaf_count": 0.0}
        return {
            "mean_growth_rate": round(float(df["growth_rate"].mean()), 3),
            "mean_biomass_g": round(float(df["biomass_g"].mean()), 2),
            "mean_leaf_count": round(float(df["leaf_count"].mean()), 1),
        }

    def daily_time_series(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.groupby("date", as_index=False)["biomass_g"].mean()

    def grouped_by_treatment(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.groupby("treatment", as_index=False)["growth_rate"].mean()


def render_dashboard() -> None:
    """Renders the Streamlit dashboard UI, delegating computation to the processor."""
    st.set_page_config(page_title="Plant Experiment Dashboard", layout="wide")
    st.title("Plant Experiment Monitoring Dashboard")

    provider = ExperimentDataProvider()
    processor = DashboardDataProcessor()

    try:
        raw_df = provider.load()
    except DashboardDataError as exc:
        st.error(f"Failed to load dataset: {exc}")
        return

    with st.sidebar:
        st.header("Filters")
        species = st.selectbox("Species", sorted(raw_df["species"].unique()))
        treatment = st.selectbox("Treatment", sorted(raw_df["treatment"].unique()))
        min_date, max_date = raw_df["date"].min(), raw_df["date"].max()
        start_date, end_date = st.date_input("Date range", value=(min_date, max_date))

    filters = DashboardFilters(species=species, treatment=treatment, date_range=(start_date, end_date))
    filtered_df = processor.apply_filters(raw_df, filters)

    metrics = processor.summary_metrics(filtered_df)
    col1, col2, col3 = st.columns(3)
    col1.metric("Mean Growth Rate", metrics["mean_growth_rate"])
    col2.metric("Mean Biomass (g)", metrics["mean_biomass_g"])
    col3.metric("Mean Leaf Count", metrics["mean_leaf_count"])

    st.subheader("Biomass Over Time")
    st.line_chart(processor.daily_time_series(filtered_df).set_index("date"))

    st.subheader("Mean Growth Rate by Treatment (All Species)")
    st.bar_chart(processor.grouped_by_treatment(raw_df).set_index("treatment"))

    st.subheader("Biomass vs. Leaf Count")
    st.scatter_chart(filtered_df, x="leaf_count", y="biomass_g")

    st.subheader("Growth Rate Distribution")
    st.bar_chart(filtered_df["growth_rate"].value_counts(bins=10).sort_index())


def run() -> None:
    """Entry point for `streamlit run 09_Data_Visualization_Dashboard.py`."""
    render_dashboard()


if __name__ == "__main__":
    run()
