from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

_SUPPORTED_PYTHON_VERSIONS: tuple[str, ...] = ("3.12", "3.13")

_WORKFLOW_TEMPLATE = """\
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ci-${{{{ github.workflow }}}}-${{{{ github.ref }}}}
  cancel-in-progress: true

env:
  PYTHONUNBUFFERED: "1"

jobs:
  lint:
    name: Lint (Ruff + Black)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip

      - name: Install dependencies
        run: pip install -e ".[dev]"

      - name: Ruff check
        run: ruff check .

      - name: Ruff format check
        run: ruff format --check .

      - name: Black check
        run: black --check .

  type-check:
    name: Type Check (mypy)
    runs-on: ubuntu-latest
    needs: [lint]
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip

      - name: Install dependencies
        run: pip install -e ".[dev]"

      - name: mypy
        run: mypy src

  test:
    name: Test (Python ${{{{ matrix.python-version }}}})
    runs-on: ubuntu-latest
    needs: [type-check]
    strategy:
      fail-fast: true
      matrix:
        python-version: {python_versions}
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{{{ matrix.python-version }}}}
          cache: pip

      - name: Install dependencies
        run: pip install -e ".[dev]"

      - name: Run tests with coverage
        run: pytest --cov=scientific_app --cov-report=xml --cov-report=term-missing

      - name: Upload coverage report
        uses: actions/upload-artifact@v4
        with:
          name: coverage-py${{{{ matrix.python-version }}}}
          path: coverage.xml
          retention-days: 14

  build:
    name: Build Distribution
    runs-on: ubuntu-latest
    needs: [test]
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip

      - name: Install build tooling
        run: pip install build

      - name: Build sdist and wheel
        run: python -m build

      - name: Upload build artifacts
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/
          retention-days: 14

  publish:
    name: Publish Release
    runs-on: ubuntu-latest
    needs: [build]
    if: github.event_name == 'push' && startsWith(github.ref, 'refs/tags/v')
    environment: release
    permissions:
      id-token: write
    steps:
      - uses: actions/checkout@v4

      - name: Download build artifacts
        uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
"""


@dataclass(frozen=True)
class GitHubActionsWorkflowConfig:
    """Configuration for the generated `.github/workflows/ci.yml` workflow."""

    python_versions: tuple[str, ...] = _SUPPORTED_PYTHON_VERSIONS
    workflow_path: Path = Path(".github/workflows/ci.yml")


class GitHubActionsWorkflowGenerator:
    """Generates a professional, fail-fast GitHub Actions CI/CD workflow.

    Job graph: lint -> type-check -> test (matrix) -> build -> publish.
    Each job declares `needs:` on its predecessor so a failure in an
    earlier quality gate prevents later, more expensive jobs from running.
    Publishing is gated behind a tag-based condition and a protected
    `release` environment; it never runs on ordinary branch pushes.
    """

    def __init__(self, config: GitHubActionsWorkflowConfig | None = None) -> None:
        self.config = config or GitHubActionsWorkflowConfig()

    def generate_workflow(self) -> str:
        matrix_literal = "[" + ", ".join(f'"{version}"' for version in self.config.python_versions) + "]"
        return _WORKFLOW_TEMPLATE.format(python_versions=matrix_literal)

    def validate_job_graph(self, content: str) -> bool:
        required_job_headers = ("lint:", "type-check:", "test:", "build:", "publish:")
        required_needs_relationships = (
            "needs: [lint]",
            "needs: [type-check]",
            "needs: [test]",
            "needs: [build]",
        )
        has_all_jobs = all(header in content for header in required_job_headers)
        has_all_dependencies = all(relationship in content for relationship in required_needs_relationships)
        has_safe_publish_condition = "startsWith(github.ref, 'refs/tags/v')" in content
        return has_all_jobs and has_all_dependencies and has_safe_publish_condition

    def write_workflow(self, project_root: Path) -> Path:
        content = self.generate_workflow()
        if not self.validate_job_graph(content):
            raise ValueError("generated workflow failed structural validation")
        output_path = project_root / self.config.workflow_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")
        return output_path

    @staticmethod
    def run() -> None:
        generator = GitHubActionsWorkflowGenerator()
        written_path = generator.write_workflow(Path("."))
        is_valid = generator.validate_job_graph(generator.generate_workflow())
        print(f"GitHub Actions workflow written to: {written_path}")
        print(f"Job graph validation: {'passed' if is_valid else 'failed'}")


if __name__ == "__main__":
    GitHubActionsWorkflowGenerator.run()
