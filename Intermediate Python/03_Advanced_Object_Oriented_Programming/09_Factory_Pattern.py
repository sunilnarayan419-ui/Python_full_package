from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Callable


# ============================================================
# UNIVERSITY LEVEL
# ============================================================
# Goal: understand a simple factory function that hides object creation.


class UniSample(ABC):
    @abstractmethod
    def describe(self) -> str: ...


class UniPlantSample(UniSample):
    def describe(self) -> str:
        return "Plant sample"


class UniBloodSample(UniSample):
    def describe(self) -> str:
        return "Blood sample"


def create_sample(kind: str) -> UniSample:
    """Client calls this instead of choosing a concrete class itself."""
    if kind == "plant":
        return UniPlantSample()
    if kind == "blood":
        return UniBloodSample()
    raise ValueError(f"Unknown sample kind: {kind}")


class UniversityFactoryPattern:
    @staticmethod
    def run() -> None:
        sample = create_sample("plant")
        print(sample.describe())


# ============================================================
# INTERVIEW LEVEL
# ============================================================
# Goal: a factory that selects a processor based on configuration,
# decoupling the caller from concrete processor classes.


class IvProcessor(ABC):
    @abstractmethod
    def process(self, raw_value: float) -> float: ...


class IvPCRProcessor(IvProcessor):
    def process(self, raw_value: float) -> float:
        return raw_value * 1.5


class IvSequencingProcessor(IvProcessor):
    def process(self, raw_value: float) -> float:
        return raw_value * 0.75


class IvProcessingKind(Enum):
    PCR = auto()
    SEQUENCING = auto()


class IvProcessorFactory:
    """Client asks for a processor by enum value and never sees the
    concrete IvPCRProcessor / IvSequencingProcessor classes."""

    _builders: dict[IvProcessingKind, Callable[[], IvProcessor]] = {
        IvProcessingKind.PCR: IvPCRProcessor,
        IvProcessingKind.SEQUENCING: IvSequencingProcessor,
    }

    @classmethod
    def create(cls, kind: IvProcessingKind) -> IvProcessor:
        builder = cls._builders.get(kind)
        if builder is None:
            raise ValueError(f"Unsupported processing kind: {kind}")
        return builder()


class InterviewFactoryPattern:
    @staticmethod
    def run() -> None:
        processor = IvProcessorFactory.create(IvProcessingKind.PCR)
        print("PCR result:", processor.process(40.0))

        processor = IvProcessorFactory.create(IvProcessingKind.SEQUENCING)
        print("Sequencing result:", processor.process(40.0))


# ============================================================
# INDUSTRY LEVEL
# ============================================================
# Goal: a scalable factory where new processor types register themselves
# without modifying the factory class (Open/Closed), configuration is
# typed, and unknown/misconfigured requests raise meaningful exceptions.


class UnsupportedAssayError(ValueError):
    """Raised when no processor is registered for a requested assay kind."""


class AssayKind(Enum):
    PCR = auto()
    SEQUENCING = auto()
    PROTEIN = auto()


class AssayProcessor(ABC):
    """Every registered product must satisfy this contract."""

    @abstractmethod
    def process(self, raw_value: float) -> float: ...

    @abstractmethod
    def assay_kind(self) -> AssayKind: ...


class PCRProcessor(AssayProcessor):
    def process(self, raw_value: float) -> float:
        return round(raw_value * 1.5, 3)

    def assay_kind(self) -> AssayKind:
        return AssayKind.PCR


class SequencingProcessor(AssayProcessor):
    def process(self, raw_value: float) -> float:
        return round(raw_value * 0.75, 3)

    def assay_kind(self) -> AssayKind:
        return AssayKind.SEQUENCING


class ProteinAssayProcessor(AssayProcessor):
    def process(self, raw_value: float) -> float:
        return round(raw_value**0.5, 3)

    def assay_kind(self) -> AssayKind:
        return AssayKind.PROTEIN


class AssayProcessorFactory:
    """Registry-based factory: adding a new AssayKind means registering a
    new processor class, not editing this factory's logic (Open/Closed).
    The client depends only on `create()` and the AssayProcessor contract.
    """

    def __init__(self) -> None:
        self._registry: dict[AssayKind, Callable[[], AssayProcessor]] = {}

    def register(self, kind: AssayKind, builder: Callable[[], AssayProcessor]) -> None:
        self._registry[kind] = builder

    def create(self, kind: AssayKind) -> AssayProcessor:
        builder = self._registry.get(kind)
        if builder is None:
            raise UnsupportedAssayError(f"No processor registered for {kind}")
        return builder()

    def supported_kinds(self) -> list[AssayKind]:
        return list(self._registry.keys())


def build_default_factory() -> AssayProcessorFactory:
    """Composition root: wires concrete processors into the factory once,
    keeping registration logic out of the factory class itself."""
    factory = AssayProcessorFactory()
    factory.register(AssayKind.PCR, PCRProcessor)
    factory.register(AssayKind.SEQUENCING, SequencingProcessor)
    factory.register(AssayKind.PROTEIN, ProteinAssayProcessor)
    return factory


class IndustryFactoryPattern:
    @staticmethod
    def run() -> None:
        factory = build_default_factory()
        print("Supported kinds:", [k.name for k in factory.supported_kinds()])

        for kind, raw_value in (
            (AssayKind.PCR, 40.0),
            (AssayKind.SEQUENCING, 40.0),
            (AssayKind.PROTEIN, 81.0),
        ):
            processor = factory.create(kind)
            print(f"{processor.assay_kind().name}: {processor.process(raw_value)}")

        try:
            factory.create(AssayKind.PROTEIN)  # still supported, sanity check
            factory.register(AssayKind.PROTEIN, ProteinAssayProcessor)  # idempotent
            factory.create(AssayKind.PCR)
            del factory._registry[AssayKind.PCR]  # simulate a missing registration
            factory.create(AssayKind.PCR)
        except UnsupportedAssayError as exc:
            print("Rejected:", exc)


if __name__ == "__main__":
    UniversityFactoryPattern.run()
    InterviewFactoryPattern.run()
    IndustryFactoryPattern.run()
