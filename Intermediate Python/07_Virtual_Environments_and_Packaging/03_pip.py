"""Demonstrates professional use of pip as the Python package installer.

Where this fits: pip installs and manages individual packages inside
whatever environment it is invoked in. It is NOT a project/metadata
manager -- it does not define what your project's dependencies *are*
(that is pyproject.toml's job) and it does not lock a dependency graph
by default (that is what requirements files with pinned hashes, or
tools like Poetry/uv, are for). pip is the installation mechanism at
the bottom of that stack.

All commands below run via subprocess.run() with explicit argument
lists (never shell=True), captured output, and checked return codes,
targeting the current interpreter's environment for inspection-only
operations.
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass


class PipCommandError(RuntimeError):
    """Raised when a pip subprocess invocation fails."""


@dataclass(frozen=True, slots=True)
class InstalledPackage:
    name: str
    version: str


def _run_pip(args: list[str]) -> str:
    """Runs `python -m pip <args>` safely and returns captured stdout.

    Uses `sys.executable -m pip` rather than a bare `pip` command so the
    invocation always targets the currently active interpreter's
    environment, avoiding accidental use of an unrelated pip on PATH.
    """
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", *args],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise PipCommandError("pip is not available for this interpreter") from exc
    except subprocess.CalledProcessError as exc:
        raise PipCommandError(f"pip {' '.join(args)} failed: {exc.stderr}") from exc
    return result.stdout


def list_installed_packages() -> list[InstalledPackage]:
    """Inspects currently installed packages without modifying the
    environment -- a read-only, always-safe demonstration of pip usage.
    """
    output = _run_pip(["list", "--format=freeze"])
    packages: list[InstalledPackage] = []
    for line in output.splitlines():
        if "==" not in line:
            continue
        name, _, version = line.partition("==")
        packages.append(InstalledPackage(name=name, version=version))
    return packages


def show_package_metadata(package_name: str) -> str:
    """Inspects metadata for a single installed package via `pip show`."""
    return _run_pip(["show", package_name])


def freeze_environment() -> str:
    """Produces a `pip freeze`-equivalent snapshot, the basis for a
    requirements.txt lockfile-style export (see 04_requirements.py for
    how such output is consumed as a reproducibility artifact).
    """
    return _run_pip(["freeze"])


if __name__ == "__main__":
    try:
        installed = list_installed_packages()
    except PipCommandError as exc:
        print(f"Could not inspect environment: {exc}")
        raise SystemExit(1) from exc

    print(f"Installed package count: {len(installed)}")
    for package in installed[:5]:
        print(f"  {package.name}=={package.version}")

    if installed:
        sample_package = installed[0].name
        try:
            metadata = show_package_metadata(sample_package)
            first_line = metadata.splitlines()[0] if metadata else ""
            print(f"\nSample metadata lookup for '{sample_package}': {first_line}")
        except PipCommandError as exc:
            print(f"Metadata lookup failed: {exc}")
