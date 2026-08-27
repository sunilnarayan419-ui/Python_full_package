"""Basic if statement applied to plant/genomic data."""


class HeightThresholdScreener:
    def __init__(self, height_cm: float, threshold_cm: float) -> None:
        self.height_cm = height_cm
        self.threshold_cm = threshold_cm

    def passes(self) -> bool:
        if self.height_cm > self.threshold_cm:
            return True
        return False


class PlantSampleGate:
    def __init__(self, samples: list[dict]) -> None:
        self.samples = samples

    def find_tall(self) -> list[dict]:
        tall: list[dict] = []
        for s in self.samples:
            if s["height_cm"] > 30:
                tall.append(s)
        return tall


class SequencePresenceCheck:
    def __init__(self, sequence: str) -> None:
        self.sequence = sequence

    def has_data(self) -> bool:
        if self.sequence:
            return True
        return False


if __name__ == "__main__":
    print(HeightThresholdScreener(45.0, 30.0).passes())

    gate = PlantSampleGate([
        {"id": "P1", "height_cm": 35.0},
        {"id": "P2", "height_cm": 20.0},
    ])
    print(gate.find_tall())

    print(SequencePresenceCheck("ATGC").has_data())
