"""if/else binary decisions in scientific data."""


class ExpressionBinary:
    def __init__(self, value: float, threshold: float) -> None:
        self.value = value
        self.threshold = threshold

    def label(self) -> str:
        if self.value >= self.threshold:
            return "HIGH"
        else:
            return "LOW"


class SampleQualityCheck:
    def __init__(self, quality: float) -> None:
        self.quality = quality

    def status(self) -> str:
        if self.quality >= 30.0:
            return "PASS"
        else:
            return "FAIL"


class SequencePresenceGate:
    def __init__(self, sequence: str) -> None:
        self.sequence = sequence

    def description(self) -> str:
        if self.sequence:
            return f"Sequence present: length={len(self.sequence)}"
        else:
            return "Sequence absent"


if __name__ == "__main__":
    print(ExpressionBinary(2.5, 1.0).label())

    print(SampleQualityCheck(28.0).status())

    print(SequencePresenceGate("ATGC").description())
    print(SequencePresenceGate("").description())
