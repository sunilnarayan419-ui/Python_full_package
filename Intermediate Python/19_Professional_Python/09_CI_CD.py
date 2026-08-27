from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class QualityGateStatus(Enum):
    """Result state for a single CI/CD quality gate."""

    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass(frozen=True)
class QualityGate:
    """A single named validation stage in the pipeline (e.g. 'lint', 'test')."""

    name: str
    command: tuple[str, ...]
    required: bool = True
    depends_on: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class QualityGateResult:
    """Outcome of executing one quality gate."""

    gate_name: str
    status: QualityGateStatus
    detail: str = ""


class PipelineOrderingError(RuntimeError):
    """Raised when a pipeline definition has an invalid dependency graph."""


class CIPipelineDefinition:
    """Provider-agnostic representation of a fail-fast Python CI/CD pipeline.

    This class models the quality-gate architecture (formatting, linting,
    type checking, tests, coverage, build) independently of any specific
    CI vendor, so the same definition can drive GitHub Actions, GitLab CI,
    or another runner. It does not execute commands itself; a runner
    integration is responsible for that.
    """

    def __init__(self, gates: list[QualityGate] | None = None) -> None:
        self.gates: list[QualityGate] = gates or self._default_gates()
        self._validate_dependency_graph()

    @staticmethod
    def _default_gates() -> list[QualityGate]:
        return [
            QualityGate(name="format", command=("ruff", "format", "--check", ".")),
            QualityGate(name="lint", command=("ruff", "check", "."), depends_on=("format",)),
            QualityGate(
                name="type-check",
                command=("mypy", "src"),
                depends_on=("lint",),
            ),
            QualityGate(
                name="test",
                command=("pytest", "--cov=scientific_app", "--cov-report=term-missing"),
                depends_on=("type-check",),
            ),
            QualityGate(
                name="build",
                command=("python", "-m", "build"),
                depends_on=("test",),
            ),
        ]

    def _validate_dependency_graph(self) -> None:
        known_names = {gate.name for gate in self.gates}
        for gate in self.gates:
            for dependency in gate.depends_on:
                if dependency not in known_names:
                    raise PipelineOrderingError(
                        f"gate '{gate.name}' depends on unknown gate '{dependency}'"
                    )

    def execution_order(self) -> list[str]:
        """Topologically sorts gates by dependency, preserving declaration order among independents."""
        resolved: list[str] = []
        remaining = list(self.gates)
        while remaining:
            progressed = False
            for gate in list(remaining):
                if all(dependency in resolved for dependency in gate.depends_on):
                    resolved.append(gate.name)
                    remaining.remove(gate)
                    progressed = True
            if not progressed:
                unresolved_names = ", ".join(gate.name for gate in remaining)
                raise PipelineOrderingError(f"circular dependency detected among gates: {unresolved_names}")
        return resolved

    def evaluate_fail_fast(self, results: list[QualityGateResult]) -> bool:
        """Returns True only if every required gate passed; stops counting after the first failure."""
        results_by_name = {result.gate_name: result for result in results}
        for gate in self.gates:
            result = results_by_name.get(gate.name)
            if result is None:
                if gate.required:
                    return False
                continue
            if gate.required and result.status is not QualityGateStatus.PASSED:
                return False
        return True

    def render_summary(self, results: list[QualityGateResult]) -> str:
        lines = ["CI/CD Pipeline Summary", "=" * 23]
        for result in results:
            lines.append(f"[{result.status.value.upper():7s}] {result.gate_name}: {result.detail}")
        overall = "PASSED" if self.evaluate_fail_fast(results) else "FAILED"
        lines.append(f"Overall: {overall}")
        return "\n".join(lines)

    @staticmethod
    def run() -> None:
        pipeline = CIPipelineDefinition()
        print("Execution order (dependency-resolved):")
        for stage_name in pipeline.execution_order():
            print(f"  -> {stage_name}")

        simulated_results = [
            QualityGateResult("format", QualityGateStatus.PASSED, "no formatting issues"),
            QualityGateResult("lint", QualityGateStatus.PASSED, "0 lint violations"),
            QualityGateResult("type-check", QualityGateStatus.PASSED, "0 type errors"),
            QualityGateResult("test", QualityGateStatus.PASSED, "128 passed, 94% coverage"),
            QualityGateResult("build", QualityGateStatus.PASSED, "wheel and sdist built"),
        ]
        print()
        print(pipeline.render_summary(simulated_results))


if __name__ == "__main__":
    CIPipelineDefinition.run()
