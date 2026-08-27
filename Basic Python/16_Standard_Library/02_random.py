"""Demonstrates the random module for experimental sampling and simulation."""

import random


class UniversityRandom:
    """Introduces basic random generation using a seeded generator."""

    def __init__(self, seed: int = 42) -> None:
        self.generator = random.Random(seed)

    def generate_measurement_noise(self) -> float:
        """Simulate small instrument noise added to a measurement."""
        return self.generator.random()

    def pick_random_specimen(self, specimens: list[str]) -> str:
        return self.generator.choice(specimens)

    @staticmethod
    def run() -> None:
        demo = UniversityRandom(seed=42)
        specimens = ["Arabidopsis", "Zea mays", "Oryza sativa"]

        noise = demo.generate_measurement_noise()
        chosen = demo.pick_random_specimen(specimens)

        print(f"Simulated instrument noise: {noise:.4f}")
        print(f"Randomly selected specimen: {chosen}")


class InterviewRandom:
    """Solves a reproducible randomized-group-assignment problem, with edge cases."""

    def __init__(self, seed: int = 7) -> None:
        self.generator = random.Random(seed)

    def assign_treatment_groups(
        self, sample_ids: list[str], group_names: list[str]
    ) -> dict[str, str]:
        """Randomly assign each sample to one of the provided treatment groups.

        Raises ValueError if inputs are empty, ensuring the caller cannot silently
        receive an empty or malformed assignment map.
        """
        if not sample_ids:
            raise ValueError("sample_ids must not be empty.")
        if not group_names:
            raise ValueError("group_names must not be empty.")

        return {sample_id: self.generator.choice(group_names) for sample_id in sample_ids}

    def draw_random_subset(self, population: list[str], subset_size: int) -> list[str]:
        """Draw a reproducible random subset without replacement, validating size."""
        if subset_size < 0:
            raise ValueError("subset_size cannot be negative.")
        if subset_size > len(population):
            raise ValueError("subset_size cannot exceed population size.")
        return self.generator.sample(population, subset_size)

    @staticmethod
    def run() -> None:
        solver = InterviewRandom(seed=7)

        # Test case 1: normal assignment
        samples = [f"sample_{i:03d}" for i in range(1, 7)]
        groups = ["control", "treatment_A", "treatment_B"]
        assignments = solver.assign_treatment_groups(samples, groups)
        print("Treatment assignments:", assignments)

        # Test case 2: edge case, empty sample list
        try:
            solver.assign_treatment_groups([], groups)
        except ValueError as error:
            print(f"Handled empty input: {error}")

        subset = solver.draw_random_subset(samples, subset_size=3)
        print("Random validation subset:", subset)


class IndustryRandom:
    """Controlled, reproducible simulation utility for scientific sampling workflows."""

    def __init__(self, seed: int | None = None) -> None:
        # A None seed allows non-deterministic production use, while an explicit
        # seed supports reproducible testing and audits.
        self.generator = random.Random(seed)

    def shuffle_batch_order(self, batch_ids: list[str]) -> list[str]:
        """Return a new, shuffled processing order without mutating the input."""
        ordered = list(batch_ids)
        self.generator.shuffle(ordered)
        return ordered

    def simulate_measurement_series(
        self, baseline: float, noise_scale: float, count: int
    ) -> list[float]:
        """Simulate a series of noisy measurements around a baseline value."""
        if count <= 0:
            raise ValueError("count must be positive.")
        return [
            round(baseline + self.generator.uniform(-noise_scale, noise_scale), 3)
            for _ in range(count)
        ]

    def stratified_sample(
        self, population_by_stratum: dict[str, list[str]], per_stratum: int
    ) -> dict[str, list[str]]:
        """Sample a fixed number of items from each stratum (e.g. plant species)."""
        result: dict[str, list[str]] = {}
        for stratum, items in population_by_stratum.items():
            take = min(per_stratum, len(items))
            result[stratum] = self.generator.sample(items, take)
        return result

    @staticmethod
    def run() -> None:
        simulator = IndustryRandom(seed=99)

        batches = [f"batch_{i}" for i in range(1, 6)]
        print("Shuffled batch order:", simulator.shuffle_batch_order(batches))

        series = simulator.simulate_measurement_series(baseline=25.0, noise_scale=0.5, count=5)
        print("Simulated measurement series:", series)

        population = {
            "Arabidopsis": [f"ara_{i}" for i in range(10)],
            "Zea mays": [f"maize_{i}" for i in range(10)],
        }
        sampled = simulator.stratified_sample(population, per_stratum=3)
        print("Stratified sample:", sampled)


if __name__ == "__main__":
    UniversityRandom.run()
    InterviewRandom.run()
    IndustryRandom.run()
