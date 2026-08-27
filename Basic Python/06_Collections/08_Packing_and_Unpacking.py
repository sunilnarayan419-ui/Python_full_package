"""08_Packing_and_Unpacking.py — Python packing and unpacking through plant science and genomics."""
from __future__ import annotations


class PlantMeasurementUnpackerUniversity:
    """University level: simple tuple packing and unpacking."""

    def __init__(self) -> None:
        self.measurement: tuple[str, float, int] = ("WHT-001", 28.5, 12)

    def unpack_and_display(self) -> None:
        sample_id, height, leaves = self.measurement
        print(f"University — Unpacked: {sample_id}, {height} cm, {leaves} leaves")

    @staticmethod
    def run() -> None:
        demo = PlantMeasurementUnpackerUniversity()
        demo.unpack_and_display()


class GenomicRecordUnpackerInterview:
    """Interview level: unpack scientific records cleanly."""

    def __init__(self, records: list[tuple[str, str, int, int]]) -> None:
        self.records = records

    def extract_gene_ranges(self) -> list[tuple[str, int]]:
        ranges: list[tuple[str, int]] = []
        for gene_id, chrom, start, end in self.records:
            length = end - start + 1
            ranges.append((gene_id, length))
        return ranges

    @staticmethod
    def run() -> None:
        records: list[tuple[str, str, int, int]] = [
            ("AT1G01010", "Chr1", 3631, 5899),
            ("AT1G01020", "Chr1", 6788, 9130),
            ("AT2G02010", "Chr2", 5000, 8000),
        ]
        demo = GenomicRecordUnpackerInterview(records)
        ranges = demo.extract_gene_ranges()
        print("Interview — Gene ranges:")
        for gene_id, length in ranges:
            print(f"  {gene_id}: {length} bp")


class SampleMetadataUnpackerIndustry:
    """Industry level: extended unpacking for readable scientific data processing."""

    def __init__(self, records: list[tuple[str, str, str, float, int, str]]) -> None:
        self.records = records

    def summarize(self) -> dict[str, dict[str, float | int]]:
        summary: dict[str, dict[str, float | int]] = {}
        for sample_id, species, tissue, height, leaves, *rest in self.records:
            summary[sample_id] = {
                "height_cm": height,
                "leaf_count": leaves,
                "notes": rest[0] if rest else "",
            }
        return summary

    @staticmethod
    def run() -> None:
        records: list[tuple[str, str, str, float, int, str]] = [
            ("WHT-001", "Triticum aestivum", "leaf", 28.5, 12, "healthy"),
            ("WHT-002", "Triticum aestivum", "root", 32.1, 15, "stressed"),
            ("RCE-001", "Oryza sativa", "stem", 25.8, 10),
        ]
        unpacker = SampleMetadataUnpackerIndustry(records)
        summary = unpacker.summarize()
        print("Industry — Sample summaries:")
        for sid, data in summary.items():
            print(f"  {sid}: height={data['height_cm']} cm, leaves={data['leaf_count']}, notes={data['notes']!r}")


if __name__ == "__main__":
    PlantMeasurementUnpackerUniversity.run()
    print()
    GenomicRecordUnpackerInterview.run()
    print()
    SampleMetadataUnpackerIndustry.run()