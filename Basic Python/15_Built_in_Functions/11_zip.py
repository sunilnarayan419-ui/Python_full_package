"""Demonstrations of the built-in zip() function using paired biological data."""


class UniversityZip:
    """Teach the fundamental behavior of zip() for pairing biological data."""

    def __init__(self, sample_ids: list[str], measurements: list[float]) -> None:
        self.sample_ids = sample_ids
        self.measurements = measurements

    def paired_readings(self) -> list[tuple[str, float]]:
        return list(zip(self.sample_ids, self.measurements))

    @staticmethod
    def run() -> None:
        sample_ids = ["P001", "P002", "P003"]
        measurements = [58.2, 61.4, 49.9]

        processor = UniversityZip(sample_ids, measurements)
        print(f"Paired readings: {processor.paired_readings()}")


class InterviewZip:
    """Align multiple iterables and handle unequal-length inputs safely."""

    def __init__(self, genes: list[str], expression_levels: list[float]) -> None:
        self.genes = genes
        self.expression_levels = expression_levels

    def strict_alignment(self) -> dict[str, float] | None:
        """Return an aligned mapping, or None if lengths do not match."""
        try:
            return dict(zip(self.genes, self.expression_levels, strict=True))
        except ValueError:
            return None

    def lenient_alignment(self) -> dict[str, float]:
        """Pair only up to the length of the shorter iterable."""
        return dict(zip(self.genes, self.expression_levels))

    @staticmethod
    def run() -> None:
        matched = InterviewZip(["GENE1", "GENE2"], [4.2, 9.1])
        mismatched = InterviewZip(["GENE1", "GENE2", "GENE3"], [4.2, 9.1])

        print(f"Strict alignment (matched lengths): {matched.strict_alignment()}")
        print(f"Strict alignment (mismatched lengths): {mismatched.strict_alignment()}")
        print(f"Lenient alignment (mismatched lengths): {mismatched.lenient_alignment()}")


class IndustryZip:
    """Reliably align multi-source biological data into structured records."""

    def __init__(
        self,
        sample_ids: list[str],
        species: list[str],
        phenotype_scores: list[float],
    ) -> None:
        self.sample_ids = sample_ids
        self.species = species
        self.phenotype_scores = phenotype_scores

    def build_records(self) -> list[dict[str, object]]:
        """Combine three parallel data sources into one record per sample.

        Uses strict=True so silently misaligned data sources raise an
        explicit error rather than producing truncated, incorrect records.
        """
        combined = zip(self.sample_ids, self.species, self.phenotype_scores, strict=True)
        return [
            {"sample_id": sample_id, "species": species_name, "phenotype_score": score}
            for sample_id, species_name, score in combined
        ]

    @staticmethod
    def run() -> None:
        builder = IndustryZip(
            sample_ids=["S001", "S002", "S003"],
            species=["Wheat", "Rice", "Maize"],
            phenotype_scores=[7.2, 8.9, 6.5],
        )

        for record in builder.build_records():
            print(record)


if __name__ == "__main__":
    UniversityZip.run()
    InterviewZip.run()
    IndustryZip.run()
