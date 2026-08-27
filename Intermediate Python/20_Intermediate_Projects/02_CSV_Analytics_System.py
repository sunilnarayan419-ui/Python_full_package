from __future__ import annotations

import io
import logging
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

EXPECTED_SCHEMA: dict[str, str] = {
    "order_id": "object",
    "customer_id": "object",
    "product": "object",
    "category": "object",
    "quantity": "int64",
    "unit_price": "float64",
    "order_date": "object",
}


class CSVAnalyticsError(Exception):
    """Base error for CSV analytics failures."""


class SchemaValidationError(CSVAnalyticsError):
    """Raised when a CSV file does not match the expected schema."""


class DataQualityError(CSVAnalyticsError):
    """Raised when a CSV file contains malformed values that cannot be recovered."""


@dataclass(frozen=True, slots=True)
class NumericSummary:
    column: str
    count: int
    mean: float
    std: float
    minimum: float
    maximum: float


@dataclass(frozen=True, slots=True)
class CategoricalSummary:
    column: str
    unique_values: int
    top_value: str
    top_frequency: int


@dataclass(frozen=True, slots=True)
class AnalyticsReport:
    row_count: int
    missing_value_counts: dict[str, int]
    numeric_summaries: list[NumericSummary]
    categorical_summaries: list[CategoricalSummary]
    revenue_by_category: pd.DataFrame = field(repr=False)


class CSVLoader:
    """Loads and schema-validates CSV data from a path or in-memory buffer."""

    def __init__(self, expected_schema: dict[str, str] = EXPECTED_SCHEMA) -> None:
        self._expected_schema = expected_schema

    def load_from_path(self, path: Path) -> pd.DataFrame:
        if not path.exists():
            raise FileNotFoundError(f"CSV file not found: {path}")
        try:
            df = pd.read_csv(path)
        except pd.errors.ParserError as exc:
            raise CSVAnalyticsError(f"Malformed CSV file: {path}") from exc
        except pd.errors.EmptyDataError as exc:
            raise CSVAnalyticsError(f"CSV file is empty: {path}") from exc
        return self._validate_schema(df)

    def load_from_buffer(self, buffer: io.StringIO) -> pd.DataFrame:
        try:
            df = pd.read_csv(buffer)
        except pd.errors.ParserError as exc:
            raise CSVAnalyticsError("Malformed CSV content in buffer.") from exc
        return self._validate_schema(df)

    def _validate_schema(self, df: pd.DataFrame) -> pd.DataFrame:
        missing = [col for col in self._expected_schema if col not in df.columns]
        if missing:
            raise SchemaValidationError(f"Missing required columns: {', '.join(missing)}")
        return df


class DataCleaner:
    """Cleans a validated CSV dataframe."""

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        cleaned = df.copy()
        cleaned["quantity"] = pd.to_numeric(cleaned["quantity"], errors="coerce")
        cleaned["unit_price"] = pd.to_numeric(cleaned["unit_price"], errors="coerce")
        cleaned["order_date"] = pd.to_datetime(cleaned["order_date"], errors="coerce")

        invalid_rows = cleaned["quantity"].isna() | cleaned["unit_price"].isna()
        if invalid_rows.any():
            logger.warning("Dropping %d rows with malformed numeric values.", int(invalid_rows.sum()))
            cleaned = cleaned.loc[~invalid_rows]

        cleaned["quantity"] = cleaned["quantity"].astype("int64")
        return cleaned.reset_index(drop=True)


