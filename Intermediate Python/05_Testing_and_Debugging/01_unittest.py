"""Production-quality unittest suite for a plant measurement processing service."""

from __future__ import annotations

import unittest
from dataclasses import dataclass
from statistics import mean


class InvalidMeasurementError(ValueError):
    """Raised when a scientific measurement fails validation."""


@dataclass(frozen=True, slots=True)
class PlantMeasurement:
    sample_id: str
    height_cm: float
    leaf_count: int


class PlantMeasurementProcessor:
    """Validates and aggregates plant growth measurements.

    Encapsulates the domain rules for what constitutes a physically
    plausible measurement and provides summary statistics used by
    downstream analysis pipelines.
    """

    MIN_HEIGHT_CM = 0.0
    MAX_HEIGHT_CM = 500.0

    def validate(self, measurement: PlantMeasurement) -> None:
        if not measurement.sample_id:
            raise InvalidMeasurementError("sample_id must not be empty")
        if not (self.MIN_HEIGHT_CM <= measurement.height_cm <= self.MAX_HEIGHT_CM):
            raise InvalidMeasurementError(
                f"height_cm={measurement.height_cm} outside plausible range "
                f"[{self.MIN_HEIGHT_CM}, {self.MAX_HEIGHT_CM}]"
            )
        if measurement.leaf_count < 0:
            raise InvalidMeasurementError("leaf_count cannot be negative")

    def process_batch(self, measurements: list[PlantMeasurement]) -> dict[str, float]:
        if not measurements:
            raise InvalidMeasurementError("cannot process an empty measurement batch")

        for measurement in measurements:
            self.validate(measurement)

        heights = [m.height_cm for m in measurements]
        leaf_counts = [m.leaf_count for m in measurements]

        return {
            "mean_height_cm": mean(heights),
            "max_height_cm": max(heights),
            "mean_leaf_count": mean(leaf_counts),
            "sample_count": float(len(measurements)),
        }


class TestPlantMeasurementProcessor(unittest.TestCase):
    """Behavioral tests for PlantMeasurementProcessor."""

    def setUp(self) -> None:
        # Fresh processor per test; the processor is stateless but this
        # keeps tests explicit and resilient to future internal state.
        self.processor = PlantMeasurementProcessor()

    def test_validate_accepts_plausible_measurement(self) -> None:
        measurement = PlantMeasurement(sample_id="S-001", height_cm=42.5, leaf_count=6)
        self.processor.validate(measurement)  # should not raise

    def test_validate_rejects_empty_sample_id(self) -> None:
        measurement = PlantMeasurement(sample_id="", height_cm=42.5, leaf_count=6)
        with self.assertRaises(InvalidMeasurementError):
            self.processor.validate(measurement)

    def test_validate_rejects_negative_leaf_count(self) -> None:
        measurement = PlantMeasurement(sample_id="S-002", height_cm=10.0, leaf_count=-1)
        with self.assertRaises(InvalidMeasurementError):
            self.processor.validate(measurement)

    def test_validate_boundary_heights(self) -> None:
        # Boundary conditions at the exact min/max thresholds.
        with self.subTest(boundary="min"):
            self.processor.validate(
                PlantMeasurement(sample_id="S-003", height_cm=0.0, leaf_count=1)
            )
        with self.subTest(boundary="max"):
            self.processor.validate(
                PlantMeasurement(sample_id="S-004", height_cm=500.0, leaf_count=1)
            )
        with self.subTest(boundary="just_over_max"):
            with self.assertRaises(InvalidMeasurementError):
                self.processor.validate(
                    PlantMeasurement(sample_id="S-005", height_cm=500.01, leaf_count=1)
                )

    def test_process_batch_computes_expected_statistics(self) -> None:
        measurements = [
            PlantMeasurement(sample_id="S-010", height_cm=10.0, leaf_count=2),
            PlantMeasurement(sample_id="S-011", height_cm=20.0, leaf_count=4),
            PlantMeasurement(sample_id="S-012", height_cm=30.0, leaf_count=6),
        ]

        result = self.processor.process_batch(measurements)

        self.assertAlmostEqual(result["mean_height_cm"], 20.0, places=6)
        self.assertAlmostEqual(result["max_height_cm"], 30.0, places=6)
        self.assertAlmostEqual(result["mean_leaf_count"], 4.0, places=6)
        self.assertEqual(result["sample_count"], 3.0)

    def test_process_batch_rejects_empty_input(self) -> None:
        with self.assertRaises(InvalidMeasurementError):
            self.processor.process_batch([])

    def test_process_batch_propagates_validation_failure(self) -> None:
        measurements = [
            PlantMeasurement(sample_id="S-020", height_cm=15.0, leaf_count=3),
            PlantMeasurement(sample_id="S-021", height_cm=-5.0, leaf_count=3),
        ]
        with self.assertRaises(InvalidMeasurementError):
            self.processor.process_batch(measurements)

    def test_process_batch_result_is_none_free(self) -> None:
        measurements = [PlantMeasurement(sample_id="S-030", height_cm=12.0, leaf_count=2)]
        result = self.processor.process_batch(measurements)
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
