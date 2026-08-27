from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

_PYPROJECT_RUFF_SECTION = """\
[tool.ruff]
line-length = 100
target-version = "py312"
src = ["src", "tests"]

[tool.ruff.lint]
select = ["E", "F", "W", "I", "UP", "B", "C4", "SIM", "N", "PL"]
ignore = ["PLR0913"]

[tool.ruff.lint.isort]
known-first-party = ["scientific_app"]
combine-as-imports = true

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
"""


class RuffNotInstalledError(RuntimeError):
    """Raised when the `ruff` executable cannot be located on PATH."""


@dataclass(frozen=True)
class RuffFinding:
    """A single Ruff diagnostic."""

    file_path: str
    rule_code: str
    message: str
    line: int


@dataclass(frozen=True)
class RuffRunResult:
    """Outcome of a Ruff invocation."""

    passed: bool
    return_code: int
    findings: tuple[RuffFinding, ...]
    stderr: str


class RuffLinter:
    """Subprocess-safe wrapper around the Ruff linter/formatter CLI.

    Ruff owns linting, import sorting (via its isort-compatible rule set),
    and optional formatting for this project, avoiding duplicated or
    conflicting configuration with a separate isort tool.
    """

    def __init__(self, project_root: Path | None = None) -> None:
        self.project_root: Path = project_root or Path.cwd()

    @staticmethod
    def is_installed() -> bool:
        return shutil.which("ruff") is not None

    def _run(self, args: list[str]) -> subprocess.CompletedProcess[str]:
        if not self.is_installed():
            raise RuffNotInstalledError(
                "ruff is not installed. Add it as a development dependency "
                "(e.g. 'pip install ruff') to enable linting and formatting checks."
            )
        return subprocess.run(
            ["ruff", *args],
            cwd=self.project_root,
            capture_output=True,
            text=True,
            check=False,
        )

    def lint(self, targets: list[Path] | None = None, *, fix: bool = False) -> RuffRunResult:
        resolved_targets = [str(target) for target in (targets or [])] or ["."]
        args = ["check", "--output-format=json", *resolved_targets]
        if fix:
            args.append("--fix")
        result = self._run(args)

        findings: list[RuffFinding] = []
        if result.stdout.strip():
            try:
                raw_findings = json.loads(result.stdout)
            except json.JSONDecodeError:
                raw_findings = []
            for entry in raw_findings:
                findings.append(
                    RuffFinding(
                        file_path=entry.get("filename", ""),
                        rule_code=entry.get("code") or "",
                        message=entry.get("message", ""),
                        line=entry.get("location", {}).get("row", 0),
                    )
                )
        return RuffRunResult(
            passed=result.returncode == 0,
            return_code=result.returncode,
            findings=tuple(findings),
            stderr=result.stderr,
        )

    def format_check(self, targets: list[Path] | None = None) -> RuffRunResult:
        resolved_targets = [str(target) for target in (targets or [])] or ["."]
        result = self._run(["format", "--check", *resolved_targets])
        return RuffRunResult(
            passed=result.returncode == 0,
            return_code=result.returncode,
            findings=(),
            stderr=result.stderr,
        )

    def pyproject_section(self) -> str:
        return _PYPROJECT_RUFF_SECTION

    @staticmethod
    def run() -> None:
        linter = RuffLinter()
        if not linter.is_installed():
            print("ruff is not installed; skipping checks. Install with 'pip install ruff'.")
            print("Recommended pyproject.toml section:")
            print(linter.pyproject_section())
            return

        lint_result = linter.lint()
        if lint_result.passed:
            print("Ruff lint check passed.")
        else:
            print(f"Ruff lint check found {len(lint_result.findings)} issue(s):")
            for finding in lint_result.findings[:20]:
                print(f"  {finding.file_path}:{finding.line} [{finding.rule_code}] {finding.message}")

        format_result = linter.format_check()
        print("Ruff format check passed." if format_result.passed else "Ruff format check found unformatted files.")


if __name__ == "__main__":
    RuffLinter.run()
