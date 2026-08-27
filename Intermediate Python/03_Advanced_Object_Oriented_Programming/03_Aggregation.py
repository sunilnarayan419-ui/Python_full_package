from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


# ============================================================
# UNIVERSITY LEVEL
# ============================================================
# Goal: understand weak ownership -- the part can outlive the whole.


@dataclass
class UniResearcher:
    """Exists independently of any project."""

    name: str
    institution: str


class UniResearchProject:
    """Aggregation: a ResearchProject holds REFERENCES to Researchers.

    Researchers are created elsewhere and simply attached here; removing
    the project does not destroy the researchers.
    """

    def __init__(self, title: str) -> None:
        self.title = title
        self.researchers: list[UniResearcher] = []

    def add_researcher(self, researcher: UniResearcher) -> None:
        self.researchers.append(researcher)


class UniversityAggregation:
    @staticmethod
    def run() -> None:
        dr_rao = UniResearcher("Dr. Rao", "IISc")
        dr_lin = UniResearcher("Dr. Lin", "NUS")

        project = UniResearchProject("Drought-Resistant Rice")
        project.add_researcher(dr_rao)
        project.add_researcher(dr_lin)

        print(f"{project.title} has {len(project.researchers)} researchers")
        del project  # researchers still exist and are usable
        print("Researcher still valid after project deleted:", dr_rao.name)


# ============================================================
# INTERVIEW LEVEL
# ============================================================
# Goal: demonstrate that researchers persist and can join multiple
# projects concurrently -- the key aggregation trade-off vs composition.


class IvResearcher:
    def __init__(self, researcher_id: str, name: str) -> None:
        self.researcher_id = researcher_id
        self.name = name


class IvResearchProject:
    """Holds shared references; does not manage researcher lifecycle.

    Unlike composition, removing a researcher from this project (or
    discarding the project entirely) must never delete the researcher --
    the same person may be attached to several concurrent projects.
    """

    def __init__(self, title: str) -> None:
        self.title = title
        self._researchers: dict[str, IvResearcher] = {}

    def attach(self, researcher: IvResearcher) -> None:
        self._researchers[researcher.researcher_id] = researcher

    def detach(self, researcher_id: str) -> None:
        self._researchers.pop(researcher_id, None)

    def researcher_ids(self) -> list[str]:
        return list(self._researchers.keys())


class InterviewAggregation:
    @staticmethod
    def run() -> None:
        rao = IvResearcher("R-01", "Dr. Rao")

        project_a = IvResearchProject("Drought-Resistant Rice")
        project_b = IvResearchProject("Soil Microbiome Mapping")

        project_a.attach(rao)
        project_b.attach(rao)  # same researcher, two independent projects

        print("Project A researchers:", project_a.researcher_ids())
        print("Project B researchers:", project_b.researcher_ids())

        project_a.detach("R-01")
        print("After detach, Project A:", project_a.researcher_ids())
        print("Project B unaffected:", project_b.researcher_ids())


# ============================================================
# INDUSTRY LEVEL
# ============================================================
# Goal: a realistic model where lab equipment and researchers are shared
# resources across multiple workflows, with clear aggregation semantics
# distinct from ownership/composition.


class ResourceUnavailableError(RuntimeError):
    """Raised when a shared resource cannot be allocated."""


@dataclass(frozen=True, slots=True)
class Researcher:
    researcher_id: str
    name: str


@dataclass(frozen=True, slots=True)
class LabInstrument:
    instrument_id: str
    model: str


class ResourceRegistry(Protocol):
    """Central source of truth for shared, independently-lived resources.

    Workflows aggregate references obtained here; they never own or
    construct Researcher/LabInstrument instances themselves.
    """

    def get_researcher(self, researcher_id: str) -> Researcher: ...

    def get_instrument(self, instrument_id: str) -> LabInstrument: ...


class InMemoryResourceRegistry:
    def __init__(self) -> None:
        self._researchers: dict[str, Researcher] = {}
        self._instruments: dict[str, LabInstrument] = {}

    def register_researcher(self, researcher: Researcher) -> None:
        self._researchers[researcher.researcher_id] = researcher

    def register_instrument(self, instrument: LabInstrument) -> None:
        self._instruments[instrument.instrument_id] = instrument

    def get_researcher(self, researcher_id: str) -> Researcher:
        try:
            return self._researchers[researcher_id]
        except KeyError as exc:
            raise ResourceUnavailableError(f"Unknown researcher {researcher_id}") from exc

    def get_instrument(self, instrument_id: str) -> LabInstrument:
        try:
            return self._instruments[instrument_id]
        except KeyError as exc:
            raise ResourceUnavailableError(f"Unknown instrument {instrument_id}") from exc


@dataclass
class ScientificWorkflow:
    """Aggregates shared resources by reference.

    A workflow's lifecycle (creation/deletion) never affects the shared
    Researcher or LabInstrument objects it references -- those live in the
    ResourceRegistry and may simultaneously belong to other workflows.
    This is the defining trait that distinguishes aggregation from the
    strong-ownership composition shown in 02_Composition.py.
    """

    name: str
    registry: ResourceRegistry
    researcher_ids: list[str] = field(default_factory=list)
    instrument_ids: list[str] = field(default_factory=list)

    def assign_researcher(self, researcher_id: str) -> None:
        self.registry.get_researcher(researcher_id)  # validates existence
        self.researcher_ids.append(researcher_id)

    def assign_instrument(self, instrument_id: str) -> None:
        self.registry.get_instrument(instrument_id)
        self.instrument_ids.append(instrument_id)

    def describe(self) -> str:
        researchers = [self.registry.get_researcher(r).name for r in self.researcher_ids]
        instruments = [self.registry.get_instrument(i).model for i in self.instrument_ids]
        return f"{self.name}: researchers={researchers}, instruments={instruments}"


class IndustryAggregation:
    @staticmethod
    def run() -> None:
        registry = InMemoryResourceRegistry()
        registry.register_researcher(Researcher("R-01", "Dr. Rao"))
        registry.register_instrument(LabInstrument("INS-01", "PCR Cycler X200"))

        workflow_a = ScientificWorkflow("Genotyping Batch A", registry)
        workflow_b = ScientificWorkflow("Genotyping Batch B", registry)

        workflow_a.assign_researcher("R-01")
        workflow_a.assign_instrument("INS-01")
        workflow_b.assign_researcher("R-01")  # shared across workflows
        workflow_b.assign_instrument("INS-01")

        print(workflow_a.describe())
        print(workflow_b.describe())

        del workflow_a  # shared resources remain valid in the registry
        print("Instrument still registered:", registry.get_instrument("INS-01").model)


if __name__ == "__main__":
    UniversityAggregation.run()
    InterviewAggregation.run()
    IndustryAggregation.run()
