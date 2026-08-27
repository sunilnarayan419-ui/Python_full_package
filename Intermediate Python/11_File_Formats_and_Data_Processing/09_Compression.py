from __future__ import annotations

import bz2
import gzip
import lzma
import logging
import shutil
import zipfile
from pathlib import Path

logger = logging.getLogger(__name__)

_CHUNK_SIZE = 64 * 1024  # 64 KiB streaming chunk size


class FileProcessingError(RuntimeError):
    """Raised when a file-processing operation fails."""


# Trade-offs (no single algorithm is universally best):
#   gzip   - balanced/general-purpose; fast; widely supported; moderate ratio
#   bz2    - often better ratio than gzip on text-like data; slower
#   lzma   - typically the best compression ratio; highest CPU/memory cost
#   zipfile- archive/container format bundling multiple files with metadata,
#            not primarily a single-stream compressor


def compress_file_gzip(source_path: Path, dest_path: Path, *, compresslevel: int = 6) -> None:
    """Stream-compress a file with gzip in bounded-size chunks."""
    if not source_path.is_file():
        raise FileProcessingError(f"source file not found: {source_path}")

    tmp_path = dest_path.with_suffix(dest_path.suffix + ".tmp")
    try:
        with source_path.open("rb") as src, gzip.open(
            tmp_path, "wb", compresslevel=compresslevel
        ) as dst:
            shutil.copyfileobj(src, dst, length=_CHUNK_SIZE)
        tmp_path.replace(dest_path)
        logger.info(
            "gzip-compressed %s -> %s (%d -> %d bytes)",
            source_path.name,
            dest_path.name,
            source_path.stat().st_size,
            dest_path.stat().st_size,
        )
    except Exception:
        tmp_path.unlink(missing_ok=True)
        raise


def decompress_file_gzip(source_path: Path, dest_path: Path) -> None:
    """Stream-decompress a gzip file in bounded-size chunks."""
    if not source_path.is_file():
        raise FileProcessingError(f"compressed file not found: {source_path}")

    tmp_path = dest_path.with_suffix(dest_path.suffix + ".tmp")
    try:
        with gzip.open(source_path, "rb") as src, tmp_path.open("wb") as dst:
            shutil.copyfileobj(src, dst, length=_CHUNK_SIZE)
        tmp_path.replace(dest_path)
        logger.info("gzip-decompressed %s -> %s", source_path.name, dest_path.name)
    except Exception:
        tmp_path.unlink(missing_ok=True)
        raise


def compress_file_bz2(source_path: Path, dest_path: Path, *, compresslevel: int = 9) -> None:
    """Stream-compress a file with bz2; typically stronger ratio, slower than gzip."""
    if not source_path.is_file():
        raise FileProcessingError(f"source file not found: {source_path}")

    tmp_path = dest_path.with_suffix(dest_path.suffix + ".tmp")
    try:
        with source_path.open("rb") as src, bz2.open(
            tmp_path, "wb", compresslevel=compresslevel
        ) as dst:
            shutil.copyfileobj(src, dst, length=_CHUNK_SIZE)
        tmp_path.replace(dest_path)
        logger.info("bz2-compressed %s -> %s", source_path.name, dest_path.name)
    except Exception:
        tmp_path.unlink(missing_ok=True)
        raise


def compress_file_lzma(source_path: Path, dest_path: Path, *, preset: int = 6) -> None:
    """Stream-compress a file with lzma; highest ratio, most CPU/memory intensive."""
    if not source_path.is_file():
        raise FileProcessingError(f"source file not found: {source_path}")

    tmp_path = dest_path.with_suffix(dest_path.suffix + ".tmp")
    try:
        with source_path.open("rb") as src, lzma.open(tmp_path, "wb", preset=preset) as dst:
            shutil.copyfileobj(src, dst, length=_CHUNK_SIZE)
        tmp_path.replace(dest_path)
        logger.info("lzma-compressed %s -> %s", source_path.name, dest_path.name)
    except Exception:
        tmp_path.unlink(missing_ok=True)
        raise


def create_archive(archive_path: Path, member_paths: list[Path]) -> None:
    """Bundle multiple files into a single compressed zip archive.

    zipfile is used here for its archive/container semantics (multiple
    named members with independent metadata), which the single-stream
    gzip/bz2/lzma modules do not provide.
    """
    for member_path in member_paths:
        if not member_path.is_file():
            raise FileProcessingError(f"archive member not found: {member_path}")

    tmp_path = archive_path.with_suffix(archive_path.suffix + ".tmp")
    try:
        with zipfile.ZipFile(
            tmp_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6
        ) as archive:
            for member_path in member_paths:
                archive.write(member_path, arcname=member_path.name)
        tmp_path.replace(archive_path)
        logger.info("created archive %s with %d member(s)", archive_path, len(member_paths))
    except Exception:
        tmp_path.unlink(missing_ok=True)
        raise


def extract_archive(archive_path: Path, dest_dir: Path) -> list[Path]:
    """Safely extract a zip archive, rejecting entries that would escape dest_dir."""
    if not archive_path.is_file():
        raise FileProcessingError(f"archive not found: {archive_path}")

    dest_dir.mkdir(parents=True, exist_ok=True)
    resolved_dest = dest_dir.resolve()
    extracted: list[Path] = []

    with zipfile.ZipFile(archive_path, "r") as archive:
        for info in archive.infolist():
            target_path = (dest_dir / info.filename).resolve()
            if not target_path.is_relative_to(resolved_dest):
                raise FileProcessingError(
                    f"refusing to extract path-traversal entry: {info.filename!r}"
                )
            if info.is_dir():
                target_path.mkdir(parents=True, exist_ok=True)
                continue
            target_path.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(info, "r") as src, target_path.open("wb") as dst:
                shutil.copyfileobj(src, dst, length=_CHUNK_SIZE)
            extracted.append(target_path)

    logger.info("extracted %d file(s) from %s to %s", len(extracted), archive_path, dest_dir)
    return extracted


def _demo() -> None:
    import tempfile

    logging.basicConfig(level=logging.INFO)

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        source_a = tmp_path / "measurements_a.txt"
        source_b = tmp_path / "measurements_b.txt"
        source_a.write_text("sample_id,height_cm\nPS-001,12.4\nPS-002,45.7\n" * 200, encoding="utf-8")
        source_b.write_text("sample_id,leaf_count\nPS-001,8\nPS-002,14\n" * 200, encoding="utf-8")

        gz_path = tmp_path / "measurements_a.txt.gz"
        compress_file_gzip(source_a, gz_path)
        restored_a = tmp_path / "measurements_a_restored.txt"
        decompress_file_gzip(gz_path, restored_a)
        assert restored_a.read_text(encoding="utf-8") == source_a.read_text(encoding="utf-8")

        bz2_path = tmp_path / "measurements_a.txt.bz2"
        compress_file_bz2(source_a, bz2_path)

        lzma_path = tmp_path / "measurements_a.txt.xz"
        compress_file_lzma(source_a, lzma_path)

        logger.info(
            "sizes: original=%d gzip=%d bz2=%d lzma=%d",
            source_a.stat().st_size,
            gz_path.stat().st_size,
            bz2_path.stat().st_size,
            lzma_path.stat().st_size,
        )

        archive_path = tmp_path / "measurements_bundle.zip"
        create_archive(archive_path, [source_a, source_b])

        extract_dir = tmp_path / "extracted"
        extracted_files = extract_archive(archive_path, extract_dir)
        logger.info("extracted files: %s", [p.name for p in extracted_files])


if __name__ == "__main__":
    _demo()
