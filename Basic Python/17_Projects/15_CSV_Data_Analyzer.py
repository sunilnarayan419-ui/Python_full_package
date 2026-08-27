"""A professional CSV-analysis application built on the standard library.

Pipeline: CSVLoader -> DataValidator -> DataAnalyzer -> ReportGenerator,
composed by a thin Application/CLI layer.
"""

from __future__ import annotations

import csv
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path


class CSVAnalyzerError(Exception):
    """Base exception for CSV-analysis failures."""


class FileNotFoundCSVError(CSVAnalyzerError):
    """Raised when the requested CSV file does not exist."""


class EmptyCSVError(CSVAnalyzerError):
    """Raised when the CSV file has no data rows."""


class ColumnNotFoundError(CSVAnalyzerError):
    """Raised when a requested column is not present in the dataset."""


@dataclass(slots=True)
class Dataset:
    """An in-memory representation of a loaded, validated CSV dataset."""

    headers: list[str]
    rows: list[dict[str, str]]

    def column_values(self, column: str) -> list[str]:
        if column not in self.headers:
            raise ColumnNotFoundError(f"Column '{column}' not found in dataset.")
        return [row.get(column, "") for row in self.rows]

    def numeric_values(self, column: str) -> list[float]:
        values = []
        for raw in self.column_values(column):
            if raw is None or raw.strip() == "":
                continue
            try:
                values.append(float(raw))
            except ValueError:
                continue
        return values


@dataclass(slots=True, frozen=True)
class ColumnSummary:
    """Summary statistics for a single numeric column."""

    column: str
    count: int
    mean: float
    median: float
    minimum: float
    maximum: float
    std_dev: float


class CSVLoader:
    """Loads CSV files from disk into an in-memory Dataset."""

    @staticmethod
    def load(path: Path) -> Dataset:
        if not path.exists():
            raise FileNotFoundCSVError(f"File not found: {path}")
        try:
            with path.open(newline="", encoding="utf-8") as handle:
                reader = csv.DictReader(handle)
                headers = reader.fieldnames or []
                rows = [dict(row) for row in reader]
        except (OSError, csv.Error) as exc:
            raise CSVAnalyzerError(f"Failed to read CSV file: {exc}") from exc

        if not rows:
            raise EmptyCSVError("CSV file contains no data rows.")
        return Dataset(headers=list(headers), rows=rows)


class DataValidator:
    """Validates a loaded dataset for structural consistency."""

    @staticmethod
    def validate(dataset: Dataset) -> list[str]:
        """Return a list of human-readable validation warnings (non-fatal)."""
        warnings: list[str] = []
        for column in dataset.headers:
            missing_count = sum(
                1 for row in dataset.rows if not row.get(column, "").strip()
            )
            if missing_count:
                warnings.append(f"Column '{column}' has {missing_count} missing value(s).")

        expected_width = len(dataset.headers)
        malformed_rows = sum(1 for row in dataset.rows if len(row) != expected_width)
        if malformed_rows:
            warnings.append(f"{malformed_rows} row(s) have a different number of fields than the header.")
        return warnings

    @staticmethod
    def detect_numeric_columns(dataset: Dataset) -> list[str]:
        numeric_columns = []
        for column in dataset.headers:
            values = dataset.column_values(column)
            non_empty = [v for v in values if v.strip()]
            if not non_empty:
                continue
            if all(_is_number(v) for v in non_empty):
                numeric_columns.append(column)
        return numeric_columns


