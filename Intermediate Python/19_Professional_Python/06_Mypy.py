from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from statistics import mean

_PYPROJECT_MYPY_SECTION = """\
[tool.mypy]
python_version = "3.12"
mypy_path = "src"
packages = ["scientific_app"]
strict = true
warn_unused_configs = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
no_implicit_optional = true
show_error_codes = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
"""


class MypyNotInstalledError(RuntimeError):
    """Raised when the `mypy` executable cannot be located on PATH."""


@dataclass(frozen=True)
class TypeCheckResult:
    """Outcome of a mypy invocation."""

    passed: bool
    return_code: int
    error_count: int
    report: str


def process_sample(sample_id: str, measurements: list[float]) -> float:
    """Compute the mean of a list of experimental measurements for one sample.

    Raises:
        ValueError: If `measurements` is empty or `sample_id` is blank.
    """
    if not sample_id.strip():
        raise ValueError("sample_id must not be blank")
    if not measurements:
        raise ValueError(f"no measurements provided for sample '{sample_id}'")
    return mean(measurements)


def normalize_measurements(measurements: list[float], reference: float) -> list[float]:
    """Normalize measurements against a reference value.

    Raises:
        ValueError: If `reference` is zero.
    """
    if reference == 0:
        raise ValueError("reference value must be non-zero")
    return [value / reference for value in measurements]


class TypeCheckRunner:
    """Subprocess-safe wrapper around the mypy static type checker CLI."""

    def __init__(self, project_root: Path | None = None, source_directory: str = "src") -> None:
        self.project_root: Path = project_root or Path.cwd()
        self.source_directory = source_directory

    @staticmethod
    def is_installed() -> bool:
        return shutil.which("mypy") is not None

    def check(self, targets: list[Path] | None = None) -> TypeCheckResult:
        if not self.is_installed():
            raise MypyNotInstalledError(
                "mypy is not installed. Add it as a development dependency "
                "(e.g. 'pip install mypy') to enable static type checking."
            )
        resolved_targets = [str(target) for target in (targets or [])] or [self.source_directory]
        result = subprocess.run(
            ["mypy", *resolved_targets],
            cwd=self.project_root,
            capture_output=True,
            text=True,
            check=False,
        )
        error_lines = [line for line in result.stdout.splitlines() if ": error:" in line]
        return TypeCheckResult(
            passed=result.returncode == 0,
            return_code=result.returncode,
            error_count=len(error_lines),
            report=result.stdout,
        )

    def pyproject_section(self) -> str:
        return _PYPROJECT_MYPY_SECTION

    @staticmethod
    def run() -> None:
        sample_mean = process_sample("SAMPLE-001", [1.2, 3.4, 2.9])
        normalized = normalize_measurements([1.2, 3.4, 2.9], reference=sample_mean)
        print(f"sample_mean={sample_mean:.4f}")
        print(f"normalized={normalized}")

        runner = TypeCheckRunner()
        if not runner.is_installed():
            print("mypy is not installed; skipping check. Install with 'pip install mypy'.")
            print("Recommended pyproject.toml section:")
            print(runner.pyproject_section())
            return

        result = runner.check(targets=[Path(__file__)])
        if result.passed:
            print("mypy check passed with no errors.")
        else:
            print(f"mypy check found {result.error_count} error(s):")
            print(result.report)


if __name__ == "__main__":
    TypeCheckRunner.run()
