"""Demonstrates requirements-file conventions for dependency pinning and
reproducible deployment environments.

Where this fits: requirements files (requirements.txt,
requirements-dev.txt) are an installation manifest consumed by pip --
they are NOT project metadata. pyproject.toml declares what a package
*is* and what it *depends on* in the abstract (e.g. "numpy>=1.26");
a requirements file pins those declarations (or a full transitive
closure) to exact, reproducible versions for a specific deployment
target (e.g. "numpy==1.26.4").

Distinguishing pinning strategies:
    - Exact pin  ("numpy==1.26.4"): maximally reproducible, used for
      deployment/production environments.
    - Compatible range ("numpy>=1.26,<2.0"): used in library
      dependency declarations to avoid over-constraining consumers.
    - Unpinned ("numpy"): acceptable only for quick local exploration,
      never for reproducible deployments -- invites dependency drift.
"""

from __future__ import annotations

from dataclasses import dataclass


class RequirementParseError(ValueError):
    """Raised when a requirement line cannot be parsed into its parts."""


@dataclass(frozen=True, slots=True)
class PinnedRequirement:
    name: str
    version: str


# Realistic runtime requirements for a genomics data-processing service.
# Exact pins: this file targets a reproducible deployment environment.
PRODUCTION_REQUIREMENTS = """\
biopython==1.83
numpy==1.26.4
pandas==2.2.1
scikit-learn==1.4.1.post1
networkx==3.2.1
"""

# Development-only tooling: never installed in production containers.
# Kept in a separate file so runtime images stay minimal and auditable.
DEVELOPMENT_REQUIREMENTS = """\
-r requirements.txt
pytest==8.1.1
mypy==1.9.0
flake8==7.0.0
build==1.2.1
"""


def parse_pinned_requirements(requirements_text: str) -> list[PinnedRequirement]:
    """Parses simple `name==version` lines, skipping comments, blank
    lines, and `-r other_file.txt` includes.

    Raises:
        RequirementParseError: If a non-comment, non-include line does
            not use exact pinning (`==`), since this parser is intended
            for validating deployment-grade pinned requirement sets.
    """
    pinned: list[PinnedRequirement] = []
    for raw_line in requirements_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith("-r"):
            continue
        if "==" not in line:
            raise RequirementParseError(f"expected an exact pin, got: '{line}'")
        name, _, version = line.partition("==")
        pinned.append(PinnedRequirement(name=name.strip(), version=version.strip()))
    return pinned


def detect_drift(
    pinned: list[PinnedRequirement], installed: dict[str, str]
) -> list[str]:
    """Compares pinned requirements against an installed-package mapping
    and reports mismatches -- the core check that catches dependency
    drift between what a requirements file declares and what an
    environment actually has installed.
    """
    mismatches = []
    for requirement in pinned:
        installed_version = installed.get(requirement.name)
        if installed_version is None:
            mismatches.append(f"{requirement.name}: not installed")
        elif installed_version != requirement.version:
            mismatches.append(
                f"{requirement.name}: pinned {requirement.version}, "
                f"installed {installed_version}"
            )
    return mismatches


if __name__ == "__main__":
    pinned = parse_pinned_requirements(PRODUCTION_REQUIREMENTS)
    print(f"Parsed {len(pinned)} pinned production requirements:")
    for requirement in pinned:
        print(f"  {requirement.name}=={requirement.version}")

    # Simulated installed environment, standing in for a real `pip freeze`
    # result, to demonstrate drift detection without depending on what
    # happens to be installed on the machine running this file.
    simulated_installed = {
        "biopython": "1.83",
        "numpy": "1.26.4",
        "pandas": "2.1.0",  # intentionally drifted from the pin
        "scikit-learn": "1.4.1.post1",
        # networkx intentionally missing entirely
    }

    drift = detect_drift(pinned, simulated_installed)
    print("\nDependency drift detected:" if drift else "\nNo dependency drift detected.")
    for issue in drift:
        print(f"  {issue}")
