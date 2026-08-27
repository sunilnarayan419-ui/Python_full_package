"""Demonstrates itertools for memory-efficient scientific data pipelines."""

from itertools import chain, combinations, groupby, islice, product


class UniversityItertools:
    """Introduces basic iterator tools using experimental treatment combinations."""

    def __init__(self, treatments: list[str]) -> None:
        self.treatments = treatments

    def all_pairs(self) -> list[tuple[str, str]]:
        return list(combinations(self.treatments, 2))

    @staticmethod
    def run() -> None:
        treatments = ["control", "drug_A", "drug_B", "drug_C"]
        demo = UniversityItertools(treatments)

        pairs = demo.all_pairs()
        print(f"Treatment pairs to test: {pairs}")


class InterviewItertools:
    """Solves a Cartesian-product experimental-design problem, with edge cases."""

    def build_experimental_conditions(
        self, concentrations: list[float], temperatures: list[float]
    ) -> list[tuple[float, float]]:
        """Build every concentration/temperature combination for a plate design.

        Raises ValueError for empty inputs, since an empty design list would
        silently skip an entire experimental run.
        """
        if not concentrations or not temperatures:
            raise ValueError("concentrations and temperatures must not be empty.")
        return list(product(concentrations, temperatures))

    def take_first_n_conditions(
        self, conditions: list[tuple[float, float]], n: int
    ) -> list[tuple[float, float]]:
        """Lazily take the first n conditions without materializing extra work."""
        if n < 0:
            raise ValueError("n must not be negative.")
        return list(islice(conditions, n))

    @staticmethod
    def run() -> None:
        solver = InterviewItertools()

        # Test case 1: normal combination
        conditions = solver.build_experimental_conditions(
            concentrations=[0.1, 0.5, 1.0], temperatures=[25.0, 37.0]
        )
        print(f"Experimental conditions ({len(conditions)}): {conditions}")

        limited = solver.take_first_n_conditions(conditions, n=3)
        print(f"First 3 conditions to run today: {limited}")

        # Test case 2: edge case, empty input
        try:
            solver.build_experimental_conditions([], [25.0])
        except ValueError as error:
            print(f"Handled empty input: {error}")


class IndustryItertools:
    """Memory-efficient, lazy scientific data pipeline built on itertools."""

    def stream_batches(self, records: list[dict[str, str]], batch_size: int):
        """Yield successive batches from records without loading them all at once.

        Uses islice on an iterator so that only batch_size records are realized
        into a list at a time, keeping memory use bounded for large datasets.
        """
        if batch_size <= 0:
            raise ValueError("batch_size must be positive.")

        iterator = iter(records)
        while batch := list(islice(iterator, batch_size)):
            yield batch

    def group_by_species(self, records: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
        """Group pre-sorted records by species using groupby.

        Records must already be sorted by species, since itertools.groupby only
        groups consecutive equal keys rather than performing a full sort itself.
        """
        sorted_records = sorted(records, key=lambda record: record["species"])
        grouped: dict[str, list[dict[str, str]]] = {}
        for species, group in groupby(sorted_records, key=lambda record: record["species"]):
            grouped[species] = list(group)
        return grouped

    def merge_sample_sources(
        self, *sources: list[dict[str, str]]
    ) -> chain[dict[str, str]]:
        """Lazily chain multiple sample record sources into a single iterator."""
        return chain(*sources)

    @staticmethod
    def run() -> None:
        pipeline = IndustryItertools()

        records = [
            {"id": "s1", "species": "Zea mays"},
            {"id": "s2", "species": "Arabidopsis"},
            {"id": "s3", "species": "Zea mays"},
            {"id": "s4", "species": "Oryza sativa"},
        ]

        batches = list(pipeline.stream_batches(records, batch_size=2))
        print(f"Streamed batches: {batches}")

        grouped = pipeline.group_by_species(records)
        print(f"Grouped by species: {[k for k in grouped]}")

        extra_records = [{"id": "s5", "species": "Oryza sativa"}]
        merged = pipeline.merge_sample_sources(records, extra_records)
        merged_ids = [record["id"] for record in merged]
        print(f"Merged sample IDs (lazy chain consumed): {merged_ids}")


if __name__ == "__main__":
    UniversityItertools.run()
    InterviewItertools.run()
    IndustryItertools.run()
