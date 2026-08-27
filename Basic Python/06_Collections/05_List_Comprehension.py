"""05_List_Comprehension.py — Python list comprehensions through plant science and genomics."""

from __future__ import annotations


class PlantHeightConverterUniversity:
    """University level: transform plant heights with list comprehensions."""

    def __init__(self, heights_cm: list[float]) -> None:
        self.heights_cm = heights_cm

    def convert_to_meters(self) -> list[float]:
        return [height / 100 for height in self.heights_cm]

    @staticmethod
    def run() -> None:
        heights = [28.5, 32.1, 25.8, 30.0, 27.3]

        demo = PlantHeightConverterUniversity(heights)
        meters = demo.convert_to_meters()

        print("University — Heights in meters:")
        for cm, meter in zip(heights, meters):
            print(f"  {cm} cm -> {meter} m")


class GeneExpressionFilterInterview:
    """Interview level: filter and transform genomic records."""

    def __init__(self, records: list[dict[str, str | float]]) -> None:
        self.records = records

    def high_expression_gene_ids(self, threshold: float) -> list[str]:
        return [
            str(record["gene_id"])
            for record in self.records
            if isinstance(record.get("gene_id"), str)
            and isinstance(record.get("expression"), (int, float))
            and record["expression"] > threshold
        ]

    @staticmethod
    def run() -> None:
        records: list[dict[str, str | float]] = [
            {"gene_id": "AT1G01010", "expression": 12.5},
            {"gene_id": "AT1G01020", "expression": 3.2},
            {"gene_id": "AT1G01030", "expression": 8.3},
            {"gene_id": "AT1G01040", "expression": 15.1},
        ]

        demo = GeneExpressionFilterInterview(records)
        high = demo.high_expression_gene_ids(threshold=8.0)

        print("Interview — High-expression gene IDs (> 8.0 FPKM):")
        for gene_id in high:
            print(f"  {gene_id}")


class SequenceQualityTransformerIndustry:
    """Industry level: readable data transformation using list comprehensions."""

    def __init__(self, sequences: list[dict[str, str | int]]) -> None:
        self.sequences = sequences

    def compute_gc_contents(self) -> list[float]:
        results: list[float] = []

        for sequence_record in self.sequences:
            dna = sequence_record.get("sequence", "")

            if not isinstance(dna, str) or not dna:
                results.append(0.0)
                continue

            gc_count = sum(
                1
                for base in dna.upper()
                if base in "GC"
            )

            results.append(round(gc_count / len(dna) * 100, 2))

        return results

    def valid_sequences(
        self,
        min_length: int,
    ) -> list[dict[str, str | int]]:
        return [
            sequence
            for sequence in self.sequences
            if isinstance(sequence.get("sequence"), str)
            and len(sequence["sequence"]) >= min_length
        ]

    @staticmethod
    def run() -> None:
        sequences: list[dict[str, str | int]] = [
            {
                "seq_id": "SEQ001",
                "sequence": "ATGCGTACGGTTA",
                "organism": "Arabidopsis",
            },
            {
                "seq_id": "SEQ002",
                "sequence": "CGGCGGCGGC",
                "organism": "Wheat",
            },
            {
                "seq_id": "SEQ003",
                "sequence": "ATATATAT",
                "organism": "Rice",
            },
        ]

        transformer = SequenceQualityTransformerIndustry(sequences)

        gc_contents = transformer.compute_gc_contents()
        valid = transformer.valid_sequences(min_length=10)

        print("Industry — Sequence quality metrics:")

        for sequence, gc in zip(sequences, gc_contents):
            print(f"  {sequence['seq_id']}: GC = {gc}%")

        print("Valid sequences (>= 10 bp):")

        for sequence in valid:
            print(
                f"  {sequence['seq_id']}: "
                f"{sequence['sequence']}"
            )


if __name__ == "__main__":
    PlantHeightConverterUniversity.run()

    print()

    GeneExpressionFilterInterview.run()

    print()

    SequenceQualityTransformerIndustry.run()