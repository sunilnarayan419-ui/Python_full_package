"""Production-quality pytest suite for a laboratory sample validation service.

Run with: pytest 02_pytest.py
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pytest


class InvalidSampleError(ValueError):
    """Raised when a laboratory sample fails domain validation."""


@dataclass(frozen=True, slots=True)
class Sample:
    sample_id: str
    concentration_ng_ul: float
    volume_ul: float


class SampleValidator:
    """Validates genomics samples prior to sequencing library preparation."""

    MIN_CONCENTRATION = 0.5  # ng/uL
    MIN_VOLUME = 5.0  # uL

    def validate(self, sample: Sample) -> None:
        if not sample.sample_id.strip():
            raise InvalidSampleError("sample_id must not be blank")
        if sample.concentration_ng_ul < self.MIN_CONCENTRATION:
            raise InvalidSampleError(
                f"concentration {sample.concentration_ng_ul} ng/uL below minimum "
                f"{self.MIN_CONCENTRATION} ng/uL for sample {sample.sample_id}"
            )
        if sample.volume_ul < self.MIN_VOLUME:
            raise InvalidSampleError(
                f"volume {sample.volume_ul} uL below minimum {self.MIN_VOLUME} uL "
                f"for sample {sample.sample_id}"
            )

    def total_yield_ng(self, sample: Sample) -> float:
        self.validate(sample)
        return sample.concentration_ng_ul * sample.volume_ul

    def write_manifest(self, samples: list[Sample], destination: Path) -> Path:
        """Writes a simple manifest file; exercises real filesystem behavior."""
        lines = [f"{s.sample_id},{s.concentration_ng_ul},{s.volume_ul}" for s in samples]
        destination.write_text("\n".join(lines), encoding="utf-8")
        return destination


@pytest.fixture
def validator() -> SampleValidator:
    """A fresh validator instance per test."""
    return SampleValidator()


@pytest.fixture
def valid_sample() -> Sample:
    return Sample(sample_id="GEN-1001", concentration_ng_ul=25.0, volume_ul=20.0)


class TestSampleValidatorBasics:
    def test_validate_accepts_valid_sample(
        self, validator: SampleValidator, valid_sample: Sample
    ) -> None:
        validator.validate(valid_sample)  # should not raise

    def test_total_yield_computation(
        self, validator: SampleValidator, valid_sample: Sample
    ) -> None:
        yield_ng = validator.total_yield_ng(valid_sample)
        assert yield_ng == pytest.approx(500.0, rel=1e-6)


class TestSampleValidatorParametrized:
    @pytest.mark.parametrize(
        "sample_id,concentration,volume",
        [
            ("GEN-2001", 1.0, 10.0),
            ("GEN-2002", 100.0, 50.0),
            ("GEN-2003", 0.5, 5.0),  # exact boundary values
        ],
    )
    def test_valid_samples_pass(
        self,
        validator: SampleValidator,
        sample_id: str,
        concentration: float,
        volume: float,
    ) -> None:
        sample = Sample(sample_id, concentration, volume)
        validator.validate(sample)

    @pytest.mark.parametrize(
        "sample_id,concentration,volume,expected_message_fragment",
        [
            ("", 25.0, 20.0, "blank"),
            ("GEN-3001", 0.1, 20.0, "concentration"),
            ("GEN-3002", 25.0, 1.0, "volume"),
        ],
    )
    def test_invalid_samples_raise(
        self,
        validator: SampleValidator,
        sample_id: str,
        concentration: float,
        volume: float,
        expected_message_fragment: str,
    ) -> None:
        sample = Sample(sample_id, concentration, volume)
        with pytest.raises(InvalidSampleError, match=expected_message_fragment):
            validator.validate(sample)


class TestSampleValidatorFilesystem:
    def test_write_manifest_creates_expected_file(
        self, validator: SampleValidator, valid_sample: Sample, tmp_path: Path
    ) -> None:
        destination = tmp_path / "manifest.csv"

        result_path = validator.write_manifest([valid_sample], destination)

        assert result_path.exists()
        content = result_path.read_text(encoding="utf-8")
        assert "GEN-1001" in content
        assert content.count("\n") == 0  # single sample, no trailing newline


class TestSampleValidatorEdgeCases:
    def test_total_yield_rejects_invalid_sample(self, validator: SampleValidator) -> None:
        invalid = Sample(sample_id="GEN-4001", concentration_ng_ul=0.0, volume_ul=20.0)
        with pytest.raises(InvalidSampleError):
            validator.total_yield_ng(invalid)

    def test_validate_whitespace_only_id_is_rejected(
        self, validator: SampleValidator
    ) -> None:
        sample = Sample(sample_id="   ", concentration_ng_ul=25.0, volume_ul=20.0)
        with pytest.raises(InvalidSampleError, match="blank"):
            validator.validate(sample)
