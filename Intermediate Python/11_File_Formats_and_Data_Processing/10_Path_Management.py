from __future__ import annotations

import logging
import re
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)


class FileProcessingError(RuntimeError):
    """Raised when a file-processing operation fails."""


class PathSecurityError(RuntimeError):
    """Raised when a supplied path fails containment or safety validation."""


_SAFE_NAME_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+$")


def ensure_scientific_data_layout(base_dir: Path) -> dict[str, Path]:
    """Create the standard scientific-data directory layout under base_dir.

    data/
        raw/
        processed/
        metadata/
        reports/
    """
    layout = {
        "raw": base_dir / "data" / "raw",
        "processed": base_dir / "data" / "processed",
        "metadata": base_dir / "data" / "metadata",
        "reports": base_dir / "data" / "reports",
    }
    for name, directory in layout.items():
        directory.mkdir(parents=True, exist_ok=True)
        logger.info("ensured directory exists: %s (%s)", directory, name)
    return layout


def safe_child_path(base_dir: Path, user_supplied_name: str) -> Path:
    """Resolve a user-supplied filename safely within base_dir.

    Rejects path traversal attempts (e.g. '../../etc/passwd'), absolute
    paths, and names containing characters outside a conservative
    allow-list. User-supplied path components must never be trusted
    blindly, even when they appear to be a simple filename.
    """
    if not _SAFE_NAME_PATTERN.match(user_supplied_name):
        raise PathSecurityError(
            f"unsafe or invalid filename component: {user_supplied_name!r}"
        )

    resolved_base = base_dir.resolve()
    candidate = (base_dir / user_supplied_name).resolve()

    if not candidate.is_relative_to(resolved_base):
        raise PathSecurityError(
            f"path traversal detected: {user_supplied_name!r} escapes {base_dir}"
        )

    return candidate


def find_raw_data_files(raw_dir: Path, *, pattern: str = "*.csv") -> list[Path]:
    """Non-recursively glob for raw data files matching a pattern."""
    if not raw_dir.is_dir():
        raise FileProcessingError(f"raw data directory does not exist: {raw_dir}")

    matches = sorted(raw_dir.glob(pattern))
    logger.info("found %d file(s) matching %r in %s", len(matches), pattern, raw_dir)
    return matches


def find_all_reports(reports_dir: Path, *, suffix: str = ".xlsx") -> list[Path]:
    """Recursively search for report files by suffix."""
    if not reports_dir.is_dir():
        raise FileProcessingError(f"reports directory does not exist: {reports_dir}")

    matches = sorted(p for p in reports_dir.rglob(f"*{suffix}") if p.is_file())
    logger.info("found %d report(s) with suffix %r under %s", len(matches), suffix, reports_dir)
    return matches


def describe_path(path: Path) -> dict[str, object]:
    """Return structural metadata about a path without assuming it exists."""
    return {
        "name": path.name,
        "stem": path.stem,
        "suffix": path.suffix,
        "parent": path.parent,
        "is_absolute": path.is_absolute(),
        "exists": path.exists(),
        "is_file": path.is_file() if path.exists() else None,
        "is_dir": path.is_dir() if path.exists() else None,
    }


def write_text_atomic(target_path: Path, content: str, *, encoding: str = "utf-8") -> None:
    """Write text to a file via a temp file plus atomic replace.

    Using a temporary file in the same directory (so the rename stays on
    one filesystem) prevents readers from ever observing a partially
    written file, and avoids clobbering existing valuable data if the
    write is interrupted mid-way.
    """
    target_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = target_path.with_suffix(target_path.suffix + ".tmp")
    try:
        tmp_path.write_text(content, encoding=encoding)
        tmp_path.replace(target_path)
        logger.info("atomically wrote %d character(s) to %s", len(content), target_path)
    except Exception:
        tmp_path.unlink(missing_ok=True)
        raise


def _demo() -> None:
    logging.basicConfig(level=logging.INFO)

    with tempfile.TemporaryDirectory() as tmp_dir:
        base_dir = Path(tmp_dir)
        layout = ensure_scientific_data_layout(base_dir)

        raw_file = layout["raw"] / "sample_batch_001.csv"
        raw_file.write_text("sample_id,height_cm\nPS-001,12.4\n", encoding="utf-8")

        found = find_raw_data_files(layout["raw"], pattern="*.csv")
        logger.info("raw files found: %s", [p.name for p in found])

        report_dir = layout["reports"] / "2025" / "march"
        report_dir.mkdir(parents=True, exist_ok=True)
        (report_dir / "summary.xlsx").write_bytes(b"")

        reports = find_all_reports(layout["reports"])
        logger.info("reports found recursively: %s", [str(p.relative_to(base_dir)) for p in reports])

        info = describe_path(raw_file)
        logger.info("path info for %s: %s", raw_file.name, info)

        safe_path = safe_child_path(layout["metadata"], "experiment_014.json")
        write_text_atomic(safe_path, '{"experiment_id": "EXP-2025-014"}')
        logger.info("wrote metadata file at %s", safe_path)

        try:
            safe_child_path(layout["metadata"], "../../etc/passwd")
        except PathSecurityError as exc:
            logger.warning("expected rejection of unsafe path: %s", exc)


if __name__ == "__main__":
    _demo()
