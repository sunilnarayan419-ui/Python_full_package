from __future__ import annotations

import logging
from pathlib import Path

import numpy as np

try:
    import h5py
except ImportError as exc:  # pragma: no cover - depends on environment
    raise ImportError(
        "h5py is required for HDF5 processing. Install it with: "
        "pip install h5py"
    ) from exc

logger = logging.getLogger(__name__)


class DataFormatError(ValueError):
    """Raised when input data does not match the expected format."""


class FileProcessingError(RuntimeError):
    """Raised when a file-processing operation fails."""


# HDF5 is well suited to large hierarchical numerical scientific datasets:
# it supports nested groups (analogous to directories), typed n-dimensional
# datasets with chunking/compression, and partial (sliced) I/O so a
# consumer can read a small window of a very large array without loading
# the entire dataset into memory.
EXPERIMENT_ROOT = "/experiment"
SAMPLES_GROUP = f"{EXPERIMENT_ROOT}/samples"
MEASUREMENTS_GROUP = f"{EXPERIMENT_ROOT}/measurements"
METADATA_GROUP = f"{EXPERIMENT_ROOT}/metadata"


def write_experiment_hdf5(
    hdf5_path: Path,
    experiment_id: str,
    sample_ids: list[str],
    expression_matrix: np.ndarray,
    gene_ids: list[str],
) -> None:
    """Write a hierarchical experiment dataset to HDF5.

    expression_matrix shape: (n_samples, n_genes)
    Chunking and gzip compression are applied to the large numerical
    dataset; small metadata arrays are stored uncompressed for simplicity.
    """
    if expression_matrix.shape[0] != len(sample_ids):
        raise DataFormatError("expression_matrix row count must match sample_ids length")
    if expression_matrix.shape[1] != len(gene_ids):
        raise DataFormatError("expression_matrix column count must match gene_ids length")

    tmp_path = hdf5_path.with_suffix(hdf5_path.suffix + ".tmp")
    try:
        with h5py.File(tmp_path, "w") as handle:
            root = handle.create_group(EXPERIMENT_ROOT.lstrip("/"))
            root.attrs["experiment_id"] = experiment_id

            samples_group = root.create_group("samples")
            samples_group.create_dataset(
                "sample_ids",
                data=np.array(sample_ids, dtype=h5py.string_dtype(encoding="utf-8")),
            )

            measurements_group = root.create_group("measurements")
            chunk_shape = (
                min(64, expression_matrix.shape[0]) or 1,
                min(256, expression_matrix.shape[1]) or 1,
            )
            expression_dataset = measurements_group.create_dataset(
                "expression_matrix",
                data=expression_matrix,
                chunks=chunk_shape,
                compression="gzip",
                compression_opts=4,
            )
            expression_dataset.attrs["units"] = "log2_normalized_counts"
            measurements_group.create_dataset(
                "gene_ids",
                data=np.array(gene_ids, dtype=h5py.string_dtype(encoding="utf-8")),
            )

            metadata_group = root.create_group("metadata")
            metadata_group.attrs["n_samples"] = expression_matrix.shape[0]
            metadata_group.attrs["n_genes"] = expression_matrix.shape[1]

        tmp_path.replace(hdf5_path)
        logger.info(
            "wrote experiment %s (%d samples x %d genes) to %s",
            experiment_id,
            expression_matrix.shape[0],
            expression_matrix.shape[1],
            hdf5_path,
        )
    except Exception:
        tmp_path.unlink(missing_ok=True)
        raise


def read_expression_slice(
    hdf5_path: Path, sample_start: int, sample_end: int
) -> np.ndarray:
    """Read a row-slice of the expression matrix without loading the full array.

    h5py datasets support NumPy-style slicing that only reads the
    requested region from disk, which is essential for datasets too large
    to fit comfortably in memory.
    """
    if not hdf5_path.is_file():
        raise FileProcessingError(f"HDF5 file not found: {hdf5_path}")

    with h5py.File(hdf5_path, "r") as handle:
        dataset_path = f"{MEASUREMENTS_GROUP}/expression_matrix"
        if dataset_path not in handle:
            raise DataFormatError(f"{hdf5_path}: missing dataset {dataset_path}")

        dataset = handle[dataset_path]
        sliced = dataset[sample_start:sample_end, :]
        logger.info(
            "read slice [%d:%d] shape=%s from %s",
            sample_start,
            sample_end,
            sliced.shape,
            hdf5_path,
        )
        return sliced


def read_experiment_metadata(hdf5_path: Path) -> dict[str, object]:
    """Read only group/dataset attributes, avoiding any large array reads."""
    if not hdf5_path.is_file():
        raise FileProcessingError(f"HDF5 file not found: {hdf5_path}")

    with h5py.File(hdf5_path, "r") as handle:
        if EXPERIMENT_ROOT.lstrip("/") not in handle:
            raise DataFormatError(f"{hdf5_path}: missing root group {EXPERIMENT_ROOT}")

        root = handle[EXPERIMENT_ROOT.lstrip("/")]
        metadata_group = root["metadata"]

        return {
            "experiment_id": root.attrs.get("experiment_id"),
            "n_samples": int(metadata_group.attrs.get("n_samples", 0)),
            "n_genes": int(metadata_group.attrs.get("n_genes", 0)),
        }


def _demo() -> None:
    import tempfile

    logging.basicConfig(level=logging.INFO)

    rng = np.random.default_rng(seed=42)
    n_samples, n_genes = 200, 500
    expression_matrix = rng.normal(loc=5.0, scale=1.5, size=(n_samples, n_genes))
    sample_ids = [f"S-{i:04d}" for i in range(n_samples)]
    gene_ids = [f"GENE-{i:04d}" for i in range(n_genes)]

    with tempfile.TemporaryDirectory() as tmp_dir:
        hdf5_path = Path(tmp_dir) / "expression_experiment.h5"
        write_experiment_hdf5(
            hdf5_path,
            experiment_id="EXP-2025-014",
            sample_ids=sample_ids,
            expression_matrix=expression_matrix,
            gene_ids=gene_ids,
        )

        metadata = read_experiment_metadata(hdf5_path)
        logger.info("metadata: %s", metadata)

        first_ten_rows = read_expression_slice(hdf5_path, 0, 10)
        logger.info("sliced read shape (no full-array load): %s", first_ten_rows.shape)


if __name__ == "__main__":
    _demo()
