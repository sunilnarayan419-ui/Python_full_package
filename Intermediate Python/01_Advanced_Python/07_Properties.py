from __future__ import annotations


class UniversityProperties:
    """Demonstrates a basic @property with a validating setter."""

    class PlantHeight:
        def __init__(self, height_cm: float) -> None:
            self._height_cm = height_cm

        @property
        def height_cm(self) -> float:
            return self._height_cm

        @height_cm.setter
        def height_cm(self, value: float) -> None:
            if value < 0:
                raise ValueError("height cannot be negative")
            self._height_cm = value

    @staticmethod
    def run() -> None:
        plant = UniversityProperties.PlantHeight(15.0)
        print(plant.height_cm)
        plant.height_cm = 18.5
        print(plant.height_cm)


class InterviewProperties:
    """Demonstrates computed read-only properties and a deletable property,
    showing properties as a clean interface over derived state."""

    class ExperimentMetadata:
        def __init__(self, start_day: int, end_day: int, sample_count: int) -> None:
            self._start_day = start_day
            self._end_day = end_day
            self._sample_count = sample_count

        @property
        def duration_days(self) -> int:
            return self._end_day - self._start_day

        @property
        def sample_count(self) -> int:
            return self._sample_count

        @sample_count.setter
        def sample_count(self, value: int) -> None:
            if value < 0:
                raise ValueError("sample_count cannot be negative")
            self._sample_count = value

        @sample_count.deleter
        def sample_count(self) -> None:
            print("sample_count reset to zero")
            self._sample_count = 0

        @property
        def samples_per_day(self) -> float:
            return self._sample_count / self.duration_days if self.duration_days else 0.0

    @staticmethod
    def run() -> None:
        metadata = InterviewProperties.ExperimentMetadata(start_day=1, end_day=8, sample_count=42)
        print(f"duration={metadata.duration_days} samples_per_day={metadata.samples_per_day:.2f}")
        del metadata.sample_count
        print(f"sample_count after delete: {metadata.sample_count}")


class IndustryProperties:
    """Demonstrates properties used to enforce invariants across dependent
    fields in a scientific domain model, keeping derived quantities always
    consistent and preventing invalid intermediate states."""

    class DoseResponseAssay:
        def __init__(self, dose_mg: float, response_percent: float) -> None:
            self._dose_mg = 0.0
            self._response_percent = 0.0
            self.dose_mg = dose_mg
            self.response_percent = response_percent

        @property
        def dose_mg(self) -> float:
            return self._dose_mg

        @dose_mg.setter
        def dose_mg(self, value: float) -> None:
            if value <= 0:
                raise ValueError("dose_mg must be positive")
            self._dose_mg = value

        @property
        def response_percent(self) -> float:
            return self._response_percent

        @response_percent.setter
        def response_percent(self, value: float) -> None:
            if not (0.0 <= value <= 100.0):
                raise ValueError("response_percent must be within [0, 100]")
            self._response_percent = value

        @property
        def potency_index(self) -> float:
            """Derived metric: response achieved per unit dose."""
            return round(self._response_percent / self._dose_mg, 4)

        @property
        def is_saturating(self) -> bool:
            return self._response_percent >= 95.0

    @staticmethod
    def run() -> None:
        assay = IndustryProperties.DoseResponseAssay(dose_mg=2.5, response_percent=68.0)
        print(f"potency_index={assay.potency_index} is_saturating={assay.is_saturating}")

        assay.response_percent = 97.5
        print(f"potency_index={assay.potency_index} is_saturating={assay.is_saturating}")

        try:
            assay.dose_mg = -1.0
        except ValueError as exc:
            print(f"caught expected error: {exc}")


if __name__ == "__main__":
    UniversityProperties.run()
    InterviewProperties.run()
    IndustryProperties.run()
