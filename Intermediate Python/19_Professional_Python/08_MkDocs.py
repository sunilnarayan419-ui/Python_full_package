from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

_MKDOCS_YML_TEMPLATE = """\
site_name: {project_name}
site_description: Documentation for {project_name}
repo_url: {repo_url}

theme:
  name: material
  palette:
    scheme: default
  features:
    - navigation.sections
    - navigation.top
    - content.code.copy

nav:
  - Home: index.md
  - Installation: installation.md
  - Usage: usage.md
  - API Reference: api.md
  - Development: development.md

markdown_extensions:
  - admonition
  - pymdownx.highlight
  - pymdownx.superfences
  - toc:
      permalink: true

plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          options:
            show_source: true
            docstring_style: google
"""

_INDEX_MD_TEMPLATE = """\
# {project_name}

{description}

See [Installation](installation.md) to get started.
"""

_INSTALLATION_MD_TEMPLATE = """\
# Installation

```bash
pip install {package_name}
```

## Development Installation

```bash
git clone {repo_url}
cd {project_slug}
pip install -e ".[dev]"
```
"""

_USAGE_MD_TEMPLATE = """\
# Usage

```python
from {package_name} import pipeline

result = pipeline.run()
```
"""

_API_MD_TEMPLATE = """\
# API Reference

::: {package_name}
"""

_DEVELOPMENT_MD_TEMPLATE = """\
# Development

## Running Tests

```bash
pytest
```

## Quality Gates

```bash
ruff check .
black --check .
mypy src
```

## Building Documentation

```bash
mkdocs build --strict
```
"""


@dataclass(frozen=True)
class MkDocsProjectLayout:
    """Filesystem layout for an MkDocs documentation tree."""

    project_root: Path

    @property
    def mkdocs_yml(self) -> Path:
        return self.project_root / "mkdocs.yml"

    @property
    def docs_dir(self) -> Path:
        return self.project_root / "docs"


class MkDocsNotInstalledError(RuntimeError):
    """Raised when the `mkdocs` executable cannot be located on PATH."""


class MkDocsProjectBuilder:
    """Generates and validates a maintainable MkDocs documentation site."""

    def __init__(
        self,
        project_root: Path,
        project_name: str,
        package_name: str,
        repo_url: str,
        description: str = "Scientific computing and bioinformatics toolkit.",
    ) -> None:
        self.layout = MkDocsProjectLayout(project_root)
        self.project_name = project_name
        self.package_name = package_name
        self.repo_url = repo_url
        self.description = description

    @staticmethod
    def is_installed() -> bool:
        return shutil.which("mkdocs") is not None

    def generate_mkdocs_yml(self) -> str:
        return _MKDOCS_YML_TEMPLATE.format(project_name=self.project_name, repo_url=self.repo_url)

    def generate_index_md(self) -> str:
        return _INDEX_MD_TEMPLATE.format(project_name=self.project_name, description=self.description)

    def generate_installation_md(self) -> str:
        return _INSTALLATION_MD_TEMPLATE.format(
            package_name=self.package_name,
            repo_url=self.repo_url,
            project_slug=self.package_name.replace("_", "-"),
        )

    def generate_usage_md(self) -> str:
        return _USAGE_MD_TEMPLATE.format(package_name=self.package_name)

    def generate_api_md(self) -> str:
        return _API_MD_TEMPLATE.format(package_name=self.package_name)

    def generate_development_md(self) -> str:
        return _DEVELOPMENT_MD_TEMPLATE

    def write_project(self) -> MkDocsProjectLayout:
        self.layout.docs_dir.mkdir(parents=True, exist_ok=True)
        self.layout.mkdocs_yml.write_text(self.generate_mkdocs_yml(), encoding="utf-8")
        (self.layout.docs_dir / "index.md").write_text(self.generate_index_md(), encoding="utf-8")
        (self.layout.docs_dir / "installation.md").write_text(self.generate_installation_md(), encoding="utf-8")
        (self.layout.docs_dir / "usage.md").write_text(self.generate_usage_md(), encoding="utf-8")
        (self.layout.docs_dir / "api.md").write_text(self.generate_api_md(), encoding="utf-8")
        (self.layout.docs_dir / "development.md").write_text(self.generate_development_md(), encoding="utf-8")
        return self.layout

    def validate_build(self) -> subprocess.CompletedProcess[str]:
        if not self.is_installed():
            raise MkDocsNotInstalledError(
                "mkdocs is not installed. Add it as a development dependency "
                "(e.g. 'pip install mkdocs mkdocs-material mkdocstrings[python]') to validate the build."
            )
        return subprocess.run(
            ["mkdocs", "build", "--strict", "--site-dir", str(self.layout.project_root / "site")],
            cwd=self.layout.project_root,
            capture_output=True,
            text=True,
            check=False,
        )

    @staticmethod
    def run() -> None:
        builder = MkDocsProjectBuilder(
            project_root=Path("mkdocs_project"),
            project_name="Scientific App",
            package_name="scientific_app",
            repo_url="https://github.com/example-org/scientific-app",
        )
        layout = builder.write_project()
        print(f"MkDocs project written under: {layout.docs_dir}")

        if not builder.is_installed():
            print("mkdocs is not installed; skipping strict build validation. Install with 'pip install mkdocs mkdocs-material'.")
            return

        result = builder.validate_build()
        if result.returncode == 0:
            print("MkDocs strict build succeeded.")
        else:
            print("MkDocs strict build failed:")
            print(result.stderr)


if __name__ == "__main__":
    MkDocsProjectBuilder.run()
