from __future__ import annotations

import time

import pandas as pd


class TrialPerformanceOptimizer:
    """Demonstrates production-oriented performance practices on a large trial dataset."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data.copy()

    def vectorized_biomass_index(self) -> pd.Series:
        """Compute a biomass index using vectorized operations (no Python loops)."""
        return (self.data["biomass_g"] * 10 / self.data["height_cm"]).round(3)

    def loop_based_biomass_index(self) -> list[float]:
        """Reference implementation using an explicit Python loop, for benchmarking only."""
        results: list[float] = []
        for biomass, height in zip(self.data["biomass_g"], self.data["height_cm"]):
            results.append(round(biomass * 10 / height, 3))
        return results

    def benchmark_vectorized_vs_loop(self) -> dict[str, float]:
        """Compare execution time of vectorized vs loop-based computation."""
        start = time.perf_counter()
        self.vectorized_biomass_index()
        vectorized_time = time.perf_counter() - start

        start = time.perf_counter()
        self.loop_based_biomass_index()
        loop_time = time.perf_counter() - start

        return {"vectorized_seconds": vectorized_time, "loop_seconds": loop_time}

    def efficient_filter(self, threshold: float) -> pd.DataFrame:
        """Filter using a precomputed boolean mask instead of repeated attribute lookups."""
        mask = self.data["biomass_g"].to_numpy() > threshold
        return self.data.loc[mask]

    def efficient_groupby_aggregation(self) -> pd.DataFrame:
        """Perform a single-pass groupby aggregation instead of multiple separate calls."""
        return self.data.groupby("treatment", observed=True).agg(
            mean_biomass_g=("biomass_g", "mean"),
            mean_height_cm=("height_cm", "mean"),
            sample_count=("sample_id", "count"),
        )

    def optimize_dtypes(self) -> pd.DataFrame:
        """Downcast numeric columns and convert low-cardinality strings to category dtype."""
        optimized = self.data.copy()
        optimized["treatment"] = optimized["treatment"].astype("category")
        optimized["height_cm"] = pd.to_numeric(optimized["height_cm"], downcast="float")
        optimized["biomass_g"] = pd.to_numeric(optimized["biomass_g"], downcast="float")
        return optimized

    def memory_usage_report(self, frame: pd.DataFrame) -> pd.Series:
        """Return per-column memory usage in bytes."""
        return frame.memory_usage(deep=True)

    def in_place_column_update(self) -> pd.DataFrame:
        """Update a column without creating an unnecessary intermediate copy."""
        updated = self.data.copy()
        updated["biomass_g"] = updated["biomass_g"].where(updated["biomass_g"] > 0, other=0.0)
        return updated

    @staticmethod
    def run() -> None:
        sample_count = 5000
        data = pd.DataFrame(
            {
                "sample_id": [f"S{i:05d}" for i in range(sample_count)],
                "treatment": pd.Series(["control", "nitrogen_high", "drought_stress"] * (sample_count // 3 + 1))[:sample_count],
                "height_cm": pd.Series(range(sample_count), dtype="float64") % 60 + 5,
                "biomass_g": pd.Series(range(sample_count), dtype="float64") % 15 + 0.5,
            }
        )

        optimizer = TrialPerformanceOptimizer(data)

        print(optimizer.benchmark_vectorized_vs_loop())
        print(optimizer.efficient_filter(threshold=12.0).shape)
        print(optimizer.efficient_groupby_aggregation())

        original_memory = optimizer.memory_usage_report(data).sum()
        optimized_data = optimizer.optimize_dtypes()
        optimized_memory = optimizer.memory_usage_report(optimized_data).sum()

        print({"original_bytes": int(original_memory), "optimized_bytes": int(optimized_memory)})
        print(optimizer.in_place_column_update().head())


if __name__ == "__main__":
    TrialPerformanceOptimizer.run()
