from __future__ import annotations

import csv
import logging
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterator, Sequence

logger = logging.getLogger(__name__)

REQUIRED_FIELDS: tuple[str, ...] = (
    "sample_id",
    "species",
    "height_cm",
    "leaf_count",
    "measurement_date",
)


class DataFormatError(ValueError):
    """Raised when input data does not match the expected format."""


class DataValidationError(ValueError):
    """Raised when parsed data fails scientific validation."""


class FileProcessingError(RuntimeError):
    """Raised when a file-processing operation fails."""


@dataclass(frozen=True, slots=True)
class PlantSample:
    sample_id: str
    species: str
    height_cm: float
    leaf_count: int
    measurement_date: date


def _parse_row(row: dict[str, str], line_number: int) -> PlantSample:
    missing = [field for field in REQUIRED_FIELDS if field not in row or row[field] == ""]
    if missing:
        raise DataFormatError(
            f"line {line_number}: missing required field(s): {', '.join(missing)}"
        )

    try:
        height_cm = float(row["height_cm"])
    except ValueError as exc:
        raise DataFormatError(
            f"line {line_number}: invalid height_cm value {row['height_cm']!r}"
        ) from exc

    try:
        leaf_count = int(row["leaf_count"])
    except ValueError as exc:
        raise DataFormatError(
            f"line {line_number}: invalid leaf_count value {row['leaf_count']!r}"
        ) from exc

    try:
        measurement_date = date.fromisoformat(row["measurement_date"])
    except ValueError as exc:
        raise DataFormatError(
            f"line {line_number}: invalid measurement_date value "
            f"{row['measurement_date']!r}"
        ) from exc

    if height_cm < 0:
        raise DataValidationError(f"line {line_number}: height_cm cannot be negative")
    if leaf_count < 0:
        raise DataValidationError(f"line {line_number}: leaf_count cannot be negative")

    return PlantSample(
        sample_id=row["sample_id"],
        species=row["species"],
        height_cm=height_cm,
        leaf_count=leaf_count,
        measurement_date=measurement_date,
    )


def iter_plant_samples(
    csv_path: Path, *, skip_malformed: bool = False
) -> Iterator[PlantSample]:
    """Stream plant samples from a CSV file row-by-row.

    Rows are validated and converted lazily so arbitrarily large files can
    be processed without loading the entire dataset into memory.
    """
    if not csv_path.is_file():
        raise FileProcessingError(f"CSV file not found: {csv_path}")

    with csv_path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)

        if reader.fieldnames is None:
            raise DataFormatError(f"{csv_path}: file has no header row")

        missing_columns = set(REQUIRED_FIELDS) - set(reader.fieldnames)
        if missing_columns:
            raise DataFormatError(
                f"{csv_path}: missing required column(s): {sorted(missing_columns)}"
            )

        record_count = 0
        skipped_count = 0
        for line_number, row in enumerate(reader, start=2):
            try:
                sample = _parse_row(row, line_number)
            except (DataFormatError, DataValidationError) as exc:
                if skip_malformed:
                    skipped_count += 1
                    logger.warning("skipping malformed row: %s", exc)
                    continue
                raise
            record_count += 1
            yield sample

        logger.info(
            "processed %s: %d valid record(s), %d skipped",
            csv_path.name,
            record_count,
            skipped_count,
        )


def write_plant_samples(csv_path: Path, samples: Sequence[PlantSample]) -> None:
    """Write plant samples to CSV using an atomic temp-file-then-replace strategy."""
    tmp_path = csv_path.with_suffix(csv_path.suffix + ".tmp")
    try:
        with tmp_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=REQUIRED_FIELDS)
            writer.writeheader()
            for sample in samples:
                writer.writerow(
                    {
                        "sample_id": sample.sample_id,
                        "species": sample.species,
                        "height_cm": f"{sample.height_cm:.2f}",
                        "leaf_count": sample.leaf_count,
                        "measurement_date": sample.measurement_date.isoformat(),
                    }
                )
        tmp_path.replace(csv_path)
        logger.info("wrote %d record(s) to %s", len(samples), csv_path)
    except Exception:
        tmp_path.unlink(missing_ok=True)
        raise


def _demo() -> None:
    import tempfile

    logging.basicConfig(level=logging.INFO)

    sample_rows = [
        PlantSample("PS-001", "Arabidopsis thaliana", 12.4, 8, date(2025, 3, 1)),
        PlantSample("PS-002", "Oryza sativa", 45.7, 14, date(2025, 3, 2)),
        PlantSample("PS-003", "Zea mays", 88.1, 20, date(2025, 3, 3)),
    ]

    with tempfile.TemporaryDirectory() as tmp_dir:
        csv_path = Path(tmp_dir) / "plant_samples.csv"
        write_plant_samples(csv_path, sample_rows)

        for sample in iter_plant_samples(csv_path):
            logger.info("loaded sample: %s (%s)", sample.sample_id, sample.species)

        malformed_path = Path(tmp_dir) / "plant_samples_malformed.csv"
        malformed_path.write_text(
            "sample_id,species,height_cm,leaf_count,measurement_date\n"
            "PS-004,Solanum lycopersicum,not_a_number,10,2025-03-04\n"
            "PS-005,Solanum lycopersicum,30.2,12,2025-03-05\n",
            encoding="utf-8",
        )
        recovered = list(iter_plant_samples(malformed_path, skip_malformed=True))
        logger.info("recovered %d record(s) from malformed file", len(recovered))


if __name__ == "__main__":
    _demo()
