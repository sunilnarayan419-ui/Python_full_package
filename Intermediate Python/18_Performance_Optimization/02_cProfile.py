from __future__ import annotations

import cProfile
import io
import pstats
import random
import time
from typing import Callable, TypeVar

T = TypeVar("T")


class GeneExpressionProfiler:
    """Programmatic cProfile workflow over a gene-expression aggregation task."""

    def __init__(self, num_genes: int, num_samples: int, seed: int = 11) -> None:
        if num_genes <= 0 or num_samples <= 0:
            raise ValueError("num_genes and num_samples must be positive")
        self.num_genes = num_genes
        self.num_samples = num_samples
        self.expression_matrix = self._generate_matrix(num_genes, num_samples, seed)

    @staticmethod
    def _generate_matrix(num_genes: int, num_samples: int, seed: int) -> list[list[float]]:
        rng = random.Random(seed)
        return [[rng.uniform(0.0, 100.0) for _ in range(num_samples)] for _ in range(num_genes)]

    def normalize_row(self, row: list[float]) -> list[float]:
        row_sum = sum(row)
        if row_sum == 0:
            return [0.0 for _ in row]
        return [value / row_sum for value in row]

    def compute_row_variance(self, row: list[float]) -> float:
        mean = sum(row) / len(row)
        return sum((value - mean) ** 2 for value in row) / len(row)

    def workload(self) -> dict[str, float]:
        normalized = [self.normalize_row(row) for row in self.expression_matrix]
        variances = [self.compute_row_variance(row) for row in normalized]
        return {
            "mean_variance": sum(variances) / len(variances),
            "max_variance": max(variances),
        }

    def benchmark(self, function: Callable[..., T], *args: object, **kwargs: object) -> tuple[T, float]:
        start = time.perf_counter()
        result = function(*args, **kwargs)
        elapsed = time.perf_counter() - start
        return result, elapsed

    def profile_workload(self) -> cProfile.Profile:
        profiler = cProfile.Profile()
        profiler.enable()
        self.workload()
        profiler.disable()
        return profiler

    def run_profile(self, sort_key: pstats.SortKey = pstats.SortKey.CUMULATIVE, top_n: int = 10) -> str:
        profiler = self.profile_workload()
        stream = io.StringIO()
        stats = pstats.Stats(profiler, stream=stream).strip_dirs()
        stats.sort_stats(sort_key)
        stats.print_stats(top_n)
        return stream.getvalue()

    def most_expensive_function(self) -> tuple[str, float]:
        profiler = self.profile_workload()
        stats = pstats.Stats(profiler)
        stats.sort_stats(pstats.SortKey.CUMULATIVE)
        entries = stats.stats.items()  # type: ignore[attr-defined]
        worst_name = ""
        worst_cumulative = -1.0
        for func_key, raw_stats in entries:
            cumulative_time = raw_stats[3]
            if cumulative_time > worst_cumulative:
                worst_cumulative = cumulative_time
                worst_name = f"{func_key[0]}:{func_key[1]}({func_key[2]})"
        return worst_name, worst_cumulative

    @staticmethod
    def run() -> None:
        profiler_workflow = GeneExpressionProfiler(num_genes=2_000, num_samples=40, seed=3)

        _, elapsed = profiler_workflow.benchmark(profiler_workflow.workload)
        print(f"workload direct timing: {elapsed:.6f}s")

        report = profiler_workflow.run_profile(top_n=10)
        print("cProfile cumulative-time report:")
        print(report)

        worst_name, worst_cumulative = profiler_workflow.most_expensive_function()
        print(f"Most expensive function: {worst_name} ({worst_cumulative:.6f}s cumulative)")


if __name__ == "__main__":
    GeneExpressionProfiler.run()
