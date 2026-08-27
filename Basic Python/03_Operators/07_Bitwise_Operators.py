"""Bitwise operators for compact genomic quality flags."""


PASS_QC = 0b0001
PASS_LENGTH = 0b0010
PASS_CONTAMINATION = 0b0100
PASS_REFERENCE = 0b1000


class QualityFlags:
    def __init__(self, flags: int) -> None:
        self.flags = flags

    def all_passed(self) -> bool:
        mask = PASS_QC | PASS_LENGTH | PASS_CONTAMINATION | PASS_REFERENCE
        return (self.flags & mask) == mask

    def failed_qc(self) -> bool:
        return (self.flags & PASS_QC) == 0


class SampleFlagsBuilder:
    def __init__(self) -> None:
        self.flags = 0

    def set(self, flag: int) -> None:
        self.flags |= flag

    def clear(self, flag: int) -> None:
        self.flags &= ~flag


class CompactFeatureFlags:
    EXPRESSED = 0b001
    DIFFERENTIAL = 0b010
    HOUSEKEEPING = 0b100

    def __init__(self, value: int) -> None:
        self.value = value

    def is_differential(self) -> bool:
        return (self.value & self.DIFFERENTIAL) != 0

    def shift(self, n: int) -> int:
        return self.value << n


if __name__ == "__main__":
    flags = QualityFlags(PASS_QC | PASS_LENGTH | PASS_CONTAMINATION)
    print(flags.all_passed())
    print(flags.failed_qc())

    f = CompactFeatureFlags(0b011)
    print(f.is_differential())
    print(f.shift(1))
