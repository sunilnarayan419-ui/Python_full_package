from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Protocol


# ============================================================
# UNIVERSITY LEVEL
# ============================================================
# Goal: understand association -- two objects collaborate without either
# owning or aggregating the other.


@dataclass
class UniScientist:
    name: str


@dataclass
class UniInstrument:
    model: str

    def operated_by(self, scientist: UniScientist) -> str:
        """Neither object holds a permanent reference to the other; the
        relationship exists only for the duration of this call."""
        return f"{scientist.name} operates {self.model}"


class UniversityAssociation:
    @staticmethod
    def run() -> None:
        scientist = UniScientist("Dr. Menon")
        instrument = UniInstrument("Spectrophotometer S-9")
        print(instrument.operated_by(scientist))


# ============================================================
# INTERVIEW LEVEL
# ============================================================
# Goal: demonstrate interaction without ownership, including a
# many-to-many association tracked externally so neither side is coupled
# to the other's collection.


class IvScientist:
    def __init__(self, name: str) -> None:
        self.name = name


class IvExperiment:
    def __init__(self, title: str) -> None:
        self.title = title


class IvAssignmentRegistry:
    """Tracks many-to-many Scientist<->Experiment associations externally.

    Neither IvScientist nor IvExperiment needs to know about the other's
    class, keeping both independently reusable and testable.
    """

    def __init__(self) -> None:
        self._links: list[tuple[str, str]] = []

    def associate(self, scientist: IvScientist, experiment: IvExperiment) -> None:
        self._links.append((scientist.name, experiment.title))

    def experiments_for(self, scientist: IvScientist) -> list[str]:
        return [exp for sci, exp in self._links if sci == scientist.name]

    def scientists_for(self, experiment: IvExperiment) -> list[str]:
        return [sci for sci, exp in self._links if exp == experiment.title]


class InterviewAssociation:
    @staticmethod
    def run() -> None:
        rao = IvScientist("Dr. Rao")
        lin = IvScientist("Dr. Lin")
        exp_a = IvExperiment("Photosynthesis Rate Study")
        exp_b = IvExperiment("Root Growth Under Stress")

        registry = IvAssignmentRegistry()
        registry.associate(rao, exp_a)
        registry.associate(rao, exp_b)
        registry.associate(lin, exp_a)

        print("Rao's experiments:", registry.experiments_for(rao))
        print("Experiment A scientists:", registry.scientists_for(exp_a))


# ============================================================
# INDUSTRY LEVEL
# ============================================================
# Goal: model realistic many-to-many associations (Compound<->Target,
# Scientist<->Instrument) via a clean, interface-driven association
# service, avoiding tight coupling between unrelated domain objects.


class AssociationError(ValueError):
    """Raised when an association cannot be formed or is not found."""


class BindingAffinity(Enum):
    STRONG = auto()
    MODERATE = auto()
    WEAK = auto()


@dataclass(frozen=True, slots=True)
class Compound:
    compound_id: str
    name: str


@dataclass(frozen=True, slots=True)
class MolecularTarget:
    target_id: str
    protein_name: str


@dataclass(frozen=True, slots=True)
class Binding:
    compound_id: str
    target_id: str
    affinity: BindingAffinity


class AssociationRepository(Protocol):
    """Abstraction the service depends on -- storage details are irrelevant
    to the association logic itself (dependency inversion)."""

    def add(self, binding: Binding) -> None: ...

    def bindings_for_compound(self, compound_id: str) -> list[Binding]: ...

    def bindings_for_target(self, target_id: str) -> list[Binding]: ...


class InMemoryAssociationRepository:
    def __init__(self) -> None:
        self._bindings: list[Binding] = []

    def add(self, binding: Binding) -> None:
        self._bindings.append(binding)

    def bindings_for_compound(self, compound_id: str) -> list[Binding]:
        return [b for b in self._bindings if b.compound_id == compound_id]

    def bindings_for_target(self, target_id: str) -> list[Binding]:
        return [b for b in self._bindings if b.target_id == target_id]


@dataclass
class CompoundTargetAssociationService:
    """Coordinates Compound<->MolecularTarget associations.

    Compound and MolecularTarget remain simple, independent domain
    objects with no knowledge of each other or of persistence; this
    service is the sole place their relationship is expressed, keeping
    the association loosely coupled and easy to evolve (e.g. adding
    assay-derived confidence scores later) without touching either
    domain object.
    """

    repository: AssociationRepository
    known_compounds: dict[str, Compound] = field(default_factory=dict)
    known_targets: dict[str, MolecularTarget] = field(default_factory=dict)

    def register_compound(self, compound: Compound) -> None:
        self.known_compounds[compound.compound_id] = compound

    def register_target(self, target: MolecularTarget) -> None:
        self.known_targets[target.target_id] = target

    def associate(
        self, compound_id: str, target_id: str, affinity: BindingAffinity
    ) -> None:
        if compound_id not in self.known_compounds:
            raise AssociationError(f"Unknown compound {compound_id}")
        if target_id not in self.known_targets:
            raise AssociationError(f"Unknown target {target_id}")
        self.repository.add(Binding(compound_id, target_id, affinity))

    def targets_for_compound(self, compound_id: str) -> list[str]:
        return [
            self.known_targets[b.target_id].protein_name
            for b in self.repository.bindings_for_compound(compound_id)
        ]

    def compounds_for_target(self, target_id: str) -> list[str]:
        return [
            self.known_compounds[b.compound_id].name
            for b in self.repository.bindings_for_target(target_id)
        ]


class IndustryAssociation:
    @staticmethod
    def run() -> None:
        service = CompoundTargetAssociationService(InMemoryAssociationRepository())

        compound = Compound("CMP-001", "Rifavizin")
        target_a = MolecularTarget("TGT-01", "DNA Gyrase")
        target_b = MolecularTarget("TGT-02", "RNA Polymerase")

        service.register_compound(compound)
        service.register_target(target_a)
        service.register_target(target_b)

        service.associate("CMP-001", "TGT-01", BindingAffinity.STRONG)
        service.associate("CMP-001", "TGT-02", BindingAffinity.WEAK)

        print("Targets for compound:", service.targets_for_compound("CMP-001"))
        print("Compounds for target A:", service.compounds_for_target("TGT-01"))

        try:
            service.associate("CMP-999", "TGT-01", BindingAffinity.MODERATE)
        except AssociationError as exc:
            print("Rejected:", exc)


if __name__ == "__main__":
    UniversityAssociation.run()
    InterviewAssociation.run()
    IndustryAssociation.run()
