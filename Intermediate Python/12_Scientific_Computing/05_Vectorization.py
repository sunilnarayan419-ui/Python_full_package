"""
05_Vectorization.py

Production-oriented vectorization for biological signal thresholding and
feature transformation, contrasted against an explicit Python-loop
implementation kept only for illustration/testing purposes.
"""

from __future__ import annotations

import logging
import time

import numpy as np

logger = logging.getLogger(__name__)


class ScientificInputError(ValueError):
    """Raised when scientific input data is invalid."""


def load_fluorescence_trace(n_samples: int = 200_000) -> np.ndarray:
    """
    Return a synthetic single-cell fluorescence intensity trace (a.u.), with
    a slow baseline drift plus noise plus sparse spike events -- a common
    shape for calcium-imaging-style signals.
    """
    rng = np.random.default_rng(seed=11)
    t = np.arange(n_samples, dtype=np.float64)
    baseline = 100.0 + 5.0 * np.sin(t / 5000.0)
    noise = rng.normal(scale=2.0, size=n_samples)
    spikes = np.zeros(n_samples)
    spike_idx = rng.choice(n_samples, size=n_samples // 500, replace=False)
    spikes[spike_idx] = rng.uniform(20.0, 60.0, size=spike_idx.size)
    return baseline + noise + spikes


def threshold_trace_loop(trace: np.ndarray, threshold: float) -> np.ndarray:
    """
    Reference (non-production) Python-loop implementation of event detection
    by simple thresholding. Kept ONLY to demonstrate the vectorization
    improvement below -- do not use this in production code paths.
    """
    n = trace.shape[0]
    out = np.empty(n, dtype=bool)
    for i in range(n):
        out[i] = trace[i] > threshold
    return out


def threshold_trace_vectorized(trace: np.ndarray, threshold: float) -> np.ndarray:
    """
    Production implementation: vectorized elementwise comparison.
    Equivalent result to the loop version, without per-element Python
    interpreter overhead.
    """
    if trace.ndim != 1:
        raise ScientificInputError(f"Expected 1D trace; got ndim={trace.ndim}")
    return trace > threshold


def normalize_trace(trace: np.ndarray) -> np.ndarray:
    """
    Min-max normalize a signal trace to [0, 1] using vectorized arithmetic.
    """
    if trace.ndim != 1:
        raise ScientificInputError(f"Expected 1D trace; got ndim={trace.ndim}")

    lo, hi = trace.min(), trace.max()
    if hi <= lo:
        raise ScientificInputError("Trace has zero dynamic range; cannot normalize")
    return (trace - lo) / (hi - lo)


def convert_intensity_to_delta_f_over_f(trace: np.ndarray, baseline_window: int = 5000) -> np.ndarray:
    """
    Convert raw fluorescence intensity to dF/F0, a standard calcium-imaging
    feature transformation, using vectorized operations against a scalar
    baseline computed from an initial window.
    """
    if trace.ndim != 1:
        raise ScientificInputError(f"Expected 1D trace; got ndim={trace.ndim}")
    if baseline_window <= 0 or baseline_window > trace.shape[0]:
        raise ScientificInputError("Invalid baseline_window")

    f0 = trace[:baseline_window].mean()
    if f0 == 0:
        raise ScientificInputError("Baseline F0 is zero; cannot compute dF/F0")
    return (trace - f0) / f0


def benchmark_loop_vs_vectorized(trace: np.ndarray, threshold: float, n_bench_samples: int = 20_000) -> tuple[float, float]:
    """
    Benchmark the loop-based approach against the vectorized approach on a
    reduced sample count (the loop version does not scale to the full trace
    in reasonable time). Returns (loop_seconds, vectorized_seconds).

    This does not claim vectorization is universally faster for every
    operation -- for genuinely elementwise numeric work like thresholding it
    typically is, due to avoiding per-element Python bytecode dispatch.
    """
    small_trace = trace[:n_bench_samples]

    t0 = time.perf_counter()
    threshold_trace_loop(small_trace, threshold)
    loop_time = time.perf_counter() - t0

    t0 = time.perf_counter()
    threshold_trace_vectorized(small_trace, threshold)
    vec_time = time.perf_counter() - t0

    return loop_time, vec_time


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    trace = load_fluorescence_trace()
    logger.info("Loaded fluorescence trace: n_samples=%d", trace.size)

    events = threshold_trace_vectorized(trace, threshold=115.0)
    print(f"Detected {events.sum()} above-threshold samples out of {trace.size}")

    normalized = normalize_trace(trace)
    print("Normalized trace range:", normalized.min(), normalized.max())

    dff = convert_intensity_to_delta_f_over_f(trace)
    print("dF/F0 range: [%.3f, %.3f]" % (dff.min(), dff.max()))

    loop_time, vec_time = benchmark_loop_vs_vectorized(trace, threshold=115.0)
    print(f"Loop threshold time:       {loop_time * 1e3:.3f} ms (small subset only)")
    print(f"Vectorized threshold time: {vec_time * 1e3:.3f} ms (small subset only)")
    if vec_time > 0:
        print(f"Speedup on this subset: ~{loop_time / vec_time:.1f}x")


if __name__ == "__main__":
    main()
