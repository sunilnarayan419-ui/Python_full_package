from __future__ import annotations

import numpy as np
import pandas as pd

_MOCK_EXPRESSION_ROWS: list[dict[str, object]] = [
    {"gene_id": "ENSG00000141510", "sample_id": "S01", "condition": "tumor", "expression_value": 8.42, "chromosome": "17"},
    {"gene_id": "ENSG00000141510", "sample_id": "S02", "condition": "tumor", "expression_value": 7.95, "chromosome": "17"},
    {"gene_id": "ENSG00000141510", "sample_id": "S03", "condition": "normal", "expression_value": 4.10, "chromosome": "17"},
    {"gene_id": "ENSG00000141510", "sample_id": "S04", "condition": "normal", "expression_value": 3.88, "chromosome": "17"},
    {"gene_id": "ENSG00000012048", "sample_id": "S01", "condition": "tumor", "expression_value": 5.21, "chromosome": "17"},
    {"gene_id": "ENSG00000012048", "sample_id": "S02", "condition": "tumor", "expression_value": 5.60, "chromosome": "17"},
    {"gene_id": "ENSG00000012048", "sample_id": "S03", "condition": "normal", "expression_value": 6.02, "chromosome": "17"},
    {"gene_id": "ENSG00000012048", "sample_id": "S04", "condition": "normal", "expression_value": -1.00, "chromosome": "17"},
    {"gene_id": "ENSG00000139618", "sample_id": "S01", "condition": "tumor", "expression_value": 2.75, "chromosome": "13"},
    {"gene_id": "ENSG00000139618", "sample_id": "S02", "condition": "tumor", "expression_value": np.nan, "chromosome": "13"},
]

_MOCK_VARIANT_ROWS: list[dict[str, object]] = [
    {"gene_id": "ENSG00000141510", "chromosome": "17", "position": 7674220, "ref_allele": "C", "alt_allele": "T"},
    {"gene_id": "ENSG00000141510", "chromosome": "17", "position": 7674230, "ref_allele": "G", "alt_allele": "A"},
    {"gene_id": "ENSG00000012048", "chromosome": "17", "position": 41244936, "ref_allele": "A", "alt_allele": "G"},
    {"gene_id": "ENSG00000139618", "chromosome": "13", "position": 32340301, "ref_allele": "T", "alt_allele": "C"},
]


class MolecularDataWorkflow:
    """Industry-level molecular data processing workflow using pandas/numpy.

    Handles gene-expression and variant tables with validation,
    normalization, filtering, aggregation, and summary statistics
    typical of an early-stage pharma target-discovery pipeline.
    """

    def __init__(self, expression_rows: list[dict[str, object]], variant_rows: list[dict[str, object]]) -> None:
        """Initialize with raw expression and variant record lists.

        Args:
            expression_rows: Rows with gene_id, sample_id, condition,
                expression_value, chromosome.
            variant_rows: Rows with gene_id, chromosome, position,
                ref_allele, alt_allele.
        """
        self.expression_df: pd.DataFrame = pd.DataFrame(expression_rows)
        self.variant_df: pd.DataFrame = pd.DataFrame(variant_rows)
        self._validate_schema()

    def _validate_schema(self) -> None:
        """Validate that required columns are present in both tables."""
        required_expression = {"gene_id", "sample_id", "condition", "expression_value", "chromosome"}
        required_variant = {"gene_id", "chromosome", "position", "ref_allele", "alt_allele"}
        missing_expression = required_expression - set(self.expression_df.columns)
        missing_variant = required_variant - set(self.variant_df.columns)
        if missing_expression:
            raise ValueError(f"Expression table missing columns: {missing_expression}")
        if missing_variant:
            raise ValueError(f"Variant table missing columns: {missing_variant}")

    def clean_expression_data(self) -> pd.DataFrame:
        """Remove invalid expression values (negative or NaN) from the table.

        Negative expression_value entries are treated as instrument/pipeline
        artifacts and are dropped along with missing measurements.
        """
        cleaned = self.expression_df.copy()
        cleaned = cleaned.dropna(subset=["expression_value"])
        cleaned = cleaned[cleaned["expression_value"] >= 0]
        return cleaned.reset_index(drop=True)

    def normalize_expression(self, method: str = "zscore") -> pd.DataFrame:
        """Normalize expression values per gene across samples.

        Args:
            method: Normalization strategy, currently "zscore" (per-gene
                mean-centered, unit-variance) is supported.
        """
        if method != "zscore":
            raise ValueError(f"Unsupported normalization method: {method}")

        cleaned = self.clean_expression_data()

        def _zscore(group: pd.Series) -> pd.Series:
            std = group.std(ddof=0)
            if std == 0 or np.isnan(std):
                return group * 0.0
            return (group - group.mean()) / std

        cleaned["normalized_value"] = cleaned.groupby("gene_id")["expression_value"].transform(_zscore)
        return cleaned

    def filter_by_condition(self, condition: str) -> pd.DataFrame:
        """Filter cleaned expression rows to a single experimental condition.

        Args:
            condition: Condition label to keep (e.g. "tumor", "normal").
        """
        cleaned = self.clean_expression_data()
        return cleaned[cleaned["condition"] == condition].reset_index(drop=True)

    def aggregate_by_gene(self) -> pd.DataFrame:
        """Aggregate mean/std expression per gene and condition."""
        cleaned = self.clean_expression_data()
        aggregated = (
            cleaned.groupby(["gene_id", "condition"])["expression_value"]
            .agg(mean_expression="mean", std_expression="std", sample_count="count")
            .reset_index()
        )
        return aggregated

    def variant_density_per_gene(self) -> pd.DataFrame:
        """Compute the number of catalogued variants per gene."""
        return (
            self.variant_df.groupby("gene_id")
            .size()
            .reset_index(name="variant_count")
            .sort_values("variant_count", ascending=False)
            .reset_index(drop=True)
        )

    def summary_statistics(self) -> dict[str, float | int]:
        """Compute dataset-level summary statistics across cleaned expression data."""
        cleaned = self.clean_expression_data()
        return {
            "total_measurements": int(len(cleaned)),
            "unique_genes": int(cleaned["gene_id"].nunique()),
            "unique_samples": int(cleaned["sample_id"].nunique()),
            "mean_expression": round(float(cleaned["expression_value"].mean()), 3),
            "median_expression": round(float(cleaned["expression_value"].median()), 3),
        }

    @staticmethod
    def run() -> None:
        """Demonstrate cleaning, normalization, aggregation, and summarization."""
        workflow = MolecularDataWorkflow(_MOCK_EXPRESSION_ROWS, _MOCK_VARIANT_ROWS)

        cleaned = workflow.clean_expression_data()
        print(f"Cleaned expression rows: {len(cleaned)} / {len(workflow.expression_df)} original")

        normalized = workflow.normalize_expression()
        print("Normalized expression preview:")
        print(normalized[["gene_id", "sample_id", "expression_value", "normalized_value"]])

        tumor_only = workflow.filter_by_condition("tumor")
        print(f"Tumor-condition rows: {len(tumor_only)}")

        aggregated = workflow.aggregate_by_gene()
        print("Per-gene/condition aggregation:")
        print(aggregated)

        variant_density = workflow.variant_density_per_gene()
        print("Variant density per gene:")
        print(variant_density)

        print("Summary statistics:", workflow.summary_statistics())


if __name__ == "__main__":
    MolecularDataWorkflow.run()
