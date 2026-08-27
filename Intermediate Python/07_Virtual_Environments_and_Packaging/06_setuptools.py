"""Demonstrates setuptools as a modern PEP 517 build BACKEND, configured
through pyproject.toml rather than a setup.py-first workflow.

Where this fits: setuptools is one of several possible build backends
(others include hatchling, flit-core, pdm-backend). A "build backend"
is the component that knows how to turn a source tree into sdist/wheel
artifacts; it is invoked by a build FRONTEND (see 07_Packaging.py,
which uses `python -m build`). setuptools is NOT itself a package
manager and does not resolve or install dependencies.

Legacy note: a bare `setup.py` with imperative `setup(...)` calls was
historically required. It is explicitly LEGACY here -- shown only for
recognition, not as the recommended modern approach. Modern projects
configure setuptools declaratively through [tool.setuptools] and
[project] tables in pyproject.toml.
"""

from __future__ import annotations

import tomllib
from pathlib import Path

# Modern (recommended): setuptools configured entirely through
# pyproject.toml, with automatic src-layout package discovery.
MODERN_SETUPTOOLS_PYPROJECT_TOML = """\
[build-system]
requires = ["setuptools>=69.0"]
build-backend = "setuptools.build_meta"

[project]
name = "plant-phenotyping-analysis"
version = "1.2.0"
description = "Image-derived plant phenotyping metrics for greenhouse trials"
requires-python = ">=3.12"
dependencies = ["numpy>=1.26,<2.0", "scikit-image>=0.22"]

[project.scripts]
phenotype-report = "plant_phenotyping_analysis.cli:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
plant_phenotyping_analysis = ["calibration/*.json"]
"""

# LEGACY EXAMPLE ONLY -- shown for recognition, not recommended for new
# projects. Retained here as a comment rather than executable code to
# avoid implying it is the preferred modern approach:
#
#   from setuptools import setup, find_packages
#
#   setup(
#       name="plant-phenotyping-analysis",
#       version="1.2.0",
#       packages=find_packages(where="src"),
#       package_dir={"": "src"},
#       install_requires=["numpy>=1.26,<2.0", "scikit-image>=0.22"],
#   )


class BuildBackendConfigError(ValueError):
    """Raised when a pyproject.toml's [build-system] table is invalid."""


def read_build_backend(pyproject_path: Path) -> str:
    """Extracts the configured build backend from pyproject.toml.

    Raises:
        BuildBackendConfigError: If [build-system] or build-backend is missing.
    """
    with pyproject_path.open("rb") as handle:
        document = tomllib.load(handle)

    build_system = document.get("build-system")
    if build_system is None or "build-backend" not in build_system:
        raise BuildBackendConfigError(
            "pyproject.toml must declare [build-system] with a build-backend"
        )
    return build_system["build-backend"]


def read_discovered_package_root(pyproject_path: Path) -> list[str]:
    """Reads the src-layout discovery root(s) configured for setuptools."""
    with pyproject_path.open("rb") as handle:
        document = tomllib.load(handle)

    setuptools_config = document.get("tool", {}).get("setuptools", {})
    packages_find = setuptools_config.get("packages", {}).get("find", {})
    return packages_find.get("where", [])


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory(prefix="bioplatform_setuptools_") as tmp_dir:
        pyproject_path = Path(tmp_dir) / "pyproject.toml"
        pyproject_path.write_text(MODERN_SETUPTOOLS_PYPROJECT_TOML, encoding="utf-8")

        backend = read_build_backend(pyproject_path)
        package_roots = read_discovered_package_root(pyproject_path)

        print(f"Configured build backend: {backend}")
        print(f"Package discovery root(s): {package_roots}")
        print(
            "Note: setuptools is a build backend, not a package manager -- "
            "it does not install dependencies or resolve version conflicts."
        )
