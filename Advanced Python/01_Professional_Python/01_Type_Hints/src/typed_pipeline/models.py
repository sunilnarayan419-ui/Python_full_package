"""Core domain models for a drug-discovery compound scoring pipeline.

Demonstrates production-grade static typing: Literal, Final, Annotated,
TypedDict, frozen dataclasses, and Self-returning builders.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Annotated, Final, Literal, Self, TypedDict

ExperimentStatus = Literal["pending", "running", "completed", "failed"]

MAX_POTENCY_NM: Final[float] = 1_000_000.0
MICROMOLAR_TO_NANOMOLAR: Final[int] = 1_000


class AssayMetadata(TypedDict, total=False):
    """Optional, loosely structured metadata attached to a raw assay read."""

    instrument_id: str
    plate_barcode: str
    operator: str
    replicate_count: int


PositiveFloat = Annotated[float, "value must be > 0"]


def _validate_positive(value: float, *, field_name: str) -> float:
    if value <= 0:
        raise ValueError(f"{field_name} must be strictly positive, got {value!r}")
    return value


@dataclass(frozen=True, slots=True)
class AssayResult:
    """An immutable single potency measurement for a compound against a target."""

    target_id: str
    ic50_nm: PositiveFloat
    metadata: AssayMetadata = field(default_factory=dict)

    def __post_init__(self) -> None:
        _validate_positive(self.ic50_nm, field_name="ic50_nm")
        if self.ic50_nm > MAX_POTENCY_NM:
            raise ValueError(
                f"ic50_nm {self.ic50_nm} exceeds physically plausible maximum"
            )

    @property
    def ic50_um(self) -> float:
        return self.ic50_nm / MICROMOLAR_TO_NANOMOLAR


@dataclass(frozen=True, slots=True)
class CompoundRecord:
    """A candidate compound tracked through the discovery pipeline."""

    compound_id: str
    smiles: str
    molecular_weight: PositiveFloat
    status: ExperimentStatus = "pending"
    assay_results: tuple[AssayResult, ...] = field(default_factory=tuple)

    def with_status(self, status: ExperimentStatus) -> Self:
        """Return a new record with an updated status (immutable update)."""
        return replace(self, status=status)

    def with_assay_result(self, result: AssayResult) -> Self:
        return replace(self, assay_results=(*self.assay_results, result))

    def best_potency(self) -> AssayResult | None:
        if not self.assay_results:
            return None
        return min(self.assay_results, key=lambda r: r.ic50_nm)
