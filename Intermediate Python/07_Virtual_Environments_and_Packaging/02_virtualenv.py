"""Demonstrates the third-party `virtualenv` tool and how it differs
from the standard-library `venv` module.

Where this fits: virtualenv predates venv (which was added in Python
3.3, itself based on virtualenv's design) and remains widely used in
industry because it is typically faster, supports older Python
versions, and offers more configurable environment creation (custom
seeders, app-data caching, broader platform/interpreter discovery).

venv vs virtualenv:
    - venv: standard library, zero install cost, sufficient for most
      modern single-version projects.
    - virtualenv: third-party, faster environment creation, used in
      CI pipelines and multi-interpreter tooling (e.g. tox) that need
      its extra features.

This module does NOT install virtualenv automatically. If it is not
available, it fails gracefully with an explanatory message rather than
raising a raw ImportError/FileNotFoundError to the caller.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


class VirtualenvUnavailableError(RuntimeError):
    """Raised when the virtualenv tool cannot be located on this system."""


class VirtualenvCreationError(RuntimeError):
    """Raised when virtualenv is available but environment creation fails."""


@dataclass(frozen=True, slots=True)
class VirtualenvInfo:
    root: Path
    python_executable: Path


def _find_virtualenv_executable() -> str:
    """Locates the virtualenv CLI without assuming it is installed."""
    executable = shutil.which("virtualenv")
    if executable is None:
        raise VirtualenvUnavailableError(
            "virtualenv is not installed in this environment. "
            "Install it explicitly (e.g. 'pip install virtualenv') if the "
            "extra features it provides over stdlib venv are needed."
        )
    return executable


def create_environment_with_virtualenv(env_root: Path) -> VirtualenvInfo:
    """Creates an isolated environment using the third-party virtualenv tool.

    Raises:
        VirtualenvUnavailableError: If virtualenv is not installed.
        VirtualenvCreationError: If virtualenv is installed but the
            environment creation subprocess fails.
    """
    virtualenv_executable = _find_virtualenv_executable()

    try:
        subprocess.run(
            [virtualenv_executable, str(env_root)],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        raise VirtualenvCreationError(
            f"virtualenv failed to create an environment at {env_root}: {exc.stderr}"
        ) from exc

    python_executable = (
        env_root / "Scripts" / "python.exe"
        if sys.platform == "win32"
        else env_root / "bin" / "python"
    )
    return VirtualenvInfo(root=env_root, python_executable=python_executable)


if __name__ == "__main__":
    with tempfile.TemporaryDirectory(prefix="bioplatform_virtualenv_") as tmp_dir:
        env_root = Path(tmp_dir) / "sequencing_toolkit_env"

        try:
            info = create_environment_with_virtualenv(env_root)
        except VirtualenvUnavailableError as exc:
            print(f"Skipping demonstration: {exc}")
        except VirtualenvCreationError as exc:
            print(f"Environment creation failed: {exc}")
        else:
            print(f"Created environment at: {info.root}")
            print(f"Environment interpreter: {info.python_executable}")
