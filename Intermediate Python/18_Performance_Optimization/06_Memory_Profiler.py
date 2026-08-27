from __future__ import annotations

import time
from typing import Callable, Iterator, TypeVar

import numpy as np

try:
    from memory_profiler import memory_usage
    _MEMORY_PROFILER_AVAILABLE = True
except ImportError:
    _MEMORY_PROFILER_AVAILABLE = False

T = TypeVar("T")


class ExperimentalMeasurementMemoryWorkflow:
    """Contrasts a copy-heavy baseline against a streaming, low-memory pipeline.

    Workload: normalizing large batches of experimental sensor readings
    (e.g. fluorescence intensity measurements) and computing summary
    statistics. Demonstrates:
    REDUCE MEMORY ALLOCATION -> AVOID COPIES -> STREAM DATA -> MEASURE.
    """

    def __init__(self, num_batches: int, batch_size: int, seed: int = 4) -> None:
        if num_batches <= 0 or batch_size <= 0:
            raise ValueError("num_batches and batch_size must be positive")
        self.num_batches = num_batches
        self.batch_size = batch_size
        self._seed = seed

    def _generate_batch(self, rng: np.random.Generator) -> np.ndarray:
        return rng.uniform(low=0.0, high=5000.0, size=self.batch_size).astype(np.float64)

    def baseline_normalize_all(self) -> float:
        """Materializes every batch as float64 and concatenates before reducing."""
        rng = np.random.default_rng(self._seed)
        all_batches: list[np.ndarray] = []
        for _ in range(self.num_batches):
            batch = self._generate_batch(rng)
            normalized = (batch - batch.mean()) / batch.std()
            all_batches.append(normalized.copy())
        stacked = np.concatenate(all_batches)
        return float(stacked.mean())

    def _batch_stream(self) -> Iterator[np.ndarray]:
        rng = np.random.default_rng(self._seed)
        for _ in range(self.num_batches):
            yield self._generate_batch(rng)

    def streaming_normalize_all(self) -> float:
        """Streams batches with float32 dtype and running aggregation, avoiding full materialization."""
        running_sum = 0.0
        running_count = 0
        for batch in self._batch_stream():
            batch32 = batch.astype(np.float32, copy=False)
            mean = batch32.mean()
            std = batch32.std()
            if std == 0:
                continue
            normalized = (batch32 - mean) / std
            running_sum += float(normalized.sum())
            running_count += normalized.size
        return running_sum / running_count if running_count else 0.0

    def benchmark(self, function: Callable[..., T], *args: object, **kwargs: object) -> tuple[T, float]:
        start = time.perf_counter()
        result = function(*args, **kwargs)
        elapsed = time.perf_counter() - start
        return result, elapsed

    def profile_memory(self, function: Callable[..., T]) -> tuple[T, float]:
        if not _MEMORY_PROFILER_AVAILABLE:
            raise RuntimeError(
                "memory_profiler is not installed. Install it with 'pip install memory_profiler' "
                "to enable peak memory measurement."
            )
        usage_samples, result = memory_usage((function,), retval=True, interval=0.01)
        peak_mb = max(usage_samples) - min(usage_samples)
        return result, peak_mb

    @staticmethod
    def run() -> None:
        workflow = ExperimentalMeasurementMemoryWorkflow(num_batches=200, batch_size=20_000, seed=13)

        baseline_result, baseline_elapsed = workflow.benchmark(workflow.baseline_normalize_all)
        print(f"baseline: mean={baseline_result:.6f}, elapsed={baseline_elapsed:.6f}s")

        streaming_result, streaming_elapsed = workflow.benchmark(workflow.streaming_normalize_all)
        print(f"streaming: mean={streaming_result:.6f}, elapsed={streaming_elapsed:.6f}s")

        if not np.isclose(baseline_result, streaming_result, atol=1e-2):
            raise RuntimeError("Optimized implementation changed the numerical result.")

        if _MEMORY_PROFILER_AVAILABLE:
            _, baseline_peak_mb = workflow.profile_memory(workflow.baseline_normalize_all)
            _, streaming_peak_mb = workflow.profile_memory(workflow.streaming_normalize_all)
            print(f"baseline peak memory delta: {baseline_peak_mb:.3f} MiB")
            print(f"streaming peak memory delta: {streaming_peak_mb:.3f} MiB")
        else:
            print(
                "memory_profiler not installed; skipping peak memory measurement. "
                "Install with 'pip install memory_profiler' to enable it."
            )


if __name__ == "__main__":
    ExperimentalMeasurementMemoryWorkflow.run()
