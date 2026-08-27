"""
16_Sparse_Matrices.py

Production-oriented sparse numerical computation for a biological
gene-interaction network and a sparse single-cell-style gene x cell count
matrix, using scipy.sparse formats chosen for their specific workload
strengths.
"""

from __future__ import annotations

import logging

import numpy as np
from scipy import sparse

logger = logging.getLogger(__name__)


class ScientificInputError(ValueError):
    """Raised when scientific input data is invalid."""


def build_sparse_count_matrix_coo(
    n_genes: int, n_cells: int, n_nonzero: int, seed: int = 21
) -> sparse.coo_matrix:
    """
    Construct a sparse single-cell gene-expression count matrix in COO
    (coordinate) format, appropriate for CONSTRUCTION from scattered
    (row, col, value) triples -- the natural output shape of a sparse
    sequencing pipeline. COO is not efficient for arithmetic/indexing and is
    typically converted to CSR/CSC before further computation.
    """
    if n_genes <= 0 or n_cells <= 0:
        raise ScientificInputError("n_genes and n_cells must be positive")
    if not (0 < n_nonzero <= n_genes * n_cells):
        raise ScientificInputError("n_nonzero must be between 1 and n_genes * n_cells")

    rng = np.random.default_rng(seed)
    rows = rng.integers(0, n_genes, size=n_nonzero)
    cols = rng.integers(0, n_cells, size=n_nonzero)
    counts = rng.poisson(lam=3.0, size=n_nonzero).astype(np.float64) + 1.0  # counts >= 1

    matrix = sparse.coo_matrix((counts, (rows, cols)), shape=(n_genes, n_cells))
    # Duplicate (row, col) pairs from independent draws sum automatically on
    # conversion; report actual stored-nonzero count after summation.
    return matrix


def to_csr_for_row_operations(coo: sparse.coo_matrix) -> sparse.csr_matrix:
    """
    Convert to CSR (Compressed Sparse Row) format, the appropriate choice
    for efficient ROW-slicing and matrix-vector products -- e.g. extracting
    all expression values for one gene, or projecting cells onto a gene-
    weight vector.
    """
    return coo.tocsr()


def to_csc_for_column_operations(coo: sparse.coo_matrix) -> sparse.csc_matrix:
    """
    Convert to CSC (Compressed Sparse Column) format, the appropriate choice
    for efficient COLUMN-slicing -- e.g. extracting the full expression
    profile of one cell across all genes.
    """
    return coo.tocsc()


def total_counts_per_cell(csr: sparse.csr_matrix) -> np.ndarray:
    """
    Compute total UMI/read counts per cell (column sums) directly on the
    sparse matrix without densifying, using the matrix's built-in sum
    reduction which operates on stored nonzero entries only.
    """
    if not sparse.issparse(csr):
        raise ScientificInputError("Expected a sparse matrix")
    # .sum(axis=0) returns a np.matrix; convert to a flat ndarray explicitly.
    return np.asarray(csr.sum(axis=0)).ravel()


def project_gene_weights(csr: sparse.csr_matrix, gene_weights: np.ndarray) -> np.ndarray:
    """
    Compute a weighted gene-score per cell via sparse matrix-vector
    multiplication (gene_weights^T @ matrix), which scipy.sparse implements
    with algorithmic complexity proportional to the number of stored
    nonzeros rather than n_genes * n_cells -- the key advantage of sparse
    representation for this workload.
    """
    n_genes, n_cells = csr.shape
    if gene_weights.shape != (n_genes,):
        raise ScientificInputError(f"gene_weights must have shape ({n_genes},)")

    scores = csr.T @ gene_weights  # sparse matrix-vector product
    return np.asarray(scores).ravel()


def build_gene_interaction_network(n_genes: int, n_edges: int, seed: int = 23) -> sparse.csr_matrix:
    """
    Build a sparse symmetric adjacency matrix representing a gene-gene
    interaction network (e.g. co-expression or protein-protein interaction
    edges), stored in CSR format for efficient neighbor-lookup and
    matrix-vector operations (e.g. network propagation / diffusion steps).
    """
    if n_genes <= 0:
        raise ScientificInputError("n_genes must be positive")
    max_edges = n_genes * (n_genes - 1) // 2
    if not (0 < n_edges <= max_edges):
        raise ScientificInputError(f"n_edges must be between 1 and {max_edges}")

    rng = np.random.default_rng(seed)
    row = rng.integers(0, n_genes, size=n_edges)
    col = rng.integers(0, n_genes, size=n_edges)
    valid = row != col  # no self-loops
    row, col = row[valid], col[valid]
    weight = np.ones(row.shape[0])

    upper = sparse.coo_matrix((weight, (row, col)), shape=(n_genes, n_genes))
    symmetric = upper.maximum(upper.T)  # ensure symmetry without double counting
    return symmetric.tocsr()


def network_sparsity_report(matrix: sparse.spmatrix) -> dict[str, float]:
    """
    Report memory-relevant sparsity statistics WITHOUT densifying the
    matrix. Densifying (.toarray()) a large sparse matrix purely to inspect
    it defeats the purpose of using a sparse format at all.
    """
    n_rows, n_cols = matrix.shape
    n_possible = n_rows * n_cols
    n_stored = matrix.nnz
    density = n_stored / n_possible if n_possible > 0 else 0.0

    dense_bytes = n_possible * 8  # float64
    sparse_bytes = matrix.data.nbytes + matrix.indices.nbytes + matrix.indptr.nbytes \
        if isinstance(matrix, (sparse.csr_matrix, sparse.csc_matrix)) else matrix.data.nbytes

    return {
        "density": density,
        "nnz": n_stored,
        "dense_size_mb": dense_bytes / 1e6,
        "sparse_size_mb": sparse_bytes / 1e6,
    }


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    coo = build_sparse_count_matrix_coo(n_genes=2000, n_cells=500, n_nonzero=40_000)
    csr = to_csr_for_row_operations(coo)
    csc = to_csc_for_column_operations(coo)
    logger.info("Sparse count matrix: shape=%s nnz=%d", csr.shape, csr.nnz)

    per_cell_totals = total_counts_per_cell(csr)
    print("Total counts, first 5 cells:", np.round(per_cell_totals[:5], 1))

    rng = np.random.default_rng(seed=99)
    gene_weights = rng.normal(size=2000)
    scores = project_gene_weights(csr, gene_weights)
    print("Gene-weighted cell scores, first 5 cells:", np.round(scores[:5], 3))

    network = build_gene_interaction_network(n_genes=2000, n_edges=8000)
    report = network_sparsity_report(network)
    print(
        f"Gene network: density={report['density']:.5f}, nnz={report['nnz']}, "
        f"dense_size={report['dense_size_mb']:.2f}MB vs sparse_size={report['sparse_size_mb']:.2f}MB"
    )

    # Explicitly demonstrate: only densify a SMALL matrix for inspection.
    small = build_gene_interaction_network(n_genes=6, n_edges=8)
    print("Small network densified for inspection only:\n", small.toarray())


if __name__ == "__main__":
    main()
