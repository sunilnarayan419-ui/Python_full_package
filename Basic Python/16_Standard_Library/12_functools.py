"""Demonstrates functools for reusable and cached scientific computations."""

from functools import lru_cache, partial, reduce


class UniversityFunctools:
    """Introduces basic functools usage with reduce for combining measurements."""

    def __init__(self, measurements: list[float]) -> None:
        self.measurements = measurements

    def total_biomass(self) -> float:
        return reduce(lambda accumulated, value: accumulated + value, self.measurements, 0.0)

    @staticmethod
    def run() -> None:
        measurements = [12.4, 8.9, 15.2, 10.1]
        demo = UniversityFunctools(measurements)

        total = demo.total_biomass()
        print(f"Total biomass (via reduce): {total:.1f} g")


class InterviewFunctools:
    """Solves a reusable, partially configured calculation problem with edge cases."""

    def build_unit_converter(self, factor: float):
        """Return a partial function that converts a value using a fixed factor.

        Raises ValueError for a non-positive factor, since a zero or negative
        conversion factor would silently corrupt downstream measurements.
        """
        if factor <= 0:
            raise ValueError("Conversion factor must be positive.")
        return partial(self._convert, factor=factor)

    @staticmethod
    def _convert(value: float, factor: float) -> float:
        return value * factor

    @staticmethod
    def run() -> None:
        solver = InterviewFunctools()

        # Test case 1: normal conversion, milligrams to grams
        mg_to_g = solver.build_unit_converter(factor=0.001)
        print(f"250 mg in grams: {mg_to_g(250):.3f}")

        # Test case 2: edge case, invalid factor
        try:
            solver.build_unit_converter(factor=0)
        except ValueError as error:
            print(f"Handled invalid conversion factor: {error}")


class IndustryFunctools:
    """Reusable, cached scientific computation utility using lru_cache."""

    def __init__(self) -> None:
        self._call_count = 0

    @lru_cache(maxsize=128)
    def compute_binding_score(self, ligand_id: str, receptor_id: str) -> float:
        """Simulate an expensive drug-binding affinity computation.

        Cached because the same ligand/receptor pair is often re-evaluated
        across multiple screening rounds, and recomputation is costly.
        """
        self._call_count += 1
        # Deterministic pseudo-scientific computation, not a real binding model.
        combined = f"{ligand_id}:{receptor_id}"
        return round(sum(ord(character) for character in combined) / 100, 3)

    def score_all_pairs(
        self, ligand_ids: list[str], receptor_ids: list[str]
    ) -> dict[tuple[str, str], float]:
        """Compute binding scores for all ligand/receptor pairs, reusing the cache."""
        return {
            (ligand, receptor): self.compute_binding_score(ligand, receptor)
            for ligand in ligand_ids
            for receptor in receptor_ids
        }

    @staticmethod
    def run() -> None:
        screener = IndustryFunctools()

        ligands = ["LIG_A", "LIG_B"]
        receptors = ["REC_X", "REC_Y"]

        scores = screener.score_all_pairs(ligands, receptors)
        print(f"Binding scores: {scores}")

        # Recompute the same pair to demonstrate the cache being reused.
        repeated_score = screener.compute_binding_score("LIG_A", "REC_X")
        print(f"Repeated lookup (cached): {repeated_score}")
        print(f"Cache info: {screener.compute_binding_score.cache_info()}")


if __name__ == "__main__":
    UniversityFunctools.run()
    InterviewFunctools.run()
    IndustryFunctools.run()
