from __future__ import annotations

import time
from typing import Callable, TypeVar

import numpy as np

T = TypeVar("T")


class GeneExpressionVectorizationWorkflow:
    """Compares loop-based vs vectorized z-score normalization of expression data.

    Workload: normalizing a gene-by-sample expression matrix (z-score per
    gene) followed by a log-fold-change style transformation, a common
    preprocessing step in transcriptomics pipelines.
    """

    def __init__(self, num_genes: int, num_samples: int, seed: int = 6) -> None:
        if num_genes <= 0 or num_samples <= 0:
            raise ValueError("num_genes and num_samples must be positive")
        rng = np.random.default_rng(seed)
        raw = rng.uniform(low=0.1, high=500.0, size=(num_genes, num_samples))
        self.expression_matrix = np.asarray(raw, dtype=float)

    def baseline_loop(self) -> np.ndarray:
        num_genes, num_samples = self.expression_matrix.shape
        result = np.zeros((num_genes, num_samples), dtype=float)
        for gene_index in range(num_genes):
            row = self.expression_matrix[gene_index]
            row_mean = 0.0
            for value in row:
                row_mean += value
            row_mean /= num_samples

            variance = 0.0
            for value in row:
                variance += (value - row_mean) ** 2
            variance /= num_samples
            std_dev = variance ** 0.5 if variance > 0 else 1.0

            for sample_index in range(num_samples):
                z_score = (row[sample_index] - row_mean) / std_dev
                result[gene_index, sample_index] = np.log1p(abs(z_score)) * (1 if z_score >= 0 else -1)
        return result

    def vectorized(self) -> np.ndarray:
        matrix = self.expression_matrix
        row_mean = matrix.mean(axis=1, keepdims=True)
        row_std = matrix.std(axis=1, keepdims=True)
        row_std = np.where(row_std == 0, 1.0, row_std)
        z_scores = (matrix - row_mean) / row_std
        return np.sign(z_scores) * np.log1p(np.abs(z_scores))

    def benchmark(self, function: Callable[..., T], *args: object, **kwargs: object) -> tuple[T, float]:
        start = time.perf_counter()
        result = function(*args, **kwargs)
        elapsed = time.perf_counter() - start
        return result, elapsed

    @staticmethod
    def run() -> None:
        workflow = GeneExpressionVectorizationWorkflow(num_genes=400, num_samples=60, seed=19)

        baseline_result, baseline_elapsed = workflow.benchmark(workflow.baseline_loop)
        print(f"loop baseline: {baseline_elapsed:.6f}s")

        vectorized_result, vectorized_elapsed = workflow.benchmark(workflow.vectorized)
        print(f"vectorized: {vectorized_elapsed:.6f}s")

        if not np.allclose(baseline_result, vectorized_result, atol=1e-8):
            raise RuntimeError("Optimized implementation changed the numerical result.")

        speedup = baseline_elapsed / vectorized_elapsed if vectorized_elapsed > 0 else float("inf")
        print(f"speedup: {speedup:.2f}x")


if __name__ == "__main__":
    GeneExpressionVectorizationWorkflow.run()
