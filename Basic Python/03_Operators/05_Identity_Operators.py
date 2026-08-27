"""Identity operators in scientific data handling."""


class OptionalMeasurement:
    def __init__(self, value: float | None) -> None:
        self.value = value

    def is_missing(self) -> bool:
        return self.value is None

    def equals(self, other: "OptionalMeasurement") -> bool:
        return self.value is other.value


class MetadataRecord:
    def __init__(self, source: str | None) -> None:
        self.source = source

    def has_source(self) -> bool:
        return self.source is not None


class SequenceRecord:
    def __init__(self, header: str, sequence: str | None) -> None:
        self.header = header
        self.sequence = sequence

    def is_blank(self) -> bool:
        return self.sequence is None


if __name__ == "__main__":
    a = OptionalMeasurement(value=None)
    b = OptionalMeasurement(value=10.0)
    print(a.is_missing())
    print(a.equals(b))

    m = MetadataRecord(source=None)
    print(m.has_source())

    s = SequenceRecord(header="S001", sequence=None)
    print(s.is_blank())
