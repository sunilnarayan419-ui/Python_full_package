"""
10_Memory_Optimization.py

Production-oriented memory-efficient numerical computing patterns for large
scientific arrays: dtype selection, view-vs-copy awareness, chunked
processing, and disk-backed memory mapping for out-of-core genomic-scale
data.
"""

from __future__ import annotations

import logging
import tempfile
from pathlib import Path

import numpy as np

logger = logging.getLogger(__name__)


class ScientificInputError(ValueError):
    """Raised when scientific input data is invalid."""


def compare_dtype_footprint(n_elements: int) -> dict[str, int]:
    """
    Compare memory footprint of common dtypes for a large read-count array
    (e.g. RNA-seq raw counts, which are non-negative integers and rarely
    need 64-bit precision).
    """
    if n_elements <= 0:
        raise ScientificInputError("n_elements must be positive")

    footprints = {}
    for dtype in (np.int64, np.int32, np.uint16, np.float64, np.float32):
        footprints[np.dtype(dtype).name] = n_elements * np.dtype(dtype).itemsize
    return footprints


def demonstrate_view_vs_copy(matrix: np.ndarray) -> None:
    """
    Demonstrate which common operations return a view (share memory, no
    allocation) vs a copy (new allocation), which matters directly for
    memory budgets on large arrays.
    """
    if matrix.ndim != 2:
        raise ScientificInputError(f"Expected 2D matrix; got ndim={matrix.ndim}")

    basic_slice = matrix[:, :2]          # view: shares memory with matrix
    reshaped = matrix.reshape(-1)        # view IF matrix is C-contiguous
    fancy_indexed = matrix[[0, 2]]       # copy: fancy indexing always copies
    explicit_copy = matrix.copy()        # copy: explicit, intentional

    logger.info("basic_slice shares memory with matrix: %s", np.shares_memory(basic_slice, matrix))
    logger.info("reshaped shares memory with matrix: %s", np.shares_memory(reshaped, matrix))
    logger.info("fancy_indexed shares memory with matrix: %s", np.shares_memory(fancy_indexed, matrix))
    logger.info("explicit_copy shares memory with matrix: %s", np.shares_memory(explicit_copy, matrix))


def normalize_in_place(matrix: np.ndarray, scale: float) -> None:
    """
    Scale a matrix in place to avoid allocating a second full-size array.

    In-place operations are safe here because `matrix` is owned exclusively
    by the caller for this operation and no other view depends on its
    original (unscaled) values. In-place mutation must NOT be used when
    other code still expects to read the original data through an alias.
    """
    if scale == 0:
        raise ScientificInputError("scale must be non-zero")
    matrix *= scale  # in-place: no new allocation


def chunked_row_means(matrix: np.ndarray, chunk_rows: int) -> np.ndarray:
    """
    Compute per-row means of a large matrix in row chunks, avoiding
    materializing any large intermediate beyond one chunk at a time. This
    generalizes to memory-mapped or streamed data sources that cannot be
    fully materialized in RAM.
    """
    if chunk_rows <= 0:
        raise ScientificInputError("chunk_rows must be positive")

    n_rows = matrix.shape[0]
    means = np.empty(n_rows, dtype=np.float64)
    for start in range(0, n_rows, chunk_rows):
        stop = min(start + chunk_rows, n_rows)
        means[start:stop] = matrix[start:stop].mean(axis=1)
    return means


def demonstrate_memmap(n_rows: int, n_cols: int) -> float:
    """
    Create a disk-backed memory-mapped array (np.memmap) for a
    larger-than-comfortable-RAM genomic-scale matrix, write to it in chunks,
    and compute a reduction without loading the full array into RAM at once.

    Returns the overall mean computed via chunked access to the memmap.
    """
    if n_rows <= 0 or n_cols <= 0:
        raise ScientificInputError("n_rows and n_cols must be positive")

    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "genotype_matrix.dat"
        mm = np.memmap(path, dtype=np.float32, mode="w+", shape=(n_rows, n_cols))

        rng = np.random.default_rng(seed=9)
        chunk_rows = 1000
        for start in range(0, n_rows, chunk_rows):
            stop = min(start + chunk_rows, n_rows)
            mm[start:stop] = rng.normal(size=(stop - start, n_cols)).astype(np.float32)
        mm.flush()

        # Read back and reduce in chunks -- never materialize the full array.
        total = 0.0
        count = 0
        for start in range(0, n_rows, chunk_rows):
            stop = min(start + chunk_rows, n_rows)
            block = mm[start:stop]
            total += float(block.sum())
            count += block.size

        del mm  # release the memmap and its OS-level file handle
        return total / count


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    footprints = compare_dtype_footprint(n_elements=1_000_000)
    for name, nbytes in footprints.items():
        print(f"{name}: {nbytes / 1e6:.2f} MB for 1,000,000 elements")

    matrix = np.arange(12, dtype=np.float64).reshape(3, 4)
    demonstrate_view_vs_copy(matrix)

    normalize_in_place(matrix, scale=2.0)
    print("In-place scaled matrix:\n", matrix)

    big = np.arange(5000 * 20, dtype=np.float64).reshape(5000, 20)
    row_means = chunked_row_means(big, chunk_rows=500)
    print("Chunked row-mean computation shape:", row_means.shape)

    overall_mean = demonstrate_memmap(n_rows=5000, n_cols=50)
    print(f"Memmap-backed overall mean (safe, small demo size): {overall_mean:.5f}")


if __name__ == "__main__":
    main()
