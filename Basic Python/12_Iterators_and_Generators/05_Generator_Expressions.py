"""Generator expressions: lazy evaluation, filtering/mapping, vs list comprehensions."""


class UniversityGeneratorExpressions:
    def __init__(self, plant_records: list[dict]) -> None:
        self.plant_records = plant_records

    def height_generator_expression(self):
        """A generator expression producing heights lazily."""
        return (record["height_cm"] for record in self.plant_records)

    def tall_species_generator_expression(self, threshold: float):
        return (
            record["species"]
            for record in self.plant_records
            if record["height_cm"] >= threshold
        )

    @staticmethod
    def run() -> None:
        data = [
            {"sample_id": "P001", "species": "Wheat", "height_cm": 28.5},
            {"sample_id": "P002", "species": "Rice", "height_cm": 31.2},
            {"sample_id": "P003", "species": "Barley", "height_cm": 22.0},
        ]

        demo = UniversityGeneratorExpressions(data)
        height_gen = demo.height_generator_expression()
        print(f"Generator expression type: {type(height_gen).__name__}")
        print(f"Heights (consumed lazily): {list(height_gen)}")

        tall_gen = demo.tall_species_generator_expression(25.0)
        print(f"Species taller than 25cm: {list(tall_gen)}")


class InterviewGeneratorExpressions:
    def __init__(self, records: list[dict]) -> None:
        self.records = records

    def safe_gene_expression_values(self, key: str):
        """Generator expression that defensively skips missing/invalid values."""
        return (
            record[key]
            for record in self.records
            if isinstance(record.get(key), (int, float)) and record.get(key) >= 0
        )

    @staticmethod
    def run() -> None:
        empty_case: list[dict] = []
        processor = InterviewGeneratorExpressions(empty_case)
        result_empty = list(processor.safe_gene_expression_values("expression_level"))
        print(f"Empty records -> valid expression values: {result_empty}")

        messy_case = [
            {"gene": "wus1", "expression_level": 4.2},
            {"gene": "zmm4", "expression_level": -1.0},
            {"gene": "sb_drought1", "expression_level": "high"},
            {"gene": "cry1ab", "expression_level": 7.8},
        ]
        processor = InterviewGeneratorExpressions(messy_case)
        result_messy = list(processor.safe_gene_expression_values("expression_level"))
        print(f"Messy records -> valid expression values: {result_messy}")

        list_comp_result = [
            r["expression_level"]
            for r in messy_case
            if isinstance(r.get("expression_level"), (int, float))
            and r.get("expression_level") >= 0
        ]
        print(f"Equivalent list comprehension result: {list_comp_result}")


class IndustryGeneratorExpressions:
    def __init__(self, experiment_data: list[dict]) -> None:
        self.data = experiment_data

    def high_expression_gene_names(self, threshold: float):
        """Lazily filters and maps gene names above an expression threshold.

        Uses a generator expression to avoid building an intermediate
        list for large datasets.
        """
        return (
            record["gene"]
            for record in self.data
            if record.get("expression_level", 0.0) >= threshold
        )

    def process(self, threshold: float = 5.0) -> dict[str, object]:
        matching_genes = list(self.high_expression_gene_names(threshold))
        return {
            "total_genes": len(self.data),
            "threshold": threshold,
            "high_expression_count": len(matching_genes),
            "high_expression_genes": matching_genes,
        }

    @staticmethod
    def run() -> None:
        sample_data = [
            {"gene": "wus1", "expression_level": 4.2},
            {"gene": "zmm4", "expression_level": 6.1},
            {"gene": "sb_drought1", "expression_level": 8.9},
            {"gene": "cry1ab", "expression_level": 2.5},
        ]

        processor = IndustryGeneratorExpressions(sample_data)
        report = processor.process(threshold=5.0)
        print(f"Experiment report: {report}")


if __name__ == "__main__":
    UniversityGeneratorExpressions.run()
    InterviewGeneratorExpressions.run()
    IndustryGeneratorExpressions.run()
