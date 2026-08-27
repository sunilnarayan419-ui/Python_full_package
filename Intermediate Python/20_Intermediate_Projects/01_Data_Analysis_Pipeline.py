from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

REQUIRED_COLUMNS: tuple[str, ...] = (
    "sample_id",
    "species",
    "treatment",
    "height_cm",
    "leaf_count",
    "biomass_g",
    "soil_ph",
    "temperature_c",
    "measurement_date",
)

NUMERIC_COLUMNS: tuple[str, ...] = (
    "height_cm",
    "leaf_count",
    "biomass_g",
    "soil_ph",
    "temperature_c",
)

VALID_PH_RANGE: tuple[float, float] = (3.5, 9.5)
VALID_TEMPERATURE_RANGE: tuple[float, float] = (-5.0, 55.0)


class DataValidationError(Exception):
    """Raised when input data fails schema or domain validation."""


@dataclass(frozen=True, slots=True)
class ValidationReport:
    """Result of validating a raw dataset."""

    is_valid: bool
    missing_columns: tuple[str, ...] = field(default_factory=tuple)
    invalid_row_count: int = 0
    notes: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class AnalysisResult:
    """Structured output of the full pipeline run."""

    cleaned_row_count: int
    dropped_row_count: int
    group_summary: pd.DataFrame
    correlation_matrix: pd.DataFrame
    top_performers: pd.DataFrame


class DataValidator:
    """Validates raw experimental data against the expected schema."""

    def __init__(self, required_columns: tuple[str, ...] = REQUIRED_COLUMNS) -> None:
        self._required_columns = required_columns

    def validate(self, df: pd.DataFrame) -> ValidationReport:
        missing = tuple(col for col in self._required_columns if col not in df.columns)
        if missing:
            return ValidationReport(is_valid=False, missing_columns=missing)

        notes: list[str] = []
        invalid_mask = pd.Series(False, index=df.index)

        for col in NUMERIC_COLUMNS:
            non_numeric = pd.to_numeric(df[col], errors="coerce").isna() & df[col].notna()
            if non_numeric.any():
                notes.append(f"{non_numeric.sum()} non-numeric values found in '{col}'.")
                invalid_mask |= non_numeric

        ph_numeric = pd.to_numeric(df["soil_ph"], errors="coerce")
        out_of_range_ph = ph_numeric.notna() & ~ph_numeric.between(*VALID_PH_RANGE)
        if out_of_range_ph.any():
            notes.append(f"{out_of_range_ph.sum()} soil_ph values outside plausible range.")
            invalid_mask |= out_of_range_ph

        return ValidationReport(
            is_valid=True,
            invalid_row_count=int(invalid_mask.sum()),
            notes=tuple(notes),
        )


class DataCleaner:
    """Cleans and imputes missing or invalid values in the raw dataset."""

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        cleaned = df.copy()

        for col in NUMERIC_COLUMNS:
            cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")

        ph_valid = cleaned["soil_ph"].between(*VALID_PH_RANGE)
        cleaned.loc[~ph_valid, "soil_ph"] = np.nan

        temp_valid = cleaned["temperature_c"].between(*VALID_TEMPERATURE_RANGE)
        cleaned.loc[~temp_valid, "temperature_c"] = np.nan

        cleaned["measurement_date"] = pd.to_datetime(cleaned["measurement_date"], errors="coerce")

        group_cols = ["species", "treatment"]
        for col in NUMERIC_COLUMNS:
            cleaned[col] = cleaned.groupby(group_cols)[col].transform(
                lambda s: s.fillna(s.median())
            )
            cleaned[col] = cleaned[col].fillna(cleaned[col].median())

        essential = ["sample_id", "species", "treatment"]
        before = len(cleaned)
        cleaned = cleaned.dropna(subset=essential)
        dropped = before - len(cleaned)
        if dropped:
            logger.info("Dropped %d rows missing essential identifiers.", dropped)

        return cleaned.reset_index(drop=True)


class FeatureEngineer:
    """Derives analytical features from cleaned experimental data."""

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        enriched = df.copy()
        enriched["biomass_per_leaf"] = enriched["biomass_g"] / enriched["leaf_count"].replace(0, np.nan)
        enriched["height_biomass_ratio"] = enriched["height_cm"] / enriched["biomass_g"].replace(0, np.nan)
        enriched["biomass_per_leaf"] = enriched["biomass_per_leaf"].fillna(0.0)
        enriched["height_biomass_ratio"] = enriched["height_biomass_ratio"].fillna(0.0)
        return enriched


