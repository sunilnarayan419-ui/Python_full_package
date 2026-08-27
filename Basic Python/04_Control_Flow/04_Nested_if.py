"""Nested if statements for dependent scientific decisions."""


class SampleExistenceCheck:
    def __init__(self, height_cm: float | None, threshold: float) -> None:
        self.height_cm = height_cm
        self.threshold = threshold

    def passes(self) -> bool:
        if self.height_cm is not None:
            if self.height_cm > self.threshold:
                return True
        return False


class SequenceValidation:
    def __init__(self, sequence: str, min_length: int, gc: float) -> None:
        self.sequence = sequence
        self.min_length = min_length
        self.gc = gc

    def is_valid(self) -> bool:
        if self.sequence:
            if len(self.sequence) >= self.min_length:
                if 0.3 <= self.gc <= 0.7:
                    return True
        return False


class PhenotypeAcceptance:
    def __init__(self, plant: dict, disease_free: bool) -> None:
        self.plant = plant
        self.disease_free = disease_free

    def accepted(self) -> bool:
        if self.plant.get("height_cm") is not None:
            height = self.plant["height_cm"]
            if height > 20:
                if self.disease_free:
                    return True
        return False


if __name__ == "__main__":
    print(SampleExistenceCheck(45.0, 30.0).passes())

    print(SequenceValidation("ATGCATGC", min_length=5, gc=0.5).is_valid())

    p = PhenotypeAcceptance(plant={"height_cm": 35.0}, disease_free=True)
    print(p.accepted())
