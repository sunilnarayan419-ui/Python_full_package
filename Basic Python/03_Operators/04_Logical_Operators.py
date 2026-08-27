"""Logical operators in scientific workflows."""


class SampleEligibility:
    def __init__(self, height_cm: float, leaf_count: int) -> None:
        self.height_cm = height_cm
        self.leaf_count = leaf_count

    def is_healthy(self) -> bool:
        return self.height_cm > 20 and self.leaf_count >= 5


class PhenotypeRule:
    def __init__(self, height_cm: float, disease_present: bool) -> None:
        self.height_cm = height_cm
        self.disease_present = disease_present

    def is_eligible(self) -> bool:
        return self.height_cm > 30 or not self.disease_present


class SequencingSampleValidator:
    def __init__(self, min_quality: float, min_length: int, contamination: bool) -> None:
        self.min_quality = min_quality
        self.min_length = min_length
        self.contamination = contamination

    def is_valid(self, quality: float, length: int) -> bool:
        if self.contamination:
            return False
        return quality >= self.min_quality and length >= self.min_length


if __name__ == "__main__":
    print(SampleEligibility(45.0, 8).is_healthy())

    print(PhenotypeRule(25.0, disease_present=True).is_eligible())

    v = SequencingSampleValidator(min_quality=30.0, min_length=100, contamination=False)
    print(v.is_valid(quality=35.0, length=120))
