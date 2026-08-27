"""continue to skip invalid scientific records."""


class HeightFilter:
    def __init__(self, samples: list[dict], min_cm: float) -> None:
        self.samples = samples
        self.min_cm = min_cm

    def valid_heights(self) -> list[float]:
        result: list[float] = []
        for s in self.samples:
            height = s.get("height_cm")
            if height is None:
                continue
            if height < self.min_cm:
                continue
            result.append(height)
        return result


class SequenceCleaner:
    def __init__(self, sequence: str) -> None:
        self.sequence = sequence.upper()

    def keep_dna(self) -> str:
        kept: list[str] = []
        for base in self.sequence:
            if base not in "ACGT":
                continue
            kept.append(base)
        return "".join(kept)


class QualityRecordProcessor:
    def __init__(self, records: list[dict], min_quality: float) -> None:
        self.records = records
        self.min_quality = min_quality

    def passed(self) -> list[dict]:
        result: list[dict] = []
        for r in self.records:
            if r.get("quality", 0) < self.min_quality:
                continue
            result.append(r)
        return result


if __name__ == "__main__":
    print(HeightFilter([
        {"id": "P1", "height_cm": 25.0},
        {"id": "P2", "height_cm": None},
        {"id": "P3", "height_cm": 10.0},
    ], min_cm=15.0).valid_heights())

    print(SequenceCleaner("ATGCNX").keep_dna())

    print(QualityRecordProcessor([
        {"id": "S1", "quality": 35.0},
        {"id": "S2", "quality": 20.0},
    ], min_quality=30.0).passed())
