from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

_PYPROJECT_BLACK_SECTION = """\
[tool.black]
line-length = 100
target-version = ["py312"]
include = '\\.pyi?$'
extend-exclude = '''
/(
    \\.venv
    | build
    | dist
)/
'''
"""


class BlackNotInstalledError(RuntimeError):
    """Raised when the `black` executable cannot be located on PATH."""


@dataclass(frozen=True)
class BlackRunResult:
    """Outcome of a Black invocation."""

    passed: bool
    return_code: int
    stdout: str
    stderr: str
    changed_files: tuple[str, ...]


class BlackFormatter:
    """Subprocess-safe wrapper around the Black code formatter CLI.

    This class never reimplements formatting logic; it only orchestrates
    the `black` executable, which must be installed separately (typically
    as a development dependency declared in `pyproject.toml`).
    """

    def __init__(self, project_root: Path | None = None, line_length: int = 100) -> None:
        self.project_root: Path = project_root or Path.cwd()
        self.line_length = line_length

    @staticmethod
    def is_installed() -> bool:
        return shutil.which("black") is not None

    def _run(self, targets: list[Path], *, extra_args: list[str]) -> subprocess.CompletedProcess[str]:
        if not self.is_installed():
            raise BlackNotInstalledError(
                "black is not installed. Add it as a development dependency "
                "(e.g. 'pip install black') to enable formatting checks."
            )
        resolved_targets = [str(target) for target in targets] or [str(self.project_root)]
        command = ["black", f"--line-length={self.line_length}", *extra_args, *resolved_targets]
        return subprocess.run(
            command,
            cwd=self.project_root,
            capture_output=True,
            text=True,
            check=False,
        )

    def check(self, targets: list[Path] | None = None) -> BlackRunResult:
        result = self._run(targets or [], extra_args=["--check", "--diff"])
        changed_files = tuple(
            line.split(" ", 2)[-1]
            for line in result.stderr.splitlines()
            if line.startswith("would reformat")
        )
        return BlackRunResult(
            passed=result.returncode == 0,
            return_code=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
            changed_files=changed_files,
        )

    def format(self, targets: list[Path] | None = None) -> BlackRunResult:
        result = self._run(targets or [], extra_args=[])
        changed_files = tuple(
            line.split(" ", 1)[-1]
            for line in result.stderr.splitlines()
            if line.startswith("reformatted")
        )
        return BlackRunResult(
            passed=result.returncode == 0,
            return_code=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
            changed_files=changed_files,
        )

    def pyproject_section(self) -> str:
        return _PYPROJECT_BLACK_SECTION

    @staticmethod
    def run() -> None:
        formatter = BlackFormatter(line_length=100)
        if not formatter.is_installed():
            print("black is not installed; skipping check. Install with 'pip install black'.")
            print("Recommended pyproject.toml section:")
            print(formatter.pyproject_section())
            return

        result = formatter.check()
        if result.passed:
            print("Black check passed: all files are already formatted.")
        else:
            print(f"Black check found {len(result.changed_files)} file(s) needing formatting.")
            for file_name in result.changed_files:
                print(f"  would reformat: {file_name}")


if __name__ == "__main__":
    BlackFormatter.run()
