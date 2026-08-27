from __future__ import annotations

from typing import Any


class UniversityMetaclasses:
    """Demonstrates that a metaclass is simply the type that creates a
    class, by defining a minimal metaclass that logs class creation."""

    class LoggingMeta(type):
        def __new__(mcs, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> type:
            print(f"creating class: {name}")
            return super().__new__(mcs, name, bases, namespace)

    class Experiment(metaclass=LoggingMeta):
        def __init__(self, title: str) -> None:
            self.title = title

    @staticmethod
    def run() -> None:
        experiment = UniversityMetaclasses.Experiment("seed-germination")
        print(experiment.title)


class InterviewMetaclasses:
    """Demonstrates a realistic metaclass use case: enforcing that
    subclasses implement required interface methods at class-creation
    time, catching mistakes earlier than duck-typing would."""

    class EnforceInterfaceMeta(type):
        required_methods = ("analyze",)

        def __new__(mcs, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> type:
            cls = super().__new__(mcs, name, bases, namespace)
            if bases:  # skip check for the base class itself
                missing = [m for m in mcs.required_methods if not callable(namespace.get(m))]
                if missing:
                    raise TypeError(f"{name} is missing required methods: {missing}")
            return cls

    class DataAnalyzer(metaclass=EnforceInterfaceMeta):
        def analyze(self, values: list[float]) -> float:
            raise NotImplementedError

    class MeanAnalyzer(DataAnalyzer):
        def analyze(self, values: list[float]) -> float:
            return sum(values) / len(values) if values else 0.0

    @staticmethod
    def run() -> None:
        analyzer = InterviewMetaclasses.MeanAnalyzer()
        print(analyzer.analyze([1.0, 2.0, 3.0, 4.0]))

        try:
            class BrokenAnalyzer(InterviewMetaclasses.DataAnalyzer):
                pass

        except TypeError as exc:
            print(f"caught expected error: {exc}")


class IndustryMetaclasses:
    """Demonstrates a metaclass-based plugin/schema registry, a realistic
    industry use case where every subclass of a base processor is
    automatically discoverable by name without manual registration."""

    class ProcessorRegistryMeta(type):
        _registry: dict[str, type] = {}

        def __new__(mcs, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> type:
            cls = super().__new__(mcs, name, bases, namespace)
            if bases:  # register only concrete subclasses, not the base
                key = namespace.get("processor_key", name)
                if key in mcs._registry:
                    raise ValueError(f"duplicate processor_key registered: {key}")
                mcs._registry[key] = cls
            return cls

        @classmethod
        def get(mcs, key: str) -> type:
            if key not in mcs._registry:
                raise KeyError(f"no processor registered under key: {key}")
            return mcs._registry[key]

        @classmethod
        def available(mcs) -> list[str]:
            return sorted(mcs._registry.keys())

    class SampleProcessor(metaclass=ProcessorRegistryMeta):
        processor_key = ""

        def process(self, raw_value: float) -> float:
            raise NotImplementedError

    class RnaSeqProcessor(SampleProcessor):
        processor_key = "rna_seq"

        def process(self, raw_value: float) -> float:
            return round(raw_value * 1e6, 2)  # transcripts per million scaling

    class ProteomicsProcessor(SampleProcessor):
        processor_key = "proteomics"

        def process(self, raw_value: float) -> float:
            return round(raw_value / 1000, 4)  # normalize to micrograms

    @staticmethod
    def run() -> None:
        registry = IndustryMetaclasses.ProcessorRegistryMeta
        print(f"available processors: {registry.available()}")

        processor_cls = registry.get("rna_seq")
        processor = processor_cls()
        print(f"processed value: {processor.process(0.0042)}")

        try:
            registry.get("mass_spec")
        except KeyError as exc:
            print(f"caught expected error: {exc}")


if __name__ == "__main__":
    UniversityMetaclasses.run()
    InterviewMetaclasses.run()
    IndustryMetaclasses.run()
