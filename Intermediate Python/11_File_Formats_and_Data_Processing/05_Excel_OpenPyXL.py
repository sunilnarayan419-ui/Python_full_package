from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

try:
    from openpyxl import Workbook, load_workbook
    from openpyxl.styles import Font
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.worksheet import Worksheet
except ImportError as exc:  # pragma: no cover - depends on environment
    raise ImportError(
        "openpyxl is required for Excel processing. Install it with: "
        "pip install openpyxl"
    ) from exc

logger = logging.getLogger(__name__)


class DataFormatError(ValueError):
    """Raised when input data does not match the expected format."""


class DataValidationError(ValueError):
    """Raised when parsed data fails scientific validation."""


class FileProcessingError(RuntimeError):
    """Raised when a file-processing operation fails."""


@dataclass(frozen=True, slots=True)
class MeasurementRow:
    sample_id: str
    species: str
    height_cm: float
    leaf_count: int


HEADER_FONT = Font(bold=True)
MEASUREMENT_HEADERS = ("sample_id", "species", "height_cm", "leaf_count")


def build_experiment_workbook(
    experiment_id: str,
    summary: dict[str, str],
    measurements: list[MeasurementRow],
) -> Workbook:
    """Build a multi-sheet scientific report workbook in memory.

    Sheets:
        Experiment Summary  - key/value metadata
        Sample Measurements - tabular measurement data
    """
    workbook = Workbook()

    summary_sheet = workbook.active
    summary_sheet.title = "Experiment Summary"
    summary_sheet.append(["Field", "Value"])
    for cell in summary_sheet[1]:
        cell.font = HEADER_FONT
    summary_sheet.append(["experiment_id", experiment_id])
    for key, value in summary.items():
        summary_sheet.append([key, value])
    for column_index in (1, 2):
        summary_sheet.column_dimensions[get_column_letter(column_index)].width = 24

    measurements_sheet = workbook.create_sheet("Sample Measurements")
    measurements_sheet.append(list(MEASUREMENT_HEADERS))
    for cell in measurements_sheet[1]:
        cell.font = HEADER_FONT
    for row in measurements:
        measurements_sheet.append(
            [row.sample_id, row.species, row.height_cm, row.leaf_count]
        )
    for column_index in range(1, len(MEASUREMENT_HEADERS) + 1):
        measurements_sheet.column_dimensions[get_column_letter(column_index)].width = 18

    analysis_sheet = workbook.create_sheet("Analysis Results")
    analysis_sheet.append(["metric", "value"])
    for cell in analysis_sheet[1]:
        cell.font = HEADER_FONT
    if measurements:
        first_row = 2
        last_row = 1 + len(measurements)
        # Reference the Sample Measurements sheet directly with a formula
        # rather than recomputing aggregates in Python, so the workbook
        # stays self-consistent if a user edits the raw rows in Excel.
        avg_height_formula = (
            f"=AVERAGE('Sample Measurements'!C{first_row}:C{last_row})"
        )
        analysis_sheet.append(["average_height_cm", avg_height_formula])

    return workbook


def write_workbook_atomic(workbook: Workbook, xlsx_path: Path) -> None:
    """Save a workbook using a temp-file-then-replace strategy to avoid
    leaving a corrupted file in place if the write is interrupted."""
    tmp_path = xlsx_path.with_suffix(xlsx_path.suffix + ".tmp")
    try:
        workbook.save(tmp_path)
        tmp_path.replace(xlsx_path)
        logger.info("wrote workbook to %s", xlsx_path)
    except Exception:
        tmp_path.unlink(missing_ok=True)
        raise
    finally:
        workbook.close()


def read_measurements(xlsx_path: Path) -> list[MeasurementRow]:
    """Read the 'Sample Measurements' sheet in read-only, streaming mode.

    read_only=True avoids materializing the entire worksheet object graph
    in memory, which matters for workbooks with many rows.
    """
    if not xlsx_path.is_file():
        raise FileProcessingError(f"Workbook not found: {xlsx_path}")

    try:
        workbook = load_workbook(xlsx_path, read_only=True, data_only=True)
    except Exception as exc:
        raise DataFormatError(f"{xlsx_path}: could not open workbook ({exc})") from exc

    try:
        if "Sample Measurements" not in workbook.sheetnames:
            raise DataFormatError(
                f"{xlsx_path}: missing required sheet 'Sample Measurements'"
            )

        sheet: Worksheet = workbook["Sample Measurements"]
        rows = sheet.iter_rows(values_only=True)

        try:
            header = next(rows)
        except StopIteration as exc:
            raise DataFormatError(f"{xlsx_path}: sheet has no header row") from exc

        if tuple(header) != MEASUREMENT_HEADERS:
            raise DataFormatError(
                f"{xlsx_path}: unexpected header {header!r}, "
                f"expected {MEASUREMENT_HEADERS!r}"
            )

        results: list[MeasurementRow] = []
        for line_number, row in enumerate(rows, start=2):
            if row is None or all(value is None for value in row):
                continue
            sample_id, species, height_cm, leaf_count = row
            if sample_id is None or species is None:
                raise DataFormatError(f"row {line_number}: missing sample_id or species")
            try:
                height_cm_value = float(height_cm)
                leaf_count_value = int(leaf_count)
            except (TypeError, ValueError) as exc:
                raise DataFormatError(
                    f"row {line_number}: invalid numeric measurement data"
                ) from exc

            if height_cm_value < 0 or leaf_count_value < 0:
                raise DataValidationError(f"row {line_number}: measurement cannot be negative")

            results.append(
                MeasurementRow(
                    sample_id=str(sample_id),
                    species=str(species),
                    height_cm=height_cm_value,
                    leaf_count=leaf_count_value,
                )
            )

        logger.info("read %d measurement row(s) from %s", len(results), xlsx_path)
        return results
    finally:
        workbook.close()


def _demo() -> None:
    import tempfile

    logging.basicConfig(level=logging.INFO)

    measurements = [
        MeasurementRow("PS-001", "Arabidopsis thaliana", 12.4, 8),
        MeasurementRow("PS-002", "Oryza sativa", 45.7, 14),
        MeasurementRow("PS-003", "Zea mays", 88.1, 20),
    ]

    workbook = build_experiment_workbook(
        experiment_id="EXP-2025-014",
        summary={"lead_scientist": "N/A", "location": "greenhouse-3"},
        measurements=measurements,
    )

    with tempfile.TemporaryDirectory() as tmp_dir:
        xlsx_path = Path(tmp_dir) / "experiment_report.xlsx"
        write_workbook_atomic(workbook, xlsx_path)

        loaded = read_measurements(xlsx_path)
        logger.info("loaded %d measurement row(s) back from workbook", len(loaded))

        try:
            read_measurements(Path(tmp_dir) / "does_not_exist.xlsx")
        except FileProcessingError as exc:
            logger.warning("expected failure for missing file: %s", exc)


if __name__ == "__main__":
    _demo()
