from __future__ import annotations

from release_gate import ReleaseGate


def test_gate_passes_when_all_checks_pass() -> None:
    gate = ReleaseGate()
    gate.register("schema_version", lambda: (True, "ok"))
    result = gate.run()
    assert result.passed
    assert result.failures == ()


def test_gate_collects_all_failures() -> None:
    gate = ReleaseGate()
    gate.register("schema_version", lambda: (False, "outdated"))
    gate.register("changelog", lambda: (False, "missing entry"))
    result = gate.run()
    assert not result.passed
    assert len(result.failures) == 2
