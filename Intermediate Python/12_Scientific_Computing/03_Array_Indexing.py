"""
03_Array_Indexing.py

Production-oriented NumPy indexing patterns applied to a gene-expression
matrix (rows = genes, columns = samples), a standard bioinformatics data
layout.
"""

from __future__ import annotations

import logging

import numpy as np

logger = logging.getLogger(__name__)


class ScientificInputError(ValueError):
    """Raised when scientific input data is invalid."""


GENE_IDS = np.array(["TP53", "BRCA1", "EGFR", "MYC", "KRAS", "PTEN"])
SAMPLE_IDS = np.array(["ctrl_1", "ctrl_2", "treat_1", "treat_2", "treat_3"])


def load_expression_matrix() -> np.ndarray:
    """
    Return a (n_genes, n_samples) float64 log2-normalized expression matrix.
    """
    rng = np.random.default_rng(seed=42)
    baseline = rng.normal(loc=6.0, scale=1.0, size=(GENE_IDS.size, SAMPLE_IDS.size))
    # Simulate an upregulation effect in treated samples for two genes.
    baseline[0, 2:] += 2.5  # TP53 upregulated under treatment
    baseline[3, 2:] += 1.8  # MYC upregulated under treatment
    return baseline


def validate_matrix(matrix: np.ndarray) -> None:
    if matrix.ndim != 2:
        raise ScientificInputError(f"Expected 2D expression matrix; got ndim={matrix.ndim}")
    if matrix.shape != (GENE_IDS.size, SAMPLE_IDS.size):
        raise ScientificInputError(
            f"Expected shape {(GENE_IDS.size, SAMPLE_IDS.size)}; got {matrix.shape}"
        )
    if not np.isfinite(matrix).all():
        raise ScientificInputError("Expression matrix contains non-finite values")


def select_gene_row(matrix: np.ndarray, gene: str) -> np.ndarray:
    """
    Basic indexing: select all sample values for one gene.

    This returns a VIEW into the original matrix (no copy), since it is a
    simple row selection via a single integer index. Mutating the result
    would mutate `matrix`.
    """
    validate_matrix(matrix)
    idx = np.where(GENE_IDS == gene)[0]
    if idx.size == 0:
        raise ScientificInputError(f"Unknown gene id: {gene!r}")
    return matrix[idx[0]]


def select_treated_samples(matrix: np.ndarray) -> np.ndarray:
    """
    Slicing: select the treated-sample columns (all genes).

    Basic slices like this also return a view, not a copy.
    """
    validate_matrix(matrix)
    treated_mask = np.char.startswith(SAMPLE_IDS, "treat")
    treated_cols = np.where(treated_mask)[0]
    # Contiguous slice in this dataset layout -> view.
    return matrix[:, treated_cols[0] : treated_cols[-1] + 1]


def select_multiple_genes(matrix: np.ndarray, genes: list[str]) -> np.ndarray:
    """
    Fancy indexing: select an arbitrary, non-contiguous subset of gene rows.

    Fancy indexing (indexing with an array/list of indices) ALWAYS returns a
    COPY, not a view -- important for memory reasoning and for safely
    mutating the subset without affecting the source matrix.
    """
    validate_matrix(matrix)
    gene_to_idx = {g: i for i, g in enumerate(GENE_IDS)}
    missing = [g for g in genes if g not in gene_to_idx]
    if missing:
        raise ScientificInputError(f"Unknown gene ids: {missing}")
    idx = np.array([gene_to_idx[g] for g in genes])
    return matrix[idx]


def genes_above_threshold(matrix: np.ndarray, log2_threshold: float) -> np.ndarray:
    """
    Boolean masking: identify genes whose mean expression across all samples
    exceeds a log2 threshold. Boolean-indexed results are copies.
    """
    validate_matrix(matrix)
    gene_means = matrix.mean(axis=1)
    mask = gene_means > log2_threshold
    return GENE_IDS[mask]


def differential_expression_mask(
    matrix: np.ndarray, log2_fold_change_threshold: float
) -> np.ndarray:
    """
    Conditional scientific filtering: identify genes with a large mean
    difference between control and treated samples (simple fold-change proxy
    on log2 data, i.e. a difference of means in log space).
    """
    validate_matrix(matrix)
    control_cols = np.char.startswith(SAMPLE_IDS, "ctrl")
    treated_cols = np.char.startswith(SAMPLE_IDS, "treat")

    control_mean = matrix[:, control_cols].mean(axis=1)
    treated_mean = matrix[:, treated_cols].mean(axis=1)
    log2_fc = treated_mean - control_mean

    return GENE_IDS[np.abs(log2_fc) >= log2_fold_change_threshold]


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    matrix = load_expression_matrix()
    logger.info("Expression matrix shape=%s", matrix.shape)

    tp53_row = select_gene_row(matrix, "TP53")
    print("TP53 expression across samples:", np.round(tp53_row, 3))

    treated = select_treated_samples(matrix)
    print("Treated-sample submatrix shape:", treated.shape)

    subset = select_multiple_genes(matrix, ["EGFR", "MYC", "PTEN"])
    print("Fancy-indexed gene subset shape (copy):", subset.shape)

    high_expr = genes_above_threshold(matrix, log2_threshold=6.5)
    print("Genes with mean expression > 6.5:", high_expr)

    de_genes = differential_expression_mask(matrix, log2_fold_change_threshold=1.0)
    print("Differentially expressed genes (|log2FC| >= 1.0):", de_genes)


if __name__ == "__main__":
    main()