def _is_number(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False


class DataAnalyzer:
    """Computes statistics, filters, sorts, and groups dataset rows."""

    def summarize_column(self, dataset: Dataset, column: str) -> ColumnSummary:
        values = dataset.numeric_values(column)
        if not values:
            raise CSVAnalyzerError(f"Column '{column}' has no numeric data to summarize.")
        return ColumnSummary(
            column=column,
            count=len(values),
            mean=statistics.mean(values),
            median=statistics.median(values),
            minimum=min(values),
            maximum=max(values),
            std_dev=statistics.pstdev(values) if len(values) > 1 else 0.0,
        )

    def filter_rows(self, dataset: Dataset, column: str, predicate) -> list[dict[str, str]]:
        return [row for row in dataset.rows if predicate(row.get(column, ""))]

    def sort_rows(
        self, dataset: Dataset, column: str, numeric: bool = False, descending: bool = False
    ) -> list[dict[str, str]]:
        if column not in dataset.headers:
            raise ColumnNotFoundError(f"Column '{column}' not found in dataset.")

        def _key(row: dict[str, str]):
            value = row.get(column, "")
            if numeric:
                try:
                    return float(value)
                except ValueError:
                    return float("-inf")
            return value

        return sorted(dataset.rows, key=_key, reverse=descending)

    def group_by(self, dataset: Dataset, column: str) -> dict[str, list[dict[str, str]]]:
        groups: dict[str, list[dict[str, str]]] = defaultdict(list)
        for row in dataset.rows:
            groups[row.get(column, "")].append(row)
        return dict(groups)

    def value_counts(self, dataset: Dataset, column: str) -> Counter[str]:
        return Counter(dataset.column_values(column))


class ReportGenerator:
    """Formats analysis results into human-readable reports."""

    @staticmethod
    def dataset_overview(dataset: Dataset, warnings: list[str], numeric_columns: list[str]) -> str:
        lines = [
            "=== Dataset Overview ===",
            f"Rows: {len(dataset.rows)}",
            f"Columns: {', '.join(dataset.headers)}",
            f"Numeric columns: {', '.join(numeric_columns) if numeric_columns else 'none'}",
        ]
        if warnings:
            lines.append("\nValidation warnings:")
            lines.extend(f"  - {w}" for w in warnings)
        return "\n".join(lines)

    @staticmethod
    def column_summary_report(summary: ColumnSummary) -> str:
        return (
            f"=== Summary: {summary.column} ===\n"
            f"Count:  {summary.count}\n"
            f"Mean:   {summary.mean:.2f}\n"
            f"Median: {summary.median:.2f}\n"
            f"Min:    {summary.minimum:.2f}\n"
            f"Max:    {summary.maximum:.2f}\n"
            f"StdDev: {summary.std_dev:.2f}"
        )

    @staticmethod
    def value_counts_report(counts: Counter[str], top_n: int = 10) -> str:
        lines = ["=== Value Counts ==="]
        for value, count in counts.most_common(top_n):
            lines.append(f"  {value}: {count}")
        return "\n".join(lines)


def _print_menu() -> None:
    print("\n================================")
    print("       CSV DATA ANALYZER")
    print("================================")
    print("1. Load and inspect a CSV file")
    print("2. Summarize a numeric column")
    print("3. Value counts for a column")
    print("4. Sort rows by a column")
    print("5. Group rows by a column")
    print("0. Exit")


def _load_dataset() -> Dataset | None:
    raw_path = input("CSV file path: ").strip()
    try:
        dataset = CSVLoader.load(Path(raw_path).expanduser())
        warnings = DataValidator.validate(dataset)
        numeric_columns = DataValidator.detect_numeric_columns(dataset)
        print("\n" + ReportGenerator.dataset_overview(dataset, warnings, numeric_columns))
        return dataset
    except CSVAnalyzerError as exc:
        print(f"Error: {exc}")
        return None


def _handle_summary(dataset: Dataset, analyzer: DataAnalyzer) -> None:
    column = input("Column name: ").strip()
    try:
        summary = analyzer.summarize_column(dataset, column)
        print("\n" + ReportGenerator.column_summary_report(summary))
    except CSVAnalyzerError as exc:
        print(f"Error: {exc}")


def _handle_value_counts(dataset: Dataset, analyzer: DataAnalyzer) -> None:
    column = input("Column name: ").strip()
    try:
        counts = analyzer.value_counts(dataset, column)
        print("\n" + ReportGenerator.value_counts_report(counts))
    except CSVAnalyzerError as exc:
        print(f"Error: {exc}")


def _handle_sort(dataset: Dataset, analyzer: DataAnalyzer) -> None:
    column = input("Column name: ").strip()
    numeric = input("Numeric sort? (y/N): ").strip().lower() == "y"
    descending = input("Descending? (y/N): ").strip().lower() == "y"
    try:
        rows = analyzer.sort_rows(dataset, column, numeric=numeric, descending=descending)
        for row in rows[:20]:
            print(row)
        if len(rows) > 20:
            print(f"... and {len(rows) - 20} more row(s).")
    except CSVAnalyzerError as exc:
        print(f"Error: {exc}")


def _handle_group(dataset: Dataset, analyzer: DataAnalyzer) -> None:
    column = input("Column name: ").strip()
    try:
        groups = analyzer.group_by(dataset, column)
    except CSVAnalyzerError as exc:
        print(f"Error: {exc}")
        return
    for key, rows in groups.items():
        print(f"{key}: {len(rows)} row(s)")


def main() -> None:
    """Entry point for the interactive CSV analyzer CLI."""
    analyzer = DataAnalyzer()
    dataset: Dataset | None = None

    while True:
        _print_menu()
        choice = input("Select an option: ").strip()

        if choice == "0":
            print("Goodbye.")
            break
        elif choice == "1":
            dataset = _load_dataset()
        elif dataset is None:
            print("Please load a CSV file first (option 1).")
        elif choice == "2":
            _handle_summary(dataset, analyzer)
        elif choice == "3":
            _handle_value_counts(dataset, analyzer)
        elif choice == "4":
            _handle_sort(dataset, analyzer)
        elif choice == "5":
            _handle_group(dataset, analyzer)
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
