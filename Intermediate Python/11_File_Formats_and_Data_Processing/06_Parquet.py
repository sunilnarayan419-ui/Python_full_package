from __future__ import annotations

import logging
from pathlib import Path

try:
    import pyarrow as pa
    import pyarrow.compute as pc
    import pyarrow.dataset as ds
    import pyarrow.parquet as pq
except ImportError as exc:  # pragma: no cover - depends on environment
    raise ImportError(
        "pyarrow is required for Parquet processing. Install it with: "
        "pip install pyarrow"
    ) from exc

logger = logging.getLogger(__name__)


class DataFormatError(ValueError):
    """Raised when input data does not match the expected format."""


class FileProcessingError(RuntimeError):
    """Raised when a file-processing operation fails."""


# Parquet stores data column-by-column with an embedded schema, which is
# why it is generally preferable to CSV for analytical workloads: readers
# can select a subset of columns without scanning unrelated ones, values
# are typed (no repeated string parsing), and columnar layout compresses
# far better than row-oriented text for numeric scientific measurements.
# CSV remains preferable for small, simple, human-editable interchange.
GENE_EXPRESSION_SCHEMA = pa.schema(
    [
        pa.field("sample_id", pa.string()),
        pa.field("species", pa.string()),
        pa.field("gene_id", pa.string()),
        pa.field("expression_level", pa.float64()),
        pa.field("experiment_date", pa.date32()),
    ]
)


def build_gene_expression_table(
    sample_ids: list[str],
    species: list[str],
    gene_ids: list[str],
    expression_levels: list[float],
    experiment_dates: list[str],
) -> pa.Table:
    """Construct a typed Arrow table for gene-expression records."""
    table = pa.table(
        {
            "sample_id": sample_ids,
            "species": species,
            "gene_id": gene_ids,
            "expression_level": expression_levels,
            "experiment_date": pa.array(experiment_dates, type=pa.date32()),
        },
        schema=GENE_EXPRESSION_SCHEMA,
    )
    return table


def write_partitioned_dataset(table: pa.Table, output_dir: Path) -> None:
    """Write a table as a Hive-style partitioned Parquet dataset.

    Partitioning on 'species' is appropriate here because species is
    low-cardinality relative to dataset size. Partitioning on a
    high-cardinality column (e.g. sample_id) would create excessive small
    files and should be avoided.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    ds.write_dataset(
        table,
        base_dir=str(output_dir),
        format="parquet",
        partitioning=ds.partitioning(pa.schema([("species", pa.string())]), flavor="hive"),
        existing_data_behavior="overwrite_or_ignore",
        file_options=ds.ParquetFileFormat().make_write_options(compression="snappy"),
    )
    logger.info("wrote partitioned dataset with %d row(s) to %s", table.num_rows, output_dir)


def write_single_parquet_file(table: pa.Table, parquet_path: Path) -> None:
    """Write a table to a single Parquet file with an atomic replacement."""
    tmp_path = parquet_path.with_suffix(parquet_path.suffix + ".tmp")
    try:
        pq.write_table(table, tmp_path, compression="zstd")
        tmp_path.replace(parquet_path)
        logger.info("wrote %d row(s) to %s", table.num_rows, parquet_path)
    except Exception:
        tmp_path.unlink(missing_ok=True)
        raise


def read_selected_columns(parquet_path: Path, columns: list[str]) -> pa.Table:
    """Read only the requested columns from a Parquet file.

    Column pruning avoids deserializing and materializing unrelated data,
    which is one of the main performance advantages of a columnar format.
    """
    if not parquet_path.exists():
        raise FileProcessingError(f"Parquet path not found: {parquet_path}")

    parquet_file = pq.ParquetFile(parquet_path)
    schema_names = set(parquet_file.schema_arrow.names)
    missing = set(columns) - schema_names
    if missing:
        raise DataFormatError(f"{parquet_path}: unknown column(s) requested: {missing}")

    table = parquet_file.read(columns=columns)
    logger.info("read %d row(s), columns=%s from %s", table.num_rows, columns, parquet_path)
    return table


def read_filtered_dataset(dataset_dir: Path, species_filter: str) -> pa.Table:
    """Read a partitioned dataset applying a predicate pushdown filter.

    Because the dataset is partitioned by species, filtering on species
    lets PyArrow skip entire partition directories without opening files
    that cannot match.
    """
    if not dataset_dir.exists():
        raise FileProcessingError(f"Dataset directory not found: {dataset_dir}")

    dataset = ds.dataset(str(dataset_dir), format="parquet", partitioning="hive")
    table = dataset.to_table(filter=pc.field("species") == species_filter)
    logger.info(
        "read %d row(s) matching species=%s from %s",
        table.num_rows,
        species_filter,
        dataset_dir,
    )
    return table


def _demo() -> None:
    import tempfile

    logging.basicConfig(level=logging.INFO)

    table = build_gene_expression_table(
        sample_ids=["S-01", "S-02", "S-03", "S-04"],
        species=["Arabidopsis thaliana", "Arabidopsis thaliana", "Oryza sativa", "Oryza sativa"],
        gene_ids=["AT1G01010", "AT1G01020", "OS01G0100100", "OS01G0100200"],
        expression_levels=[5.21, 3.87, 7.02, 1.44],
        experiment_dates=["2025-03-01", "2025-03-01", "2025-03-02", "2025-03-02"],
    )

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        single_file = tmp_path / "gene_expression.parquet"
        write_single_parquet_file(table, single_file)

        partial = read_selected_columns(single_file, ["gene_id", "expression_level"])
        logger.info("column-pruned read shape: %s", partial.shape)

        dataset_dir = tmp_path / "gene_expression_dataset"
        write_partitioned_dataset(table, dataset_dir)

        filtered = read_filtered_dataset(dataset_dir, species_filter="Oryza sativa")
        logger.info("filtered read shape: %s", filtered.shape)


if __name__ == "__main__":
    _demo()
