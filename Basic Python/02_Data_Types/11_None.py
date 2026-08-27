"""Using None to represent missing/unknown scientific data."""


class NoneUniversity:
    def __init__(self, sample_id: str, height_cm: float | None) -> None:
        self.sample_id = sample_id
        self.height_cm = height_cm

    def get_height(self) -> float | None:
        return self.height_cm

    @staticmethod
    def run() -> None:
        s = NoneUniversity(sample_id="P001", height_cm=None)
        print(f"Height: {s.get_height()}")


class NoneInterview:
    def __init__(self, measurements: list[float | None]) -> None:
        self.measurements = measurements

    def count_missing(self) -> int:
        return sum(1 for m in self.measurements if m is None)

    def count_present(self) -> int:
        return sum(1 for m in self.measurements if m is not None)

    @staticmethod
    def run() -> None:
        data = [12.5, None, 14.0, None, 11.8]
        checker = NoneInterview(data)
        print(f"Missing: {checker.count_missing()}")
        print(f"Present: {checker.count_present()}")


class NoneIndustry:
    def __init__(self, field: str, value: float | None) -> None:
        self.field = field
        self.value = value

    def is_reported(self) -> bool:
        return self.value is not None

    def display(self) -> str:
        if self.value is None:
            return f"{self.field}: NA"
        return f"{self.field}: {self.value}"


if __name__ == "__main__":
    NoneUniversity.run()
    NoneInterview.run()
    NoneIndustry.run()

    chlorophyll = NoneIndustry(field="Chlorophyll", value=None)
    print(chlorophyll.display())
