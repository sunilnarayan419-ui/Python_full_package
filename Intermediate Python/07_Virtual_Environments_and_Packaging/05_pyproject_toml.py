"""Demonstrates pyproject.toml as the central, modern Python project
metadata file, using the standard-library tomllib to read it.

Where this fits: pyproject.toml (PEP 517/518/621) is the single source
of truth for a project's build system, dependencies, and metadata,
superseding scattered setup.py/setup.cfg configuration. Every modern
tool in this stage (setuptools-as-backend, build, Poetry, uv) reads or
writes this file rather than inventing its own format.

IMPORTANT: tomllib (stdlib, Python 3.11+) is READ-ONLY -- it can parse
TOML but cannot write it. The example pyproject.toml content below is
therefore constructed as a plain string and written with pathlib, not
"generated" by tomllib.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path


class ProjectMetadataError(ValueError):
    """Raised when pyproject.toml is missing required metadata fields."""


# Realistic PEP 621 metadata for a bioinformatics analysis package.
EXAMPLE_PYPROJECT_TOML = """\
[build-system]
requires = ["setuptools>=69.0"]
build-backend = "setuptools.build_meta"

[project]
name = "genomics-variant-toolkit"
version = "0.4.0"
description = "Variant calling and annotation utilities for NGS pipelines"
readme = "README.md"
requires-python = ">=3.12"
license = { text = "MIT" }
dependencies = [
    "biopython>=1.83,<2.0",
    "numpy>=1.26,<2.0",
]

[project.optional-dependencies]
dev = ["pytest>=8.1", "mypy>=1.9"]
plotting = ["matplotlib>=3.8"]

[project.scripts]
variant-toolkit = "genomics_variant_toolkit.cli:main"

[tool.mypy]
strict = true
"""


@dataclass(frozen=True, slots=True)
class ProjectMetadata:
    name: str
    version: str
    requires_python: str
    runtime_dependencies: tuple[str, ...]
    optional_dependency_groups: tuple[str, ...]


def load_project_metadata(pyproject_path: Path) -> ProjectMetadata:
    """Reads and validates the [project] table of a pyproject.toml file.

    Raises:
        ProjectMetadataError: If required PEP 621 fields are missing.
    """
    with pyproject_path.open("rb") as handle:
        document = tomllib.load(handle)

    project_table = document.get("project")
    if project_table is None:
        raise ProjectMetadataError("pyproject.toml is missing the [project] table")

    for required_field in ("name", "version"):
        if required_field not in project_table:
            raise ProjectMetadataError(
                f"[project] table is missing required field '{required_field}'"
            )

    return ProjectMetadata(
        name=project_table["name"],
        version=project_table["version"],
        requires_python=project_table.get("requires-python", ""),
        runtime_dependencies=tuple(project_table.get("dependencies", [])),
        optional_dependency_groups=tuple(
            project_table.get("optional-dependencies", {}).keys()
        ),
    )


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory(prefix="bioplatform_pyproject_") as tmp_dir:
        pyproject_path = Path(tmp_dir) / "pyproject.toml"
        pyproject_path.write_text(EXAMPLE_PYPROJECT_TOML, encoding="utf-8")

        metadata = load_project_metadata(pyproject_path)
        print(f"Project: {metadata.name} v{metadata.version}")
        print(f"Requires Python: {metadata.requires_python}")
        print(f"Runtime dependencies: {list(metadata.runtime_dependencies)}")
        print(f"Optional dependency groups: {list(metadata.optional_dependency_groups)}")
