"""Demonstrates a systematic debugging workflow applied to a genomic
sequence analysis routine.

Workflow: Reproduce -> Isolate -> Inspect state -> Root cause -> Fix -> Verify.

The defective version is preserved (renamed and clearly isolated) purely
to document the debugging process; the exported, callable implementation
is the corrected one.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GcContentResult:
    sequence_id: str
    gc_fraction: float
    length: int


# ---------------------------------------------------------------------------
# STEP 1: Reproduce
#
# Bug report: "GC content for short sequences containing lowercase bases
# comes back wrong." The defective implementation below reproduces that
# report deterministically so the failure can be isolated.
# ---------------------------------------------------------------------------


def _gc_content_defective(sequence: str) -> float:
    gc_count = 0
    for base in sequence:
        if base in ("G", "C"):  # BUG: does not account for lowercase bases
            gc_count += 1
    return gc_count / len(sequence)


def _reproduce_bug() -> tuple[str, float]:
    sequence = "gcGC"  # mixed-case, unambiguous expected GC fraction of 1.0
    observed = _gc_content_defective(sequence)
    return sequence, observed


# ---------------------------------------------------------------------------
# STEP 2-4: Isolate, inspect state, identify root cause
#
# _diagnose() reproduces the failure inside a controlled, inspectable
# scope: it records the intermediate per-base classification so the root
# cause (case-sensitive comparison) is visible without ad-hoc prints.
# ---------------------------------------------------------------------------


def _diagnose(sequence: str) -> list[tuple[str, bool]]:
    """Returns per-base (base, counted_as_gc) pairs for state inspection."""
    return [(base, base in ("G", "C")) for base in sequence]


def _assert_root_cause_is_case_sensitivity() -> None:
    sequence, observed = _reproduce_bug()
    expected = 1.0
    assert observed != expected, "expected reproduction to fail before the fix"

    diagnosis = _diagnose(sequence)
    lowercase_bases_missed = [base for base, counted in diagnosis if not counted]
    assert lowercase_bases_missed == ["g", "c"], (
        "root cause confirmed: lowercase g/c bases are not classified as GC"
    )


# ---------------------------------------------------------------------------
# STEP 5: Fix
#
# Corrected, production implementation: normalize case before comparison.
# This is the function the rest of the system should import and call.
# ---------------------------------------------------------------------------


def gc_content(sequence_id: str, sequence: str) -> GcContentResult:
    """Computes GC content for a nucleotide sequence, case-insensitively."""
    if not sequence:
        raise ValueError(f"sequence '{sequence_id}' is empty")

    normalized = sequence.upper()
    gc_count = sum(1 for base in normalized if base in ("G", "C"))

    return GcContentResult(
        sequence_id=sequence_id,
        gc_fraction=gc_count / len(normalized),
        length=len(normalized),
    )


# ---------------------------------------------------------------------------
# STEP 6: Verify
#
# Deterministic regression checks confirming the fix resolves the
# originally reported case and does not regress the already-working
# uppercase path.
# ---------------------------------------------------------------------------


def _verify_fix() -> None:
    mixed_case = gc_content("seq-mixed", "gcGC")
    assert mixed_case.gc_fraction == 1.0, "fix failed: mixed-case GC content still wrong"

    uppercase_only = gc_content("seq-upper", "ATGC")
    assert uppercase_only.gc_fraction == 0.5, "regression: uppercase path broken by fix"

    all_at = gc_content("seq-at", "atat")
    assert all_at.gc_fraction == 0.0, "regression: AT-only sequence miscounted"


if __name__ == "__main__":
    _assert_root_cause_is_case_sensitivity()
    _verify_fix()
    print("Debugging workflow verified: defect reproduced, diagnosed, fixed, and confirmed.")
