"""zip(): combining multiple biological iterables into paired/aligned data."""


class UniversityZip:
    def __init__(self, plant_ids: list[str], heights_cm: list[float]) -> None:
        self.plant_ids = plant_ids
        self.heights_cm = heights_cm

    def pair_ids_with_heights(self) -> list[tuple[str, float]]:
        return list(zip(self.plant_ids, self.heights_cm))

    @staticmethod
    def run() -> None:
        plant_ids = ["P001", "P002", "P003"]
        heights_cm = [28.5, 31.2, 24.0]

        processor = UniversityZip(plant_ids, heights_cm)
        pairs = processor.pair_ids_with_heights()

        print(f"Plant IDs: {plant_ids}")
        print(f"Heights: {heights_cm}")
        print(f"Paired (id, height): {pairs}")


class InterviewZip:
    def __init__(self, species: list[str], observations: list[str]) -> None:
        self.species = species
        self.observations = observations

    def safe_pair(self) -> list[tuple[str, str]]:
        """zip() silently truncates to the shortest iterable; demonstrate that."""
        return list(zip(self.species, self.observations))

    def strict_pair(self) -> list[tuple[str, str]] | str:
        """Uses strict=True to catch mismatched lengths explicitly."""
        try:
            return list(zip(self.species, self.observations, strict=True))
        except ValueError as error:
            return f"Length mismatch detected: {error}"

    @staticmethod
    def run() -> None:
        species_equal = ["Wheat", "Rice"]
        observations_equal = ["healthy", "stressed"]
        processor = InterviewZip(species_equal, observations_equal)
        print(f"Equal-length pairing: {processor.safe_pair()}")
        print(f"Equal-length strict pairing: {processor.strict_pair()}")

        species_unequal = ["Wheat", "Rice", "Barley"]
        observations_unequal = ["healthy", "stressed"]
        processor = InterviewZip(species_unequal, observations_unequal)
        print(f"Unequal-length lenient pairing: {processor.safe_pair()}")
        print(f"Unequal-length strict pairing: {processor.strict_pair()}")


class IndustryZip:
    def __init__(
        self,
        gene_names: list[str],
        expression_values: list[float],
        sample_ids: list[str],
    ) -> None:
        self.gene_names = gene_names
        self.expression_values = expression_values
        self.sample_ids = sample_ids

    def build_expression_records(self) -> list[dict]:
        """Aligns three related data sources into structured records.

        Uses strict=True so silent data misalignment is never tolerated
        in a production scientific pipeline.
        """
        try:
            combined = zip(
                self.sample_ids,
                self.gene_names,
                self.expression_values,
                strict=True,
            )
        except ValueError as error:
            raise ValueError(f"Cannot align mismatched data sources: {error}") from error

        return [
            {"sample_id": sample_id, "gene": gene, "expression_level": level}
            for sample_id, gene, level in combined
        ]

    def process(self) -> dict[str, object]:
        records = self.build_expression_records()
        return {
            "total_records": len(records),
            "records": records,
        }

    @staticmethod
    def run() -> None:
        sample_ids = ["RNA001", "RNA002", "RNA003"]
        gene_names = ["GA20ox", "WUS1", "CRY1AB"]
        expression_values = [12.4, 8.7, 18.2]

        processor = IndustryZip(gene_names, expression_values, sample_ids)
        report = processor.process()
        print(f"Experiment report: {report}")


if __name__ == "__main__":
    UniversityZip.run()
    InterviewZip.run()
    IndustryZip.run()
