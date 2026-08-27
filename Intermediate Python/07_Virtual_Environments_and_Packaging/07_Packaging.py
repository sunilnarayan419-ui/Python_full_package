"""Demonstrates the complete Python packaging lifecycle:

    source tree -> pyproject.toml -> build backend -> sdist + wheel -> validate

Where this fits: `python -m build` is the recommended build FRONTEND
-- a thin tool that invokes whatever backend pyproject.toml declares
(setuptools, hatchling, etc.) via the standard PEP 517 interface,
producing both a source distribution and a wheel without requiring
project-specific build scripts.

sdist (.tar.gz) vs wheel (.whl):
    - sdist contains the project source and enough metadata to build
      it; installing from an sdist may require a build step.
    - wheel is a prebuilt, ready-to-install distribution; installing
      from a wheel is generally faster and avoids invoking the build
      backend at install time when a compatible wheel is available.
      Wheels do not eliminate every build requirement across all
      ecosystems (e.g. packages with compiled extensions may still
      need platform-specific wheels or a source build).

This module builds into a temporary directory only. It never publishes
anything (see 08_Publishing_Packages.py for that stage) and never
writes into the caller's real project directory.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

MINIMAL_PACKAGE_PYPROJECT_TOML = """\
[build-system]
requires = ["setuptools>=69.0"]
build-backend = "setuptools.build_meta"

[project]
name = "microbial-growth-kinetics"
version = "0.1.0"
description = "Growth-curve fitting utilities for microbial culture assays"
requires-python = ">=3.12"
dependencies = []
"""

MINIMAL_PACKAGE_INIT = '''"""Growth-curve fitting utilities."""

__all__ = ["logistic_growth"]


def logistic_growth(t: float, carrying_capacity: float, rate: float) -> float:
    """Evaluates a simple logistic growth model at time t."""
    import math

    return carrying_capacity / (1 + math.exp(-rate * t))
'''


class BuildToolUnavailableError(RuntimeError):
    """Raised when the `build` package is not installed for this interpreter."""


class PackageBuildError(RuntimeError):
    """Raised when the build process fails."""


@dataclass(frozen=True, slots=True)
class BuildArtifacts:
    sdist_paths: tuple[Path, ...]
    wheel_paths: tuple[Path, ...]


def _scaffold_minimal_package(project_root: Path) -> None:
    (project_root / "src" / "microbial_growth_kinetics").mkdir(parents=True)
    (project_root / "pyproject.toml").write_text(
        MINIMAL_PACKAGE_PYPROJECT_TOML, encoding="utf-8"
    )
    (project_root / "src" / "microbial_growth_kinetics" / "__init__.py").write_text(
        MINIMAL_PACKAGE_INIT, encoding="utf-8"
    )


def build_distributions(project_root: Path, output_dir: Path) -> BuildArtifacts:
    """Invokes `python -m build` against project_root, writing sdist and
    wheel artifacts into output_dir.

    Raises:
        BuildToolUnavailableError: If the `build` package is not
            importable for the current interpreter.
        PackageBuildError: If the build subprocess fails.
    """
    try:
        import build  # noqa: F401  -- import only to verify availability
    except ImportError as exc:
        raise BuildToolUnavailableError(
            "the 'build' package is not installed; install it in a "
            "development environment with 'pip install build' to run "
            "this demonstration end-to-end"
        ) from exc

    try:
        subprocess.run(
            [sys.executable, "-m", "build", str(project_root), "--outdir", str(output_dir)],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        raise PackageBuildError(f"build failed: {exc.stderr}") from exc

    sdist_paths = tuple(output_dir.glob("*.tar.gz"))
    wheel_paths = tuple(output_dir.glob("*.whl"))
    return BuildArtifacts(sdist_paths=sdist_paths, wheel_paths=wheel_paths)


if __name__ == "__main__":
    with tempfile.TemporaryDirectory(prefix="bioplatform_build_") as tmp_dir:
        project_root = Path(tmp_dir) / "microbial_growth_kinetics"
        output_dir = Path(tmp_dir) / "dist"
        project_root.mkdir()
        output_dir.mkdir()

        _scaffold_minimal_package(project_root)

        try:
            artifacts = build_distributions(project_root, output_dir)
        except BuildToolUnavailableError as exc:
            print(f"Skipping build demonstration: {exc}")
        except PackageBuildError as exc:
            print(f"Build failed: {exc}")
        else:
            print(f"sdist artifacts: {[p.name for p in artifacts.sdist_paths]}")
            print(f"wheel artifacts: {[p.name for p in artifacts.wheel_paths]}")
        finally:
            shutil.rmtree(project_root, ignore_errors=True)
