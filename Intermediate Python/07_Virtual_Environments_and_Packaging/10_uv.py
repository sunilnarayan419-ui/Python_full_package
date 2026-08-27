"""Demonstrates uv, a modern, high-performance Python environment and
dependency management tool.

Where this fits: uv (from Astral) reimplements the roles of venv, pip,
pip-tools, and much of Poetry's workflow in a single, much faster,
Rust-based tool. It is not simply "a faster pip":

    - `uv venv` creates virtual environments (like stdlib venv, but
      faster).
    - `uv pip install` provides a pip-compatible installation interface
      operating on an environment.
    - `uv lock` / `uv sync` provide project-level dependency locking and
      reproducible environment synchronization, similar in spirit to
      Poetry's poetry.lock workflow, but built around pyproject.toml
      directly rather than a separate tool-specific project format.

pip alone installs packages one invocation at a time with no built-in
project-level lock file; uv's project workflow (`uv lock`/`uv sync`)
adds that reproducibility layer while remaining pip-CLI-compatible for
lower-level operations.

This module does NOT install uv automatically, does NOT modify global
Python configuration, and creates any demonstration environment inside
an isolated temporary directory only.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


class UvUnavailableError(RuntimeError):
    """Raised when the uv executable cannot be located on this system."""


class UvCommandError(RuntimeError):
    """Raised when an uv subprocess invocation fails."""


@dataclass(frozen=True, slots=True)
class UvEnvironmentInfo:
    root: Path
    python_executable: Path


def _find_uv_executable() -> str:
    executable = shutil.which("uv")
    if executable is None:
        raise UvUnavailableError(
            "uv is not installed. Install it separately "
            "(see docs.astral.sh/uv) to use its accelerated environment "
            "and dependency-locking workflows."
        )
    return executable


def check_uv_version() -> str:
    """Read-only check confirming uv is usable, without side effects.

    Raises:
        UvUnavailableError: If uv is not installed.
        UvCommandError: If uv is installed but fails to execute.
    """
    uv_executable = _find_uv_executable()
    try:
        result = subprocess.run(
            [uv_executable, "--version"],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        raise UvCommandError(f"uv --version failed: {exc.stderr}") from exc
    return result.stdout.strip()


def create_environment_with_uv(env_root: Path) -> UvEnvironmentInfo:
    """Creates an isolated virtual environment using `uv venv`.

    Raises:
        UvUnavailableError: If uv is not installed.
        UvCommandError: If environment creation fails.
    """
    uv_executable = _find_uv_executable()
    try:
        subprocess.run(
            [uv_executable, "venv", str(env_root)],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        raise UvCommandError(f"uv venv failed: {exc.stderr}") from exc

    python_executable = (
        env_root / "Scripts" / "python.exe"
        if sys.platform == "win32"
        else env_root / "bin" / "python"
    )
    return UvEnvironmentInfo(root=env_root, python_executable=python_executable)


if __name__ == "__main__":
    try:
        version = check_uv_version()
        print(f"uv is available: {version}")
    except UvUnavailableError as exc:
        print(f"Skipping live uv checks: {exc}")
        raise SystemExit(0)
    except UvCommandError as exc:
        print(f"uv check failed: {exc}")
        raise SystemExit(1) from exc

    with tempfile.TemporaryDirectory(prefix="bioplatform_uv_") as tmp_dir:
        env_root = Path(tmp_dir) / "structural_biology_env"
        try:
            info = create_environment_with_uv(env_root)
        except UvCommandError as exc:
            print(f"Environment creation failed: {exc}")
        else:
            print(f"Created environment at: {info.root}")
            print(f"Environment interpreter: {info.python_executable}")
            print(
                "Note: 'uv lock'/'uv sync' add project-level dependency "
                "locking on top of this environment layer -- a capability "
                "plain pip does not provide on its own."
            )
