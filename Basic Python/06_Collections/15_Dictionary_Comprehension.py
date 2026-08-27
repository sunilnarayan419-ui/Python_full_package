"""15_Dictionary_Comprehension.py — Python dictionary comprehensions through plant science and genomics."""
from __future__ import annotations


class PlantHeightMapUniversity:
    """University level: simple transformation into a dictionary."""

    def __init__(self, samples: list[tuple[str, float]]) -> None:
        self.samples = samples

    def build_map(self) -> dict[str, float]:
        return {sample_id: height for sample_id, height in self.samples}

    @staticmethod
    def run() -> None:
        samples = [("WHT-001", 28.5), ("WHT-002", 32.1), ("WHT-003", 25.8)]
        demo = PlantHeightMapUniversity(samples)
        height_map = demo.build_map()
        print("University — Sample height map:")
        for sid, h in height_map.items():
            print(f"  {sid}: {h} cm")


class GeneExpressionFilterMapInterview:
    """Interview level: transform and filter scientific records."""

    def __init__(self, records: list[dict[str, str | float]]) -> None:
        self.records = records

    def high_expression_map(self, threshold: float) -> dict[str, float]:
        return {
            rec["gene_id"]: float(rec["expression"])
            for rec in self.records
            if isinstance(rec.get("expression"), (int, float)) and rec["expression"] > threshold
        }

    @staticmethod
    def run() -> None:
        records: list[dict[str, str | float]] = [
            {"gene_id": "AT1G01010", "expression": 12.5},
            {"gene_id": "AT1G01020", "expression": 3.2},
            {"gene_id": "AT1G01030", "expression": 8.3},
            {"gene_id": "AT1G01040", "expression": 15.1},
        ]
        demo = GeneExpressionFilterMapInterview(records)
        high = demo.high_expression_map(threshold=8.0)
        print("Interview — High-expression map (> 8.0 FPKM):")
        for gid, expr in high.items():
            print(f"  {gid}: {expr} FPKM")


class SequenceGcTransformerIndustry:
    """Industry level: concise data-transformation component."""

    def __init__(self, sequences: list[dict[str, str]]) -> None:
        self.sequences = sequences

    def gc_content_map(self) -> dict[str, float]:
        result: dict[str, float] = {}
        for seq in self.sequences:
            sid = seq.get("seq_id", "")
            dna = seq.get("sequence", "")
            if not isinstance(sid, str) or not isinstance(dna, str) or not dna:
                continue
            gc = sum(1 for base in dna.upper() if base in "GC") / len(dna) * 100
            result[sid] = round(gc, 2)
        return result

    def filtered_map(self, min_gc: float) -> dict[str, float]:
        full = self.gc_content_map()
        return {sid: gc for sid, gc in full.items() if gc >= min_gc}

    @staticmethod
    def run() -> None:
        sequences: list[dict[str, str]] = [
            {"seq_id": "SEQ001", "sequence": "ATGCGTACGGTTA"},
            {"seq_id": "SEQ002", "sequence": "CGGCGGCGGC"},
            {"seq_id": "SEQ003", "sequence": "ATATATAT"},
        ]
        transformer = SequenceGcTransformerIndustry(sequences)
        all_gc = transformer.gc_content_map()
        high_gc = transformer.filtered_map(min_gc=50.0)
        print("Industry — GC content transformation:")
        print(f"  All:  {all_gc}")
        print(f"  >=50: {high_gc}")


if __name__ == "__main__":
    PlantHeightMapUniversity.run()
    print()
    GeneExpressionFilterMapInterview.run()
    print()
    SequenceGcTransformerIndustry.run()