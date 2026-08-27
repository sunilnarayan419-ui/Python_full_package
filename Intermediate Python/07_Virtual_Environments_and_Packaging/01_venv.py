"""Demonstrates Python's built-in venv module for creating isolated,
project-local virtual environments.

Where this fits: venv is the standard-library baseline for environment
isolation -- every dependency-management tool downstream (pip,
requirements files, Poetry, uv) ultimately operates inside an
environment created this way (or an equivalent). It ships with CPython,
requires no external installation, and is the correct default choice
when no additional project/dependency-management features are needed.

Production consideration: this module NEVER touches the interpreter
that is currently running it, nor any global site-packages. All
environments it creates are isolated under a caller-supplied directory
(a temporary directory by default) and are safe to discard.
"""

from __future__ import annotations

import sys
import venv
from dataclasses import dataclass
from pathlib import Path


class EnvironmentCreationError(RuntimeError):
    """Raised when a virtual environment could not be created or verified."""


@dataclass(frozen=True, slots=True)
class VirtualEnvironmentInfo:
    root: Path
    python_executable: Path


def _python_executable_path(env_root: Path) -> Path:
    """Returns the platform-appropriate path to the environment's
    Python executable, without hard-coding an OS-specific layout.
    """
    if sys.platform == "win32":
        return env_root / "Scripts" / "python.exe"
    return env_root / "bin" / "python"


def create_isolated_environment(env_root: Path) -> VirtualEnvironmentInfo:
    """Creates a new virtual environment at env_root using the stdlib venv API.

    Args:
        env_root: Directory in which to create the environment. Must not
            already exist as a populated, non-environment directory.

    Returns:
        VirtualEnvironmentInfo describing the created environment.

    Raises:
        EnvironmentCreationError: If the environment's Python executable
            is not present after creation, indicating creation failed.
    """
    builder = venv.EnvBuilder(with_pip=True, clear=False, symlinks=(sys.platform != "win32"))
    builder.create(str(env_root))

    python_executable = _python_executable_path(env_root)
    if not python_executable.exists():
        raise EnvironmentCreationError(
            f"environment creation appears to have failed: "
            f"expected interpreter at {python_executable}"
        )

    return VirtualEnvironmentInfo(root=env_root, python_executable=python_executable)


def demonstrate_isolation(info: VirtualEnvironmentInfo) -> bool:
    """Confirms the created environment has its own site-packages
    directory, separate from the current interpreter's -- this, not the
    interpreter binary's identity, is what makes dependency isolation
    possible. On platforms where venv symlinks its Python executable
    back to the system interpreter, comparing resolved binary paths
    would misleadingly suggest no isolation; site-packages separation
    is the property that actually matters.
    """
    pyvenv_cfg = info.root / "pyvenv.cfg"
    if not pyvenv_cfg.exists():
        return False

    env_site_packages = next(info.root.glob("lib/python*/site-packages"), None)
    if env_site_packages is None:
        env_site_packages = info.root / "Lib" / "site-packages"  # Windows layout

    python_dir_name = f"python{sys.version_info.major}.{sys.version_info.minor}"
    current_site_packages = Path(sys.prefix) / "lib" / python_dir_name / "site-packages"

    return env_site_packages.resolve() != current_site_packages.resolve()


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory(prefix="bioplatform_env_") as tmp_dir:
        env_root = Path(tmp_dir) / "genomics_pipeline_env"

        try:
            info = create_isolated_environment(env_root)
        except EnvironmentCreationError as exc:
            print(f"Environment creation failed: {exc}")
            raise SystemExit(1) from exc

        isolated = demonstrate_isolation(info)
        print(f"Created environment at: {info.root}")
        print(f"Environment interpreter: {info.python_executable}")
        print(f"Isolated from current interpreter: {isolated}")
        # TemporaryDirectory cleans up automatically; no global state touched.
