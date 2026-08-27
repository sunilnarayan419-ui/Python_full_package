"""03_List_Slicing.py — Python list slicing through plant science and genomics."""
from __future__ import annotations


class DnaSequenceSlicerUniversity:
    """University level: simple list slicing with start, stop, step."""

    def __init__(self, nucleotides: list[str]) -> None:
        self.nucleotides = nucleotides

    def demonstrate_slicing(self) -> None:
        print("University — DNA nucleotide list:")
        print(f"  Full:       {self.nucleotides}")
        print(f"  [2:6]:      {self.nucleotides[2:6]}")
        print(f"  [:4]:       {self.nucleotides[:4]}")
        print(f"  [5:]:       {self.nucleotides[5:]}")
        print(f"  [::2]:      {self.nucleotides[::2]}")
        print(f"  [-4:-1]:    {self.nucleotides[-4:-1]}")

    @staticmethod
    def run() -> None:
        seq = list("ATGCGTACGGTTA")
        demo = DnaSequenceSlicerUniversity(seq)
        demo.demonstrate_slicing()


class PlantSampleSubsetExtractorInterview:
    """Interview level: extract subsets of biological records."""

    def __init__(self, samples: list[dict[str, str | float]]) -> None:
        self.samples = samples

    def extract_range(self, start: int, stop: int, step: int = 1) -> list[dict[str, str | float]]:
        return self.samples[start:stop:step]

    @staticmethod
    def run() -> None:
        samples: list[dict[str, str | float]] = [
            {"id": "S001", "species": "Wheat", "height_cm": 28.5},
            {"id": "S002", "species": "Rice", "height_cm": 32.1},
            {"id": "S003", "species": "Maize", "height_cm": 25.8},
            {"id": "S004", "species": "Barley", "height_cm": 30.0},
            {"id": "S005", "species": "Soybean", "height_cm": 27.3},
            {"id": "S006", "species": "Tomato", "height_cm": 35.0},
        ]
        extractor = PlantSampleSubsetExtractorInterview(samples)
        print("Interview — Sample subsets:")
        print(f"  [1:4]:   {extractor.extract_range(1, 4)}")
        print(f"  [::2]:   {extractor.extract_range(0, None, 2)}")
        print(f"  [-3:]:   {extractor.extract_range(-3, None)}")


class GenomicWindowExtractorIndustry:
    """Industry level: data-windowing component for scientific records."""

    def __init__(self, records: list[dict[str, str | int]]) -> None:
        self.records = records

    def sliding_window(self, window_size: int, step: int) -> list[list[dict[str, str | int]]]:
        if window_size <= 0 or step <= 0:
            raise ValueError("window_size and step must be positive")
        windows: list[list[dict[str, str | int]]] = []
        for i in range(0, len(self.records) - window_size + 1, step):
            windows.append(self.records[i:i + window_size])
        return windows

    @staticmethod
    def run() -> None:
        records: list[dict[str, str | int]] = [
            {"gene_id": "AT1G01010", "start": 3631, "end": 5899},
            {"gene_id": "AT1G01020", "start": 6788, "end": 9130},
            {"gene_id": "AT1G01030", "start": 11649, "end": 13714},
            {"gene_id": "AT1G01040", "start": 23146, "end": 31227},
            {"gene_id": "AT1G01050", "start": 33666, "end": 37840},
        ]
        extractor = GenomicWindowExtractorIndustry(records)
        print("Industry — Sliding windows (size=3, step=1):")
        for idx, window in enumerate(extractor.sliding_window(3, 1), 1):
            ids = [r["gene_id"] for r in window]
            print(f"  Window {idx}: {ids}")


if __name__ == "__main__":
    DnaSequenceSlicerUniversity.run()
    print()
    PlantSampleSubsetExtractorInterview.run()
    print()
    GenomicWindowExtractorIndustry.run()