class CSVAnalyticsEngine:
    """Computes summaries, filters, and grouped analyses on cleaned CSV data."""

    NUMERIC_COLUMNS: tuple[str, ...] = ("quantity", "unit_price")
    CATEGORICAL_COLUMNS: tuple[str, ...] = ("category", "product")

    def missing_value_counts(self, df: pd.DataFrame) -> dict[str, int]:
        return {col: int(count) for col, count in df.isna().sum().items() if count > 0}

    def numeric_summaries(self, df: pd.DataFrame) -> list[NumericSummary]:
        summaries: list[NumericSummary] = []
        for col in self.NUMERIC_COLUMNS:
            series = df[col].dropna()
            summaries.append(
                NumericSummary(
                    column=col,
                    count=int(series.count()),
                    mean=round(float(series.mean()), 2),
                    std=round(float(series.std(ddof=1)) if series.count() > 1 else 0.0, 2),
                    minimum=round(float(series.min()), 2),
                    maximum=round(float(series.max()), 2),
                )
            )
        return summaries

    def categorical_summaries(self, df: pd.DataFrame) -> list[CategoricalSummary]:
        summaries: list[CategoricalSummary] = []
        for col in self.CATEGORICAL_COLUMNS:
            counts = df[col].value_counts()
            if counts.empty:
                continue
            summaries.append(
                CategoricalSummary(
                    column=col,
                    unique_values=int(df[col].nunique()),
                    top_value=str(counts.index[0]),
                    top_frequency=int(counts.iloc[0]),
                )
            )
        return summaries

    def filter_by_category(self, df: pd.DataFrame, category: str) -> pd.DataFrame:
        return df.loc[df["category"] == category].reset_index(drop=True)

    def revenue_by_category(self, df: pd.DataFrame) -> pd.DataFrame:
        working = df.copy()
        working["revenue"] = working["quantity"] * working["unit_price"]
        return (
            working.groupby("category")["revenue"]
            .sum()
            .round(2)
            .sort_values(ascending=False)
            .reset_index()
        )

    def build_report(self, df: pd.DataFrame) -> AnalyticsReport:
        return AnalyticsReport(
            row_count=len(df),
            missing_value_counts=self.missing_value_counts(df),
            numeric_summaries=self.numeric_summaries(df),
            categorical_summaries=self.categorical_summaries(df),
            revenue_by_category=self.revenue_by_category(df),
        )


class CSVAnalyticsSystem:
    """High-level orchestrator combining loading, cleaning, and analysis."""

    def __init__(
        self,
        loader: CSVLoader | None = None,
        cleaner: DataCleaner | None = None,
        engine: CSVAnalyticsEngine | None = None,
    ) -> None:
        self._loader = loader or CSVLoader()
        self._cleaner = cleaner or DataCleaner()
        self._engine = engine or CSVAnalyticsEngine()

    def analyze_path(self, path: Path) -> AnalyticsReport:
        raw_df = self._loader.load_from_path(path)
        cleaned_df = self._cleaner.clean(raw_df)
        return self._engine.build_report(cleaned_df)

    def analyze_buffer(self, buffer: io.StringIO) -> AnalyticsReport:
        raw_df = self._loader.load_from_buffer(buffer)
        cleaned_df = self._cleaner.clean(raw_df)
        return self._engine.build_report(cleaned_df)


def _build_sample_csv() -> io.StringIO:
    """Builds a deterministic in-memory CSV sample for demonstration purposes."""
    csv_content = """order_id,customer_id,product,category,quantity,unit_price,order_date
O1001,C001,Beaker 500ml,Labware,10,4.50,2024-01-05
O1002,C002,Centrifuge Tube,Labware,100,0.25,2024-01-06
O1003,C003,PCR Kit,Reagents,5,89.99,2024-01-07
O1004,C001,Pipette Tips,Labware,200,0.05,2024-01-08
O1005,C004,DNA Ladder,Reagents,3,45.00,2024-01-09
O1006,C005,Beaker 500ml,Labware,invalid,4.50,2024-01-10
O1007,C002,Agarose Powder,Reagents,2,32.00,2024-01-11
"""
    return io.StringIO(csv_content)


def run() -> AnalyticsReport:
    """Runs the CSV analytics system against a controlled sample dataset."""
    system = CSVAnalyticsSystem()
    buffer = _build_sample_csv()
    report = system.analyze_buffer(buffer)

    logger.info("Row count: %d", report.row_count)
    logger.info("Missing values: %s", report.missing_value_counts)
    for summary in report.numeric_summaries:
        logger.info("Numeric summary: %s", summary)
    for summary in report.categorical_summaries:
        logger.info("Categorical summary: %s", summary)
    logger.info("Revenue by category:\n%s", report.revenue_by_category.to_string(index=False))

    return report


if __name__ == "__main__":
    run()
