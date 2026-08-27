from __future__ import annotations

from typing import Any


class UniversityClassMethods:
    """Demonstrates a @classmethod used as an alternative constructor."""

    class Sample:
        def __init__(self, sample_id: str, weight_g: float) -> None:
            self.sample_id = sample_id
            self.weight_g = weight_g

        @classmethod
        def from_csv_row(cls, row: str) -> "UniversityClassMethods.Sample":
            sample_id, weight_g = row.split(",")
            return cls(sample_id, float(weight_g))

    @staticmethod
    def run() -> None:
        sample = UniversityClassMethods.Sample.from_csv_row("leaf-01,3.42")
        print(f"{sample.sample_id}: {sample.weight_g}g")


class InterviewClassMethods:
    """Demonstrates class methods for alternative constructors and
    class-level configuration/counters shared across all instances."""

    class ExperimentBatch:
        _default_unit = "mg"
        _batch_count = 0

        def __init__(self, batch_id: str, unit: str | None = None) -> None:
            self.batch_id = batch_id
            self.unit = unit or self._default_unit
            type(self)._batch_count += 1

        @classmethod
        def set_default_unit(cls, unit: str) -> None:
            cls._default_unit = unit

        @classmethod
        def batch_count(cls) -> int:
            return cls._batch_count

        @classmethod
        def from_prefix(cls, prefix: str, index: int) -> "InterviewClassMethods.ExperimentBatch":
            return cls(f"{prefix}-{index:03d}")

    @staticmethod
    def run() -> None:
        InterviewClassMethods.ExperimentBatch.set_default_unit("ug")
        batch_a = InterviewClassMethods.ExperimentBatch.from_prefix("trial", 1)
        batch_b = InterviewClassMethods.ExperimentBatch.from_prefix("trial", 2)
        print(f"{batch_a.batch_id} unit={batch_a.unit}")
        print(f"{batch_b.batch_id} unit={batch_b.unit}")
        print(f"total batches created: {InterviewClassMethods.ExperimentBatch.batch_count()}")


class IndustryClassMethods:
    """Demonstrates classmethods enabling polymorphic alternative
    constructors that correctly propagate through subclasses, plus a
    registry pattern for constructing domain objects from raw records."""

    class Measurement:
        registry: dict[str, type["IndustryClassMethods.Measurement"]] = {}

        def __init__(self, value: float, unit: str) -> None:
            self.value = value
            self.unit = unit

        def __init_subclass__(cls, **kwargs: Any) -> None:
            super().__init_subclass__(**kwargs)
            cls.registry[cls.__name__] = cls

        @classmethod
        def from_record(cls, record: dict[str, Any]) -> "IndustryClassMethods.Measurement":
            """Alternative constructor validating a raw dictionary record.
            Uses cls() so subclasses build the correct type."""
            if "value" not in record or "unit" not in record:
                raise KeyError("record must contain 'value' and 'unit'")
            return cls(float(record["value"]), str(record["unit"]))

        @classmethod
        def create_by_name(cls, name: str, record: dict[str, Any]) -> "IndustryClassMethods.Measurement":
            measurement_cls = cls.registry.get(name)
            if measurement_cls is None:
                raise ValueError(f"unknown measurement type: {name}")
            return measurement_cls.from_record(record)

        def __repr__(self) -> str:
            return f"{type(self).__name__}(value={self.value}, unit='{self.unit}')"

    class TemperatureMeasurement(Measurement):
        pass

    class HumidityMeasurement(Measurement):
        pass

    @staticmethod
    def run() -> None:
        temp = IndustryClassMethods.TemperatureMeasurement.from_record({"value": 22.5, "unit": "C"})
        print(temp)

        created = IndustryClassMethods.Measurement.create_by_name(
            "HumidityMeasurement", {"value": 63.0, "unit": "%"}
        )
        print(created)

        try:
            IndustryClassMethods.Measurement.create_by_name("PressureMeasurement", {"value": 1.0, "unit": "atm"})
        except ValueError as exc:
            print(f"caught expected error: {exc}")


if __name__ == "__main__":
    UniversityClassMethods.run()
    InterviewClassMethods.run()
    IndustryClassMethods.run()
