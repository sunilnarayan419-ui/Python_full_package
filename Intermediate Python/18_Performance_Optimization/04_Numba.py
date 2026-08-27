from __future__ import annotations

import time
from typing import Callable, TypeVar

import numpy as np

try:
    from numba import njit
    _NUMBA_AVAILABLE = True
except ImportError:
    _NUMBA_AVAILABLE = False

    def njit(*args: object, **kwargs: object) -> Callable[..., Callable[..., object]]:  # type: ignore[misc]
        def decorator(func: Callable[..., object]) -> Callable[..., object]:
            return func

        if len(args) == 1 and callable(args[0]) and not kwargs:
            return args[0]  # type: ignore[return-value]
        return decorator

T = TypeVar("T")


def _pairwise_distance_numpy(coordinates: np.ndarray) -> np.ndarray:
    """Baseline pairwise Euclidean distance between molecular coordinate points."""
    diff = coordinates[:, None, :] - coordinates[None, :, :]
    return np.sqrt(np.sum(diff * diff, axis=-1))


@njit(cache=True)
def _pairwise_distance_numba(coordinates: np.ndarray) -> np.ndarray:
    n_points = coordinates.shape[0]
    n_dims = coordinates.shape[1]
    output = np.zeros((n_points, n_points), dtype=np.float64)
    for i in range(n_points):
        for j in range(n_points):
            accumulator = 0.0
            for d in range(n_dims):
                delta = coordinates[i, d] - coordinates[j, d]
                accumulator += delta * delta
            output[i, j] = accumulator ** 0.5
    return output


class MolecularDistanceBenchmark:
    """Compares NumPy vectorized vs Numba-JIT pairwise distance computation.

    Workload: pairwise Euclidean distances between simulated atomic
    coordinates, a common step in molecular structure analysis.
    """

    def __init__(self, num_points: int, num_dimensions: int = 3, seed: int = 5) -> None:
        if num_points <= 0:
            raise ValueError("num_points must be positive")
        rng = np.random.default_rng(seed)
        self.coordinates = rng.uniform(low=-10.0, high=10.0, size=(num_points, num_dimensions))

    def baseline_numpy(self) -> np.ndarray:
        return _pairwise_distance_numpy(self.coordinates)

    def optimized_numba(self) -> np.ndarray:
        if not _NUMBA_AVAILABLE:
            raise RuntimeError(
                "numba is not installed. Install it with 'pip install numba' to enable "
                "JIT-compiled pairwise distance computation."
            )
        return _pairwise_distance_numba(self.coordinates)

    def benchmark(self, function: Callable[..., T], *args: object, **kwargs: object) -> tuple[T, float]:
        start = time.perf_counter()
        result = function(*args, **kwargs)
        elapsed = time.perf_counter() - start
        return result, elapsed

    @staticmethod
    def run() -> None:
        benchmark_suite = MolecularDistanceBenchmark(num_points=350, seed=9)

        baseline_result, baseline_elapsed = benchmark_suite.benchmark(benchmark_suite.baseline_numpy)
        print(f"numpy baseline: {baseline_elapsed:.6f}s")

        if not _NUMBA_AVAILABLE:
            print(
                "numba not installed; skipping JIT benchmark. "
                "Install with 'pip install numba' to enable it."
            )
            return

        # Warm-up call to trigger JIT compilation before timing steady-state execution.
        benchmark_suite.optimized_numba()

        optimized_result, optimized_elapsed = benchmark_suite.benchmark(benchmark_suite.optimized_numba)
        print(f"numba steady-state: {optimized_elapsed:.6f}s")

        if not np.allclose(baseline_result, optimized_result, atol=1e-8):
            raise RuntimeError("Optimized implementation changed the numerical result.")

        speedup = baseline_elapsed / optimized_elapsed if optimized_elapsed > 0 else float("inf")
        print(f"speedup: {speedup:.2f}x")


if __name__ == "__main__":
    MolecularDistanceBenchmark.run()
