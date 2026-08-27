from __future__ import annotations

from typing import Any


class _CelsiusDisplay:
    """Non-data descriptor computing a formatted display string."""

    def __get__(self, instance: Any, owner: type) -> str:
        if instance is None:
            return "unset"
        return f"{instance.temperature_c:.1f} C"


class _BoundedMeasurement:
    """Data descriptor enforcing a numeric range on assignment."""

    def __init__(self, minimum: float, maximum: float) -> None:
        self.minimum = minimum
        self.maximum = maximum
        self._name = ""

    def __set_name__(self, owner: type, name: str) -> None:
        self._name = f"_{name}"

    def __get__(self, instance: Any, owner: type) -> float:
        if instance is None:
            return self  # type: ignore[return-value]
        return getattr(instance, self._name)

    def __set__(self, instance: Any, value: float) -> None:
        if not (self.minimum <= value <= self.maximum):
            raise ValueError(
                f"value {value} outside allowed range [{self.minimum}, {self.maximum}]"
            )
        setattr(instance, self._name, value)


class _ValidatedField:
    """Generic descriptor enforcing type, range, and non-null constraints,
    reused across multiple unrelated scientific record classes."""

    def __init__(self, minimum: float, maximum: float, unit: str) -> None:
        self.minimum = minimum
        self.maximum = maximum
        self.unit = unit
        self._name = ""

    def __set_name__(self, owner: type, name: str) -> None:
        self._name = f"_{name}"

    def __get__(self, instance: Any, owner: type) -> float:
        if instance is None:
            return self  # type: ignore[return-value]
        value = getattr(instance, self._name, None)
        if value is None:
            raise AttributeError(f"{self._name[1:]} has not been set")
        return value

    def __set__(self, instance: Any, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self._name[1:]} must be numeric, got {type(value).__name__}")
        if not (self.minimum <= value <= self.maximum):
            raise ValueError(
                f"{self._name[1:]} must be within [{self.minimum}, {self.maximum}] {self.unit}, got {value}"
            )
        setattr(instance, self._name, float(value))

    def __delete__(self, instance: Any) -> None:
        raise AttributeError(f"{self._name[1:]} cannot be deleted; it is a required measurement")


class UniversityDescriptors:
    """Demonstrates a simple non-data descriptor exposing a computed value."""

    class Sample:
        display = _CelsiusDisplay()

        def __init__(self, temperature_c: float) -> None:
            self.temperature_c = temperature_c

    @staticmethod
    def run() -> None:
        sample = UniversityDescriptors.Sample(21.6)
        print(sample.display)


class InterviewDescriptors:
    """Demonstrates a data descriptor enforcing validation on assignment,
    showing why descriptors centralize repeated validation logic."""

    class SoilSample:
        ph = _BoundedMeasurement(minimum=0.0, maximum=14.0)

        def __init__(self, ph: float) -> None:
            self.ph = ph

    @staticmethod
    def run() -> None:
        sample = InterviewDescriptors.SoilSample(ph=6.5)
        print(f"ph={sample.ph}")

        try:
            sample.ph = 15.2
        except ValueError as exc:
            print(f"caught expected error: {exc}")


class IndustryDescriptors:
    """Demonstrates a reusable descriptor framework for validated laboratory
    measurements, applied across a domain class with distinct units and
    tolerances per field, avoiding duplicated validation logic."""

    class GrowthChamberReading:
        temperature = _ValidatedField(minimum=-10.0, maximum=60.0, unit="C")
        humidity = _ValidatedField(minimum=0.0, maximum=100.0, unit="%")
        co2_ppm = _ValidatedField(minimum=0.0, maximum=5000.0, unit="ppm")

        def __init__(self, temperature: float, humidity: float, co2_ppm: float) -> None:
            self.temperature = temperature
            self.humidity = humidity
            self.co2_ppm = co2_ppm

        def __repr__(self) -> str:
            return (
                f"GrowthChamberReading(temperature={self.temperature}C, "
                f"humidity={self.humidity}%, co2_ppm={self.co2_ppm}ppm)"
            )

    @staticmethod
    def run() -> None:
        reading = IndustryDescriptors.GrowthChamberReading(temperature=24.5, humidity=55.0, co2_ppm=420.0)
        print(reading)

        try:
            reading.humidity = 150.0
        except ValueError as exc:
            print(f"caught expected error: {exc}")

        try:
            del reading.temperature
        except AttributeError as exc:
            print(f"caught expected error: {exc}")


if __name__ == "__main__":
    UniversityDescriptors.run()
    InterviewDescriptors.run()
    IndustryDescriptors.run()
