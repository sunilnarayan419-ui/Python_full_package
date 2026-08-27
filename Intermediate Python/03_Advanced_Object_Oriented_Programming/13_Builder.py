from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto


# ============================================================
# UNIVERSITY LEVEL
# ============================================================
# Goal: understand step-by-step construction of a simple configuration.


@dataclass
class UniExperimentConfig:
    title: str
    sample_count: int


class UniExperimentConfigBuilder:
    def __init__(self) -> None:
        self._title = "untitled"
        self._sample_count = 1

    def with_title(self, title: str) -> UniExperimentConfigBuilder:
        self._title = title
        return self

    def with_sample_count(self, count: int) -> UniExperimentConfigBuilder:
        self._sample_count = count
        return self

    def build(self) -> UniExperimentConfig:
        return UniExperimentConfig(self._title, self._sample_count)


class UniversityBuilder:
    @staticmethod
    def run() -> None:
        config = (
            UniExperimentConfigBuilder()
            .with_title("Seed Germination Trial")
            .with_sample_count(20)
            .build()
        )
        print(config)


# ============================================================
# INTERVIEW LEVEL
# ============================================================
# Goal: construct objects with optional components and sensible defaults.


class IvReplicateMode(Enum):
    NONE = auto()
    TRIPLICATE = auto()


@dataclass(frozen=True, slots=True)
class IvAssayConfig:
    title: str
    temperature_c: float
    replicate_mode: IvReplicateMode
    notes: str | None


class IvAssayConfigBuilder:
    """Optional components (temperature, replicate mode, notes) all have
    defaults; only `title` is mandatory, demonstrating how Builder
    handles a mix of required and optional fields cleanly."""

    def __init__(self, title: str) -> None:
        self._title = title
        self._temperature_c = 25.0
        self._replicate_mode = IvReplicateMode.NONE
        self._notes: str | None = None

    def with_temperature(self, temperature_c: float) -> IvAssayConfigBuilder:
        self._temperature_c = temperature_c
        return self

    def with_replicates(self, mode: IvReplicateMode) -> IvAssayConfigBuilder:
        self._replicate_mode = mode
        return self

    def with_notes(self, notes: str) -> IvAssayConfigBuilder:
        self._notes = notes
        return self

    def build(self) -> IvAssayConfig:
        return IvAssayConfig(
            self._title, self._temperature_c, self._replicate_mode, self._notes
        )


class InterviewBuilder:
    @staticmethod
    def run() -> None:
        minimal = IvAssayConfigBuilder("Basic PCR Run").build()
        print(minimal)

        full = (
            IvAssayConfigBuilder("Protein Stability Assay")
            .with_temperature(37.0)
            .with_replicates(IvReplicateMode.TRIPLICATE)
            .with_notes("Run in dark to avoid photobleaching")
            .build()
        )
        print(full)


# ============================================================
# INDUSTRY LEVEL
# ============================================================
# Goal: a complex analysis pipeline configuration with required fields,
# optional configuration, validation, sensible defaults, and a final
# build step that produces an immutable product.


class PipelineConfigError(ValueError):
    """Raised when a pipeline configuration is invalid or incomplete."""


class NormalizationMethod(Enum):
    NONE = auto()
    MEAN = auto()
    Z_SCORE = auto()


@dataclass(frozen=True, slots=True)
class QualityThresholds:
    min_concentration_ng_ul: float
    max_concentration_ng_ul: float


@dataclass(frozen=True, slots=True)
class AnalysisPipelineConfig:
    """Immutable final product -- once built, cannot be silently mutated
    by code elsewhere in the pipeline (the reason this is worth building
    rather than trivially constructing: many optional fields, validation
    across fields, and a need for a guaranteed-consistent final object).
    """

    pipeline_name: str
    dataset_id: str
    normalization: NormalizationMethod
    quality_thresholds: QualityThresholds
    max_parallel_workers: int
    tags: tuple[str, ...]


class AnalysisPipelineConfigBuilder:
    """Required fields (pipeline_name, dataset_id) must be supplied
    explicitly; everything else has a sensible default. `build()`
    performs cross-field validation and produces an immutable,
    final AnalysisPipelineConfig -- callers cannot receive a partially
    configured or inconsistent object.
    """

    def __init__(self, pipeline_name: str, dataset_id: str) -> None:
        if not pipeline_name:
            raise PipelineConfigError("pipeline_name is required")
        if not dataset_id:
            raise PipelineConfigError("dataset_id is required")
        self._pipeline_name = pipeline_name
        self._dataset_id = dataset_id
        self._normalization = NormalizationMethod.NONE
        self._min_concentration = 0.0
        self._max_concentration = 1000.0
        self._max_parallel_workers = 1
        self._tags: list[str] = []

    def with_normalization(
        self, method: NormalizationMethod
    ) -> AnalysisPipelineConfigBuilder:
        self._normalization = method
        return self

    def with_quality_thresholds(
        self, minimum: float, maximum: float
    ) -> AnalysisPipelineConfigBuilder:
        self._min_concentration = minimum
        self._max_concentration = maximum
        return self

    def with_parallel_workers(self, count: int) -> AnalysisPipelineConfigBuilder:
        self._max_parallel_workers = count
        return self

    def with_tag(self, tag: str) -> AnalysisPipelineConfigBuilder:
        self._tags.append(tag)
        return self

    def build(self) -> AnalysisPipelineConfig:
        if self._min_concentration >= self._max_concentration:
            raise PipelineConfigError(
                "min_concentration must be less than max_concentration"
            )
        if self._max_parallel_workers <= 0:
            raise PipelineConfigError("max_parallel_workers must be positive")

        return AnalysisPipelineConfig(
            pipeline_name=self._pipeline_name,
            dataset_id=self._dataset_id,
            normalization=self._normalization,
            quality_thresholds=QualityThresholds(
                self._min_concentration, self._max_concentration
            ),
            max_parallel_workers=self._max_parallel_workers,
            tags=tuple(self._tags),
        )


class IndustryBuilder:
    @staticmethod
    def run() -> None:
        config = (
            AnalysisPipelineConfigBuilder("RNA-Seq Normalization", "DS-2026-08")
            .with_normalization(NormalizationMethod.Z_SCORE)
            .with_quality_thresholds(minimum=5.0, maximum=800.0)
            .with_parallel_workers(4)
            .with_tag("rna-seq")
            .with_tag("greenhouse-batch")
            .build()
        )
        print(config)

        try:
            (
                AnalysisPipelineConfigBuilder("Bad Config", "DS-BAD")
                .with_quality_thresholds(minimum=500.0, maximum=10.0)
                .build()
            )
        except PipelineConfigError as exc:
            print("Rejected:", exc)

        try:
            AnalysisPipelineConfigBuilder("", "DS-EMPTY")
        except PipelineConfigError as exc:
            print("Rejected:", exc)


if __name__ == "__main__":
    UniversityBuilder.run()
    InterviewBuilder.run()
    IndustryBuilder.run()
