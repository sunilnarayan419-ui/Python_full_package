from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

_PYPROJECT_ISORT_SECTION = """\
[tool.isort]
profile = "black"
line_length = 100
src_paths = ["src", "tests"]
known_first_party = ["scientific_app"]
skip_gitignore = true
"""


class ImportSortOwner(Enum):
    """Which tool is authoritative for import ordering in this project."""

    RUFF = "ruff"
    ISORT = "isort"


class IsortNotInstalledError(RuntimeError):
    """Raised when the `isort` executable cannot be located on PATH."""


@dataclass(frozen=True)
class ImportSortResult:
    """Outcome of an isort invocation."""

    passed: bool
    return_code: int
    stdout: str
    stderr: str


class ImportSortManager:
    """Coordinates import-sorting responsibility between Ruff and isort.

    Running both Ruff's import-sort rules (I001) and isort simultaneously
    on the same codebase risks conflicting output. This manager exposes an
    explicit `owner` so a project declares exactly one authority; isort's
    CLI methods refuse to run when Ruff is configured as the owner.
    """

    def __init__(self, project_root: Path | None = None, owner: ImportSortOwner = ImportSortOwner.RUFF) -> None:
        self.project_root: Path = project_root or Path.cwd()
        self.owner = owner

    @staticmethod
    def is_installed() -> bool:
        return shutil.which("isort") is not None

    def _ensure_isort_is_owner(self) -> None:
        if self.owner is not ImportSortOwner.ISORT:
            raise RuntimeError(
                "isort is not the configured import-sort owner for this project "
                f"(current owner: {self.owner.value}). Update ImportSortOwner to ISORT "
                "before invoking isort directly, to avoid conflicting with Ruff."
            )

    def _run(self, args: list[str]) -> subprocess.CompletedProcess[str]:
        if not self.is_installed():
            raise IsortNotInstalledError(
                "isort is not installed. Add it as a development dependency "
                "(e.g. 'pip install isort') to enable import-sort checks."
            )
        return subprocess.run(
            ["isort", *args],
            cwd=self.project_root,
            capture_output=True,
            text=True,
            check=False,
        )

    def check(self, targets: list[Path] | None = None) -> ImportSortResult:
        self._ensure_isort_is_owner()
        resolved_targets = [str(target) for target in (targets or [])] or ["."]
        result = self._run(["--check-only", "--diff", *resolved_targets])
        return ImportSortResult(
            passed=result.returncode == 0,
            return_code=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
        )

    def format(self, targets: list[Path] | None = None) -> ImportSortResult:
        self._ensure_isort_is_owner()
        resolved_targets = [str(target) for target in (targets or [])] or ["."]
        result = self._run(resolved_targets)
        return ImportSortResult(
            passed=result.returncode == 0,
            return_code=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
        )

    def pyproject_section(self) -> str:
        return _PYPROJECT_ISORT_SECTION

    @staticmethod
    def run() -> None:
        manager = ImportSortManager(owner=ImportSortOwner.RUFF)
        print(f"Import-sort owner: {manager.owner.value}")

        if manager.owner is ImportSortOwner.RUFF:
            print("Ruff (rule set I001) manages import sorting; isort is not invoked to avoid conflicts.")
            return

        if not manager.is_installed():
            print("isort is not installed; skipping check. Install with 'pip install isort'.")
            print("Recommended pyproject.toml section:")
            print(manager.pyproject_section())
            return

        result = manager.check()
        print("isort check passed." if result.passed else "isort check found unsorted imports.")


if __name__ == "__main__":
    ImportSortManager.run()
