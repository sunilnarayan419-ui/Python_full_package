from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

_CONF_PY_TEMPLATE = """\
from __future__ import annotations

project = "{project_name}"
author = "{author}"
copyright = "{year}, {author}"
release = "{version}"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]

napoleon_google_docstring = True
napoleon_numpy_docstring = True
autodoc_typehints = "description"
autodoc_member_order = "bysource"

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "furo"
html_static_path = ["_static"]

intersphinx_mapping = {{
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
}}
"""

_INDEX_RST_TEMPLATE = """\
{project_name} Documentation
{title_underline}

.. toctree::
   :maxdepth: 2
   :caption: Contents

   usage
   api

Indices and tables
===================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""

_API_RST_TEMPLATE = """\
API Reference
=============

.. automodule:: {package_name}
   :members:
   :undoc-members:
   :show-inheritance:
"""

_USAGE_RST_TEMPLATE = """\
Usage
=====

Installation
------------

.. code-block:: bash

   pip install {package_name}

Quick Start
-----------

.. code-block:: python

   from {package_name} import pipeline

   result = pipeline.run()
"""


@dataclass(frozen=True)
class SphinxDocumentationLayout:
    """Filesystem layout for a Sphinx documentation tree rooted at `docs_root`."""

    docs_root: Path

    @property
    def source_dir(self) -> Path:
        return self.docs_root / "source"

    @property
    def build_dir(self) -> Path:
        return self.docs_root / "build"

    @property
    def conf_py(self) -> Path:
        return self.source_dir / "conf.py"

    @property
    def index_rst(self) -> Path:
        return self.source_dir / "index.rst"

    @property
    def api_rst(self) -> Path:
        return self.source_dir / "api.rst"

    @property
    def usage_rst(self) -> Path:
        return self.source_dir / "usage.rst"


class SphinxNotInstalledError(RuntimeError):
    """Raised when the `sphinx-build` executable cannot be located on PATH."""


class SphinxDocumentationBuilder:
    """Generates and builds a maintainable Sphinx API-documentation tree."""

    def __init__(
        self,
        docs_root: Path,
        project_name: str,
        package_name: str,
        author: str,
        version: str = "0.1.0",
        year: str = "2026",
    ) -> None:
        self.layout = SphinxDocumentationLayout(docs_root)
        self.project_name = project_name
        self.package_name = package_name
        self.author = author
        self.version = version
        self.year = year

    @staticmethod
    def is_installed() -> bool:
        return shutil.which("sphinx-build") is not None

    def generate_conf_py(self) -> str:
        return _CONF_PY_TEMPLATE.format(
            project_name=self.project_name,
            author=self.author,
            year=self.year,
            version=self.version,
        )

    def generate_index_rst(self) -> str:
        title = f"{self.project_name} Documentation"
        return _INDEX_RST_TEMPLATE.format(project_name=self.project_name, title_underline="=" * len(title))

    def generate_api_rst(self) -> str:
        return _API_RST_TEMPLATE.format(package_name=self.package_name)

    def generate_usage_rst(self) -> str:
        return _USAGE_RST_TEMPLATE.format(package_name=self.package_name)

    def write_sources(self) -> SphinxDocumentationLayout:
        self.layout.source_dir.mkdir(parents=True, exist_ok=True)
        self.layout.conf_py.write_text(self.generate_conf_py(), encoding="utf-8")
        self.layout.index_rst.write_text(self.generate_index_rst(), encoding="utf-8")
        self.layout.api_rst.write_text(self.generate_api_rst(), encoding="utf-8")
        self.layout.usage_rst.write_text(self.generate_usage_rst(), encoding="utf-8")
        return self.layout

    def build_html(self) -> subprocess.CompletedProcess[str]:
        if not self.is_installed():
            raise SphinxNotInstalledError(
                "sphinx-build is not installed. Add Sphinx as a development dependency "
                "(e.g. 'pip install sphinx furo') to enable documentation builds."
            )
        self.layout.build_dir.mkdir(parents=True, exist_ok=True)
        return subprocess.run(
            ["sphinx-build", "-b", "html", str(self.layout.source_dir), str(self.layout.build_dir / "html")],
            capture_output=True,
            text=True,
            check=False,
        )

    @staticmethod
    def run() -> None:
        builder = SphinxDocumentationBuilder(
            docs_root=Path("docs"),
            project_name="Scientific App",
            package_name="scientific_app",
            author="Scientific App Contributors",
        )
        layout = builder.write_sources()
        print(f"Sphinx sources written under: {layout.source_dir}")

        if not builder.is_installed():
            print("sphinx-build is not installed; skipping HTML build. Install with 'pip install sphinx furo'.")
            return

        result = builder.build_html()
        if result.returncode == 0:
            print(f"Sphinx HTML build succeeded: {layout.build_dir / 'html'}")
        else:
            print("Sphinx HTML build failed:")
            print(result.stderr)


if __name__ == "__main__":
    SphinxDocumentationBuilder.run()
