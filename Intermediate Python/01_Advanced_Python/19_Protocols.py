from __future__ import annotations

from typing import Protocol, runtime_checkable


class UniversityProtocols:
    """Demonstrates a basic structural type using typing.Protocol: any
    class with a matching method satisfies the protocol, no inheritance
    required."""

    class HasHeight(Protocol):
        height_cm: float

    class SeedlingSample:
        def __init__(self, height_cm: float) -> None:
            self.height_cm = height_cm

    @staticmethod
    def print_height(item: "UniversityProtocols.HasHeight") -> None:
        print(f"height: {item.height_cm} cm")

    @staticmethod
    def run() -> None:
        seedling = UniversityProtocols.SeedlingSample(height_cm=6.3)
        UniversityProtocols.print_height(seedling)


class InterviewProtocols:
    """Demonstrates a runtime-checkable Protocol used to validate that
    unrelated classes implement a shared processing interface, showing
    structural typing's advantage over requiring a common base class."""

    @runtime_checkable
    class DataProcessor(Protocol):
        def process(self, value: float) -> float:
            ...

    class NormalizingProcessor:
        def __init__(self, baseline: float) -> None:
            self.baseline = baseline

        def process(self, value: float) -> float:
            return value / self.baseline if self.baseline else 0.0

    class RoundingProcessor:
        def process(self, value: float) -> float:
            return round(value)

    @staticmethod
    def run_pipeline(value: float, processors: list["InterviewProtocols.DataProcessor"]) -> float:
        for processor in processors:
            value = processor.process(value)
        return value

    @staticmethod
    def run() -> None:
        normalizer = InterviewProtocols.NormalizingProcessor(baseline=10.0)
        rounder = InterviewProtocols.RoundingProcessor()

        print(isinstance(normalizer, InterviewProtocols.DataProcessor))
        result = InterviewProtocols.run_pipeline(47.0, [normalizer, rounder])
        print(f"pipeline result: {result}")


class IndustryProtocols:
    """Demonstrates Protocols enabling dependency inversion in a
    production-style ingestion service: the service depends only on a
    narrow structural interface, allowing interchangeable data providers
    (file-based, in-memory, remote) without shared inheritance."""

    class SampleDataProvider(Protocol):
        def fetch_samples(self) -> list[dict[str, float]]:
            ...

        def source_name(self) -> str:
            ...

    class InMemorySampleProvider:
        def __init__(self, samples: list[dict[str, float]]) -> None:
            self._samples = samples

        def fetch_samples(self) -> list[dict[str, float]]:
            return list(self._samples)

        def source_name(self) -> str:
            return "in-memory"

    class SyntheticSampleProvider:
        """Generates deterministic synthetic samples, useful for testing
        the ingestion service without touching real lab systems."""

        def __init__(self, count: int, base_value: float) -> None:
            self._count = count
            self._base_value = base_value

        def fetch_samples(self) -> list[dict[str, float]]:
            return [{"sample_id": i, "value": self._base_value + i * 0.1} for i in range(self._count)]

        def source_name(self) -> str:
            return "synthetic"

    class IngestionService:
        """Depends only on the SampleDataProvider protocol, not on any
        concrete provider implementation."""

        def __init__(self, provider: "IndustryProtocols.SampleDataProvider") -> None:
            self._provider = provider

        def ingest(self) -> dict[str, float | int | str]:
            samples = self._provider.fetch_samples()
            values = [s["value"] for s in samples]
            return {
                "source": self._provider.source_name(),
                "count": len(samples),
                "average": round(sum(values) / len(values), 4) if values else 0.0,
            }

    @staticmethod
    def run() -> None:
        in_memory_provider = IndustryProtocols.InMemorySampleProvider(
            [{"sample_id": 1, "value": 4.2}, {"sample_id": 2, "value": 5.1}]
        )
        synthetic_provider = IndustryProtocols.SyntheticSampleProvider(count=5, base_value=2.0)

        for provider in (in_memory_provider, synthetic_provider):
            service = IndustryProtocols.IngestionService(provider)
            print(service.ingest())


if __name__ == "__main__":
    UniversityProtocols.run()
    InterviewProtocols.run()
    IndustryProtocols.run()
