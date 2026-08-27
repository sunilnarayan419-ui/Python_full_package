from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

_PRE_COMMIT_CONFIG_TEMPLATE = """\
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: mixed-line-ending

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/psf/black
    rev: 24.10.0
    hooks:
      - id: black
        language_version: python3.12

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy
        additional_dependencies: []
        args: [--config-file=pyproject.toml]

default_language_version:
  python: python3.12

fail_fast: true
"""

_REQUIRED_TOP_LEVEL_KEYS: tuple[str, ...] = ("repos:", "default_language_version:", "fail_fast:")
_REQUIRED_REPO_URLS: tuple[str, ...] = (
    "https://github.com/pre-commit/pre-commit-hooks",
    "https://github.com/astral-sh/ruff-pre-commit",
    "https://github.com/psf/black",
    "https://github.com/pre-commit/mirrors-mypy",
)


@dataclass(frozen=True)
class PreCommitValidationResult:
    """Outcome of a structural validation pass over pre-commit configuration text."""

    is_valid: bool
    missing_keys: tuple[str, ...]
    missing_repos: tuple[str, ...]

    def summary(self) -> str:
        if self.is_valid:
            return "pre-commit configuration is structurally valid."
        problems = list(self.missing_keys) + list(self.missing_repos)
        return "pre-commit configuration is invalid, missing: " + ", ".join(problems)


class PreCommitConfigManager:
    """Generates and structurally validates `.pre-commit-config.yaml` content.

    Ruff performs linting, fixing, and formatting. Black performs canonical
    formatting for editors/tools that expect Black output specifically.
    Ruff's import-sorting rule set (I001) is intentionally relied upon
    instead of a separate isort hook, avoiding duplicate/conflicting
    import-ordering behavior between tools.
    """

    def __init__(self, project_root: Path | None = None) -> None:
        self.project_root: Path = project_root or Path.cwd()
        self.config_path: Path = self.project_root / ".pre-commit-config.yaml"

    def generate_config(self) -> str:
        return _PRE_COMMIT_CONFIG_TEMPLATE

    def validate_config(self, content: str) -> PreCommitValidationResult:
        missing_keys = tuple(key for key in _REQUIRED_TOP_LEVEL_KEYS if key not in content)
        missing_repos = tuple(url for url in _REQUIRED_REPO_URLS if url not in content)
        is_valid = not missing_keys and not missing_repos
        return PreCommitValidationResult(is_valid, missing_keys, missing_repos)

    def write_config(self) -> Path:
        content = self.generate_config()
        validation = self.validate_config(content)
        if not validation.is_valid:
            raise ValueError(validation.summary())
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.config_path.write_text(content, encoding="utf-8")
        return self.config_path

    @staticmethod
    def run() -> None:
        manager = PreCommitConfigManager()
        written_path = manager.write_config()
        validation = manager.validate_config(manager.generate_config())
        print(f"pre-commit configuration written to: {written_path}")
        print(validation.summary())


if __name__ == "__main__":
    PreCommitConfigManager.run()
