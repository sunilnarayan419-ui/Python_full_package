"""Demonstrates Poetry as a Python project/dependency management tool.

Where this fits: Poetry manages an entire project's dependency graph,
lock file, virtual environment, and build/publish workflow through one
pyproject.toml-centric CLI. It is NOT simply a replacement for pip --

    - pip installs whatever packages you tell it to, one invocation at
      a time, with no built-in concept of a locked, resolved dependency
      graph for your project.
    - Poetry resolves your entire declared dependency set into a
      poetry.lock file (a full, reproducible dependency graph with
      exact versions and hashes), manages a dedicated virtual
      environment for the project, and can build/publish the project
      itself -- capabilities pip alone does not provide.

This module does NOT install Poetry automatically and does NOT modify
any real project. If Poetry is unavailable, it fails gracefully with a
clear message. Where subprocess calls are demonstrated, they use safe,
non-destructive Poetry subcommands only.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

# Example pyproject.toml section as Poetry would generate/consume it --
# note Poetry's own [tool.poetry] table alongside PEP 621 [project] data
# in modern Poetry versions.
EXAMPLE_POETRY_PYPROJECT_TOML = """\
[tool.poetry]
name = "proteomics-pipeline"
version = "0.3.0"
description = "Mass-spectrometry proteomics data processing pipeline"
authors = ["Scientific Platform Team"]

[tool.poetry.dependencies]
python = "^3.12"
biopython = "^1.83"
numpy = "^1.26"

[tool.poetry.group.dev.dependencies]
pytest = "^8.1"
mypy = "^1.9"

[build-system]
requires = ["poetry-core>=1.9.0"]
build-backend = "poetry.core.masonry.api"
"""


class PoetryUnavailableError(RuntimeError):
    """Raised when the Poetry executable cannot be located."""


class PoetryCommandError(RuntimeError):
    """Raised when a Poetry subprocess invocation fails."""


@dataclass(frozen=True, slots=True)
class PoetryProjectInfo:
    name: str
    version: str


def _find_poetry_executable() -> str:
    executable = shutil.which("poetry")
    if executable is None:
        raise PoetryUnavailableError(
            "Poetry is not installed. Install it separately "
            "(see python-poetry.org) if project-level dependency locking "
            "and environment management are needed beyond plain pip."
        )
    return executable


def check_poetry_version() -> str:
    """Read-only, non-destructive check confirming Poetry is usable.

    Raises:
        PoetryUnavailableError: If Poetry is not installed.
        PoetryCommandError: If Poetry is installed but fails to run.
    """
    poetry_executable = _find_poetry_executable()
    try:
        result = subprocess.run(
            [poetry_executable, "--version"],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        raise PoetryCommandError(f"poetry --version failed: {exc.stderr}") from exc
    return result.stdout.strip()


def initialize_demo_project(project_root: Path) -> None:
    """Writes a Poetry-managed pyproject.toml into an isolated temporary
    project directory. Does NOT run `poetry install` or touch any real
    environment, keeping the demonstration side-effect-free.
    """
    project_root.mkdir(parents=True, exist_ok=True)
    (project_root / "pyproject.toml").write_text(
        EXAMPLE_POETRY_PYPROJECT_TOML, encoding="utf-8"
    )


if __name__ == "__main__":
    try:
        version = check_poetry_version()
        print(f"Poetry is available: {version}")
    except PoetryUnavailableError as exc:
        print(f"Skipping live Poetry checks: {exc}")
    except PoetryCommandError as exc:
        print(f"Poetry check failed: {exc}")

    with tempfile.TemporaryDirectory(prefix="bioplatform_poetry_") as tmp_dir:
        project_root = Path(tmp_dir) / "proteomics_pipeline"
        initialize_demo_project(project_root)
        print(f"\nDemo Poetry project scaffolded at: {project_root}")
        print(
            "Distinction: Poetry resolves + locks the full dependency graph "
            "into poetry.lock and manages the project's own virtual "
            "environment; pip only installs the packages it is told to, "
            "with no project-level locking of its own."
        )
