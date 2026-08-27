"""06_Tuples.py — Python tuples through plant science and genomics."""
from __future__ import annotations


class PlantMeasurementTupleUniversity:
    """University level: tuples as fixed biological measurements."""

    def __init__(self, sample_id: str, height_cm: float, leaf_count: int) -> None:
        self.record: tuple[str, float, int] = (sample_id, height_cm, leaf_count)

    def display(self) -> None:
        sample_id, height, leaves = self.record
        print(f"University — Sample: {sample_id}, Height: {height} cm, Leaves: {leaves}")

    @staticmethod
    def run() -> None:
        demo = PlantMeasurementTupleUniversity("WHT-001", 28.5, 12)
        demo.display()


class GenomicCoordinateInterview:
    """Interview level: immutable scientific metadata for genomic coordinates."""

    def __init__(self, coordinates: list[tuple[str, int, int, str]]) -> None:
        self.coordinates = coordinates

    def find_in_range(self, chrom: str, start: int, end: int) -> list[tuple[str, int, int, str]]:
        return [
            coord for coord in self.coordinates
            if coord[0] == chrom and not (coord[2] < start or coord[1] > end)
        ]

    @staticmethod
    def run() -> None:
        coords: list[tuple[str, int, int, str]] = [
            ("Chr1", 3631, 5899, "AT1G01010"),
            ("Chr1", 6788, 9130, "AT1G01020"),
            ("Chr2", 5000, 8000, "AT2G02010"),
        ]
        demo = GenomicCoordinateInterview(coords)
        found = demo.find_in_range("Chr1", 4000, 7000)
        print("Interview — Genes overlapping Chr1:4000-7000:")
        for c in found:
            print(f"  {c[3]}: {c[0]}:{c[1]}-{c[2]}")


class SequenceRecordFactoryIndustry:
    """Industry level: tuples for fixed records and immutable return values."""

    @staticmethod
    def parse_fasta_header(header: str) -> tuple[str, str, str]:
        parts = header.strip().split("|")
        if len(parts) < 3:
            raise ValueError("header must contain at least 3 pipe-separated fields")
        return (parts[0], parts[1], parts[2])

    @staticmethod
    def run() -> None:
        header = "sp|AT1G01010|TOC1_ARATH"
        record = SequenceRecordFactoryIndustry.parse_fasta_header(header)
        print("Industry — Parsed FASTA header:")
        print(f"  Database:   {record[0]}")
        print(f"  Gene ID:    {record[1]}")
        print(f"  Protein:    {record[2]}")
        print(f"  Full tuple: {record}")


if __name__ == "__main__":
    PlantMeasurementTupleUniversity.run()
    print()
    GenomicCoordinateInterview.run()
    print()
    SequenceRecordFactoryIndustry.run()