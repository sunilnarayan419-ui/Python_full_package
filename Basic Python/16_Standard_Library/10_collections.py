"""Demonstrates the collections module for biological data aggregation."""

from collections import Counter, defaultdict, deque


class UniversityCollections:
    """Introduces Counter for tallying mutation types in a dataset."""

    def __init__(self, mutation_types: list[str]) -> None:
        self.mutation_types = mutation_types

    def count_mutation_types(self) -> Counter[str]:
        return Counter(self.mutation_types)

    @staticmethod
    def run() -> None:
        mutations = ["missense", "silent", "missense", "nonsense", "silent", "missense"]
        demo = UniversityCollections(mutations)

        counts = demo.count_mutation_types()
        print(f"Mutation type counts: {dict(counts)}")
        print(f"Most common mutation: {counts.most_common(1)}")


class InterviewCollections:
    """Solves a species-grouping problem using defaultdict, with edge cases."""

    def group_measurements_by_species(
        self, records: list[tuple[str, float]]
    ) -> dict[str, list[float]]:
        """Group plant height measurements by species name.

        Returns an empty dict for empty input rather than raising, since an
        empty dataset is a valid (if uninteresting) grouping result.
        """
        grouped: defaultdict[str, list[float]] = defaultdict(list)
        for species, height in records:
            if not species:
                raise ValueError("species name must not be empty.")
            grouped[species].append(height)
        return dict(grouped)

    @staticmethod
    def run() -> None:
        solver = InterviewCollections()

        # Test case 1: normal grouping
        records = [
            ("Arabidopsis", 24.5),
            ("Zea mays", 88.0),
            ("Arabidopsis", 26.1),
            ("Zea mays", 91.5),
        ]
        grouped = solver.group_measurements_by_species(records)
        print(f"Grouped measurements: {grouped}")

        # Test case 2: edge case, empty input
        empty_grouped = solver.group_measurements_by_species([])
        print(f"Grouped measurements (empty input): {empty_grouped}")

        # Test case 3: edge case, invalid species name
        try:
            solver.group_measurements_by_species([("", 10.0)])
        except ValueError as error:
            print(f"Handled invalid species name: {error}")


class IndustryCollections:
    """Reusable sample-processing queue and aggregation utility."""

    def __init__(self, max_queue_size: int = 100) -> None:
        self.processing_queue: deque[str] = deque(maxlen=max_queue_size)

    def enqueue_sample(self, sample_id: str) -> None:
        """Add a sample to the processing queue, evicting the oldest if full."""
        self.processing_queue.append(sample_id)

    def process_next(self) -> str | None:
        """Pop and return the next sample in FIFO order, or None if empty."""
        if not self.processing_queue:
            return None
        return self.processing_queue.popleft()

    def aggregate_gene_counts(self, gene_hits: list[str]) -> dict[str, int]:
        """Aggregate gene hit counts using Counter, sorted by frequency."""
        counts = Counter(gene_hits)
        return dict(counts.most_common())

    @staticmethod
    def run() -> None:
        manager = IndustryCollections(max_queue_size=3)

        for sample_id in ["sample_001", "sample_002", "sample_003", "sample_004"]:
            manager.enqueue_sample(sample_id)

        print(f"Queue after enqueueing (maxlen=3): {list(manager.processing_queue)}")
        print(f"Processing next sample: {manager.process_next()}")

        gene_hits = ["BRCA1", "TP53", "BRCA1", "EGFR", "TP53", "BRCA1"]
        aggregated = manager.aggregate_gene_counts(gene_hits)
        print(f"Aggregated gene hit counts: {aggregated}")


if __name__ == "__main__":
    UniversityCollections.run()
    InterviewCollections.run()
    IndustryCollections.run()
