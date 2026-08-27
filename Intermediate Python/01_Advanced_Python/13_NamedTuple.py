from __future__ import annotations

from collections import namedtuple
from typing import NamedTuple


class UniversityNamedTuple:
    """Demonstrates collections.namedtuple for a simple immutable record."""

    LeafMeasurement = namedtuple("LeafMeasurement", ["length_cm", "width_cm"])

    @staticmethod
    def run() -> None:
        leaf = UniversityNamedTuple.LeafMeasurement(length_cm=8.2, width_cm=3.5)
        print(leaf)
        print(f"length={leaf.length_cm} width={leaf[1]}")


class InterviewNamedTuple:
    """Demonstrates typing.NamedTuple with type hints, default values, and
    a derived method, showing why the typed variant is preferred in modern
    code over collections.namedtuple."""

    class SoilReading(NamedTuple):
        ph: float
        moisture_percent: float
        location: str = "unspecified"

        def is_acidic(self) -> bool:
            return self.ph < 7.0

    @staticmethod
    def run() -> None:
        reading = InterviewNamedTuple.SoilReading(ph=6.2, moisture_percent=34.5, location="plot-A")
        print(reading)
        print(f"is_acidic={reading.is_acidic()}")

        default_location_reading = InterviewNamedTuple.SoilReading(ph=7.5, moisture_percent=20.0)
        print(default_location_reading)


class IndustryNamedTuple:
    """Demonstrates typing.NamedTuple used as a lightweight, immutable,
    hashable value object in a production data pipeline: comparable,
    unpackable, and safely usable as a dictionary key or set member."""

    class SequenceCoordinate(NamedTuple):
        chromosome: str
        start: int
        end: int

        def length(self) -> int:
            return self.end - self.start

        def overlaps(self, other: "IndustryNamedTuple.SequenceCoordinate") -> bool:
            if self.chromosome != other.chromosome:
                return False
            return self.start < other.end and other.start < self.end

    @staticmethod
    def merge_coordinates(
        coordinates: list["IndustryNamedTuple.SequenceCoordinate"],
    ) -> list["IndustryNamedTuple.SequenceCoordinate"]:
        SequenceCoordinate = IndustryNamedTuple.SequenceCoordinate
        by_chromosome: dict[str, list[SequenceCoordinate]] = {}
        for coord in coordinates:
            by_chromosome.setdefault(coord.chromosome, []).append(coord)

        merged: list[SequenceCoordinate] = []
        for chrom, coords in by_chromosome.items():
            for coord in sorted(coords, key=lambda c: c.start):
                if merged and merged[-1].overlaps(coord) and merged[-1].chromosome == chrom:
                    last = merged.pop()
                    merged.append(SequenceCoordinate(chrom, last.start, max(last.end, coord.end)))
                else:
                    merged.append(coord)
        return merged

    @staticmethod
    def run() -> None:
        SequenceCoordinate = IndustryNamedTuple.SequenceCoordinate
        coordinates = [
            SequenceCoordinate("chr1", 100, 200),
            SequenceCoordinate("chr1", 150, 300),
            SequenceCoordinate("chr1", 500, 600),
            SequenceCoordinate("chr2", 10, 50),
        ]

        for coord in coordinates:
            print(f"{coord} length={coord.length()}")

        merged = IndustryNamedTuple.merge_coordinates(coordinates)
        print(f"merged intervals: {merged}")

        coordinate_set = {coordinates[0], coordinates[1]}
        print(f"usable in a set: {coordinate_set}")


if __name__ == "__main__":
    UniversityNamedTuple.run()
    InterviewNamedTuple.run()
    IndustryNamedTuple.run()
