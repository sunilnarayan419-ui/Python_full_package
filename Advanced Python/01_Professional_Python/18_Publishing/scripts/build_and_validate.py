#!/usr/bin/env python3
"""Builds sdist + wheel for a package and validates the resulting
artifacts before any publish step — the kind of script a CI release
job invokes prior to `twine upload`.

Never publishes anything itself and never reads or embeds credentials;
authentication is handled entirely by the external `twine`/CI
environment via `TWINE_USERNAME`/`TWINE_PASSWORD` or a configured
`~/.pypirc`, neither of which this script touches.
"""
from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class BuildArtifact:
    path: Path
    sha256: str
    size_bytes: int


class BuildValidationError(Exception):
    pass


def clean_build_directories(project_root: Path) -> None:
    for directory_name in ("dist", "build"):
        target = project_root / directory_name
        if target.exists():
            shutil.rmtree(target)


def run_build(project_root: Path) -> None:
    result = subprocess.run(
        [sys.executable, "-m", "build"],
        cwd=project_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise BuildValidationError(f"build failed:\n{result.stdout}\n{result.stderr}")


def collect_artifacts(project_root: Path) -> list[BuildArtifact]:
    dist_dir = project_root / "dist"
    if not dist_dir.exists():
        raise BuildValidationError("dist/ directory was not created by the build")
    artifacts: list[BuildArtifact] = []
    for artifact_path in sorted(dist_dir.glob("*")):
        digest = hashlib.sha256(artifact_path.read_bytes()).hexdigest()
        artifacts.append(
            BuildArtifact(path=artifact_path, sha256=digest, size_bytes=artifact_path.stat().st_size)
        )
    if not artifacts:
        raise BuildValidationError("no build artifacts were produced")
    return artifacts


def validate_with_twine(project_root: Path) -> str:
    result = subprocess.run(
        [sys.executable, "-m", "twine", "check", "dist/*"],
        cwd=project_root,
        shell=False,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise BuildValidationError(f"twine check failed:\n{result.stdout}\n{result.stderr}")
    return result.stdout


def main(project_root: Path) -> int:
    clean_build_directories(project_root)
    run_build(project_root)
    artifacts = collect_artifacts(project_root)
    for artifact in artifacts:
        print(f"{artifact.path.name}  sha256={artifact.sha256}  ({artifact.size_bytes} bytes)")
    twine_output = validate_with_twine(project_root)
    print(twine_output)
    print("Build validated. Ready for a human-reviewed `twine upload` step (not run here).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(Path(__file__).resolve().parent.parent))