class GroupedAnalyzer:
    """Performs grouped statistical analysis on enriched experimental data."""

    def summarize(self, df: pd.DataFrame) -> pd.DataFrame:
        summary = (
            df.groupby(["species", "treatment"])
            .agg(
                sample_count=("sample_id", "count"),
                mean_height_cm=("height_cm", "mean"),
                mean_biomass_g=("biomass_g", "mean"),
                mean_leaf_count=("leaf_count", "mean"),
                mean_soil_ph=("soil_ph", "mean"),
            )
            .round(3)
            .reset_index()
        )
        return summary

    def correlations(self, df: pd.DataFrame) -> pd.DataFrame:
        return df[list(NUMERIC_COLUMNS)].corr().round(3)

    def top_performers(self, df: pd.DataFrame, metric: str = "biomass_g", n: int = 5) -> pd.DataFrame:
        return (
            df.sort_values(metric, ascending=False)
            .loc[:, ["sample_id", "species", "treatment", metric]]
            .head(n)
            .reset_index(drop=True)
        )


class DataAnalysisPipeline:
    """Coordinates validation, cleaning, feature engineering, and analysis."""

    def __init__(
        self,
        validator: DataValidator | None = None,
        cleaner: DataCleaner | None = None,
        engineer: FeatureEngineer | None = None,
        analyzer: GroupedAnalyzer | None = None,
    ) -> None:
        self._validator = validator or DataValidator()
        self._cleaner = cleaner or DataCleaner()
        self._engineer = engineer or FeatureEngineer()
        self._analyzer = analyzer or GroupedAnalyzer()

    def run(self, raw_df: pd.DataFrame) -> AnalysisResult:
        report = self._validator.validate(raw_df)
        if not report.is_valid:
            raise DataValidationError(
                f"Missing required columns: {', '.join(report.missing_columns)}"
            )
        for note in report.notes:
            logger.warning(note)

        cleaned = self._cleaner.clean(raw_df)
        dropped = len(raw_df) - len(cleaned)

        enriched = self._engineer.transform(cleaned)
        group_summary = self._analyzer.summarize(enriched)
        correlation_matrix = self._analyzer.correlations(enriched)
        top_performers = self._analyzer.top_performers(enriched)

        return AnalysisResult(
            cleaned_row_count=len(enriched),
            dropped_row_count=dropped,
            group_summary=group_summary,
            correlation_matrix=correlation_matrix,
            top_performers=top_performers,
        )


def _build_sample_dataset() -> pd.DataFrame:
    """Builds a deterministic sample plant-experiment dataset."""
    rng = np.random.default_rng(42)
    n = 60
    species = rng.choice(["Arabidopsis thaliana", "Zea mays", "Glycine max"], size=n)
    treatment = rng.choice(["control", "drought", "high_nitrogen"], size=n)

    data = {
        "sample_id": [f"S{i:04d}" for i in range(n)],
        "species": species,
        "treatment": treatment,
        "height_cm": rng.normal(35, 8, n).round(2),
        "leaf_count": rng.integers(4, 20, n),
        "biomass_g": rng.normal(12, 3, n).round(2),
        "soil_ph": rng.normal(6.5, 0.6, n).round(2),
        "temperature_c": rng.normal(22, 4, n).round(1),
        "measurement_date": [date(2024, 6, 1 + (i % 28)) for i in range(n)],
    }
    df = pd.DataFrame(data)
    df.loc[3, "soil_ph"] = 15.0
    df.loc[7, "height_cm"] = np.nan
    df["biomass_g"] = df["biomass_g"].astype(object)
    df.loc[10, "biomass_g"] = "invalid"
    return df


def run() -> AnalysisResult:
    """Runs the pipeline end-to-end on a deterministic sample dataset."""
    raw_df = _build_sample_dataset()
    pipeline = DataAnalysisPipeline()
    result = pipeline.run(raw_df)

    logger.info("Cleaned rows: %d (dropped %d)", result.cleaned_row_count, result.dropped_row_count)
    logger.info("Group summary:\n%s", result.group_summary.to_string(index=False))
    logger.info("Top performers:\n%s", result.top_performers.to_string(index=False))

    return result


if __name__ == "__main__":
    run()
