"""Production-oriented logging for an experiment processing pipeline."""

from __future__ import annotations

import logging
from dataclasses import dataclass

# Module-level logger: reusable library code never calls basicConfig()
# itself, so it can be embedded in any application's logging setup
# without clobbering that application's configuration.
logger = logging.getLogger(__name__)


class SampleValidationError(ValueError):
    """Raised when a sample fails validation prior to analysis."""


@dataclass(frozen=True, slots=True)
class Sample:
    sample_id: str
    concentration_ng_ul: float


class ExperimentPipeline:
    """Processes samples through validation and analysis, emitting
    structured diagnostic events at each stage.
    """

    MIN_CONCENTRATION = 0.5

    def start_experiment(self, experiment_id: str, sample_count: int) -> None:
        logger.info(
            "Experiment started: id=%s sample_count=%d", experiment_id, sample_count
        )

    def process_sample(self, sample: Sample) -> float:
        logger.debug(
            "Processing sample %s (concentration=%.3f ng/uL)",
            sample.sample_id,
            sample.concentration_ng_ul,
        )

        try:
            self._validate(sample)
        except SampleValidationError:
            logger.warning(
                "Validation failed for sample %s: concentration=%.3f below minimum %.3f",
                sample.sample_id,
                sample.concentration_ng_ul,
                self.MIN_CONCENTRATION,
            )
            raise

        result = sample.concentration_ng_ul * 2.0
        logger.info("Sample processed: id=%s result=%.3f", sample.sample_id, result)
        return result

    def _validate(self, sample: Sample) -> None:
        if sample.concentration_ng_ul < self.MIN_CONCENTRATION:
            raise SampleValidationError(
                f"concentration below minimum for sample {sample.sample_id}"
            )

    def finish_experiment(self, experiment_id: str, processed_count: int) -> None:
        logger.info(
            "Analysis completed: id=%s processed_count=%d",
            experiment_id,
            processed_count,
        )

    def handle_unexpected_failure(self, sample: Sample, exc: Exception) -> None:
        # logger.exception() automatically attaches the current traceback;
        # only call it from within an active except block.
        logger.exception(
            "Unexpected processing failure for sample %s", sample.sample_id
        )


def _configure_standalone_logging() -> None:
    """Isolated demo configuration -- never called by library code itself."""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
    )


if __name__ == "__main__":
    _configure_standalone_logging()

    pipeline = ExperimentPipeline()
    samples = [
        Sample(sample_id="S-100", concentration_ng_ul=12.5),
        Sample(sample_id="S-101", concentration_ng_ul=0.1),  # will fail validation
    ]

    pipeline.start_experiment("EXP-2026-01", sample_count=len(samples))

    processed = 0
    for sample in samples:
        try:
            pipeline.process_sample(sample)
            processed += 1
        except SampleValidationError:
            # Expected domain failure: already logged as a warning inside
            # process_sample; the pipeline continues with remaining samples.
            continue
        except Exception as exc:  # noqa: BLE001 -- top-level safety net only
            pipeline.handle_unexpected_failure(sample, exc)

    pipeline.finish_experiment("EXP-2026-01", processed_count=processed)
