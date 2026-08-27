"""A safe, configurable file-organization utility.

Scans a source directory and organizes files into category
subdirectories by extension, with a mandatory dry-run mode and
careful handling of filename collisions. Never deletes user files.
"""

from __future__ import annotations

import logging
import shutil
from dataclasses import dataclass, field
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

CATEGORY_MAP: dict[str, str] = {
    ".jpg": "Images", ".jpeg": "Images", ".png": "Images", ".gif": "Images",
    ".bmp": "Images", ".svg": "Images", ".webp": "Images",
    ".pdf": "Documents", ".doc": "Documents", ".docx": "Documents",
    ".txt": "Documents", ".rtf": "Documents", ".odt": "Documents",
    ".xls": "Spreadsheets", ".xlsx": "Spreadsheets", ".csv": "Spreadsheets",
    ".mp3": "Audio", ".wav": "Audio", ".flac": "Audio", ".aac": "Audio",
    ".mp4": "Video", ".mkv": "Video", ".avi": "Video", ".mov": "Video",
    ".zip": "Archives", ".rar": "Archives", ".7z": "Archives", ".tar": "Archives",
    ".gz": "Archives",
    ".py": "Code", ".js": "Code", ".java": "Code", ".c": "Code", ".cpp": "Code",
    ".json": "Code", ".html": "Code", ".css": "Code",
}
DEFAULT_CATEGORY = "Other"


class FileOrganizerError(Exception):
    """Base exception for file-organization failures."""


class InvalidDirectoryError(FileOrganizerError):
    """Raised when the source directory is invalid or inaccessible."""


@dataclass(slots=True)
class OrganizeAction:
    """A single planned or executed file move."""

    source: Path
    destination: Path
    executed: bool = False
    error: str | None = None


@dataclass(slots=True)
class OrganizeSummary:
    """Aggregate results of an organization run."""

    dry_run: bool
    actions: list[OrganizeAction] = field(default_factory=list)

    @property
    def success_count(self) -> int:
        return sum(1 for a in self.actions if a.executed and not a.error)

    @property
    def error_count(self) -> int:
        return sum(1 for a in self.actions if a.error)

    def report(self) -> str:
        mode = "DRY RUN" if self.dry_run else "EXECUTED"
        lines = [f"=== {mode}: {len(self.actions)} file(s) processed ==="]
        for action in self.actions:
            status = "ERROR" if action.error else ("MOVED" if action.executed else "PLANNED")
            lines.append(f"[{status}] {action.source.name} -> {action.destination}")
            if action.error:
                lines.append(f"    reason: {action.error}")
        lines.append(f"Success: {self.success_count} | Errors: {self.error_count}")
        return "\n".join(lines)


class FileOrganizerService:
    """Business logic for scanning and organizing a directory of files."""

    def __init__(self, category_map: dict[str, str] | None = None) -> None:
        self._category_map = category_map or CATEGORY_MAP

    def plan(self, source_dir: Path) -> list[OrganizeAction]:
        """Compute the planned moves without touching the filesystem."""
        self._validate_directory(source_dir)
        actions: list[OrganizeAction] = []
        for entry in sorted(source_dir.iterdir()):
            if entry.is_dir():
                continue
            category = self._category_map.get(entry.suffix.lower(), DEFAULT_CATEGORY)
            destination_dir = source_dir / category
            destination = self._resolve_collision(destination_dir / entry.name)
            actions.append(OrganizeAction(source=entry, destination=destination))
        return actions

    def execute(self, source_dir: Path, dry_run: bool = True, copy: bool = False) -> OrganizeSummary:
        """Organize files in `source_dir`.

        When `dry_run` is True (the default), no filesystem changes are
        made and the plan is only reported. Set `copy=True` to copy files
        instead of moving them.
        """
        actions = self.plan(source_dir)
        summary = OrganizeSummary(dry_run=dry_run, actions=actions)

        if dry_run:
            return summary

        for action in actions:
            try:
                action.destination.parent.mkdir(parents=True, exist_ok=True)
                if copy:
                    shutil.copy2(action.source, action.destination)
                else:
                    shutil.move(str(action.source), str(action.destination))
                action.executed = True
            except OSError as exc:
                action.error = str(exc)
                logger.error("Failed to process %s: %s", action.source, exc)

        return summary

    @staticmethod
    def _resolve_collision(destination: Path) -> Path:
        if not destination.exists():
            return destination
        stem, suffix, parent = destination.stem, destination.suffix, destination.parent
        counter = 1
        candidate = parent / f"{stem}_{counter}{suffix}"
        while candidate.exists():
            counter += 1
            candidate = parent / f"{stem}_{counter}{suffix}"
        return candidate

    @staticmethod
    def _validate_directory(source_dir: Path) -> None:
        if not source_dir.exists():
            raise InvalidDirectoryError(f"Directory does not exist: {source_dir}")
        if not source_dir.is_dir():
            raise InvalidDirectoryError(f"Not a directory: {source_dir}")


def main() -> None:
    """Entry point for the interactive file organizer CLI."""
    print("=== File Organizer ===")
    raw_path = input("Enter the directory to organize: ").strip()
    source_dir = Path(raw_path).expanduser().resolve()

    service = FileOrganizerService()
    try:
        service._validate_directory(source_dir)
    except FileOrganizerError as exc:
        print(f"Error: {exc}")
        return

    copy_mode = input("Copy instead of move? (y/N): ").strip().lower() == "y"

    print("\nRunning a dry run first (no files will be changed)...\n")
    dry_summary = service.execute(source_dir, dry_run=True, copy=copy_mode)
    print(dry_summary.report())

    if not dry_summary.actions:
        print("\nNothing to organize.")
        return

    confirm = input("\nProceed with the actual operation? (y/N): ").strip().lower()
    if confirm != "y":
        print("Operation cancelled. No files were changed.")
        return

    real_summary = service.execute(source_dir, dry_run=False, copy=copy_mode)
    print("\n" + real_summary.report())


if __name__ == "__main__":
    main()
