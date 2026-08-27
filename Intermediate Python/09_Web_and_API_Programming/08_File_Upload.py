"""
08_File_Upload.py

Secure ingestion of scientific data files (CSV, FASTA, JSON) via FastAPI
UploadFile, following the pipeline:

    Upload -> Validate -> Generate safe internal filename -> Store
        -> Process -> Cleanup / retention

Security properties enforced:
    - the client-supplied filename is NEVER trusted or used to build a
      filesystem path (prevents path traversal)
    - extension and content-type are validated against an allow-list
    - size is bounded and enforced while streaming, so a client cannot
      exhaust memory or disk by uploading an oversized file
    - files are written to a controlled temporary directory with a
      generated, collision-resistant internal name
    - uploaded content is only ever parsed as data, never executed
"""

from __future__ import annotations

import logging
import os
import tempfile
import uuid
from dataclasses import dataclass
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile, status

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS: dict[str, set[str]] = {
    "text/csv": {".csv"},
    "application/json": {".json"},
    "text/x-fasta": {".fasta", ".fa"},
    "text/plain": {".fasta", ".fa", ".csv"},
}

MAX_UPLOAD_SIZE_BYTES = int(os.environ.get("MAX_UPLOAD_SIZE", 25 * 1024 * 1024))  # 25 MB default
CHUNK_SIZE_BYTES = 1024 * 1024  # 1 MB

UPLOAD_ROOT = Path(tempfile.gettempdir()) / "scientific-uploads"


class InvalidUploadError(ValueError):
    """Raised when an uploaded file fails validation."""


class UploadTooLargeError(InvalidUploadError):
    """Raised when an uploaded file exceeds the configured size limit."""


@dataclass(slots=True)
class StoredUpload:
    internal_id: str
    storage_path: Path
    original_filename: str
    size_bytes: int
    content_type: str


def _safe_suffix(original_filename: str, content_type: str) -> str:
    """Derive a validated file extension without ever trusting the raw
    client filename as a path component."""
    suffix = Path(original_filename).suffix.lower()
    allowed_for_type = ALLOWED_EXTENSIONS.get(content_type)
    if allowed_for_type is None:
        raise InvalidUploadError(f"unsupported content type: {content_type}")
    if suffix not in allowed_for_type:
        raise InvalidUploadError(
            f"extension '{suffix}' not permitted for content type '{content_type}'"
        )
    return suffix


def _ensure_upload_root() -> Path:
    UPLOAD_ROOT.mkdir(parents=True, exist_ok=True, mode=0o700)
    return UPLOAD_ROOT


async def store_upload(upload: UploadFile) -> StoredUpload:
    """Validate and persist an uploaded scientific data file.

    The original filename is used only for display/metadata purposes --
    the on-disk name is always a generated UUID, and the file is always
    written inside UPLOAD_ROOT, so a filename like '../../etc/passwd'
    cannot escape the intended directory.
    """
    if upload.filename is None:
        raise InvalidUploadError("filename is required")
    if upload.content_type is None:
        raise InvalidUploadError("content-type is required")

    suffix = _safe_suffix(upload.filename, upload.content_type)

    root = _ensure_upload_root()
    internal_id = uuid.uuid4().hex
    storage_path = (root / f"{internal_id}{suffix}").resolve()

    # Defense in depth: even though the name is generated, confirm the
    # resolved path still lives under the intended root before writing.
    if root.resolve() not in storage_path.parents:
        raise InvalidUploadError("resolved storage path escaped upload root")

    bytes_written = 0
    try:
        with open(storage_path, "wb") as destination:
            while chunk := await upload.read(CHUNK_SIZE_BYTES):
                bytes_written += len(chunk)
                if bytes_written > MAX_UPLOAD_SIZE_BYTES:
                    raise UploadTooLargeError(
                        f"upload exceeds maximum size of {MAX_UPLOAD_SIZE_BYTES} bytes"
                    )
                destination.write(chunk)
    except UploadTooLargeError:
        storage_path.unlink(missing_ok=True)
        raise
    except Exception:
        storage_path.unlink(missing_ok=True)
        raise
    finally:
        await upload.close()

    logger.info(
        "upload stored internal_id=%s size=%d content_type=%s",
        internal_id, bytes_written, upload.content_type,
    )

    return StoredUpload(
        internal_id=internal_id,
        storage_path=storage_path,
        original_filename=upload.filename,
        size_bytes=bytes_written,
        content_type=upload.content_type,
    )


def cleanup_upload(stored: StoredUpload) -> None:
    """Remove a processed upload once it is no longer needed, per the
    service's retention policy."""
    stored.storage_path.unlink(missing_ok=True)
    logger.info("upload cleaned up internal_id=%s", stored.internal_id)


def count_csv_data_rows(path: Path) -> int:
    """Example downstream processing step: count data rows in an uploaded
    CSV without loading the entire file into memory at once."""
    row_count = 0
    with open(path, "r", encoding="utf-8", errors="strict", newline="") as handle:
        next(handle, None)  # skip header
        for _ in handle:
            row_count += 1
    return row_count


app = FastAPI(title="Scientific File Ingestion API")


@app.post("/uploads/datasets", status_code=status.HTTP_201_CREATED)
async def upload_dataset(file: UploadFile) -> dict[str, object]:
    try:
        stored = await store_upload(file)
    except UploadTooLargeError as exc:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=str(exc))
    except InvalidUploadError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))

    try:
        row_count = None
        if stored.storage_path.suffix == ".csv":
            row_count = count_csv_data_rows(stored.storage_path)
    finally:
        cleanup_upload(stored)

    return {
        "original_filename": stored.original_filename,
        "size_bytes": stored.size_bytes,
        "content_type": stored.content_type,
        "row_count": row_count,
    }
