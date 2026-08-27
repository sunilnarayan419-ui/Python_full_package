"""
07_Random_Module.py

Production-oriented, reproducible random number generation for scientific
simulation: measurement noise injection, Monte Carlo dose simulation, and
bootstrap resampling, all using np.random.Generator / default_rng rather than
legacy global random state.
"""

from __future__ import annotations

import logging

import numpy as np

logger = logging.getLogger(__name__)


class ScientificInputError(ValueError):
    """Raised when scientific input data is invalid."""


def make_rng(seed: int | None = None) -> np.random.Generator:
    """
    Construct an explicit RNG instance. Passing an explicit seed gives
    reproducible results across runs; passing None draws entropy from the OS
    for genuinely non-deterministic use (e.g. production simulation ensembles
    where independent runs are desired).
    """
    return np.random.default_rng(seed)


def simulate_measurement_noise(
    true_values: np.ndarray, relative_noise_sd: float, rng: np.random.Generator
) -> np.ndarray:
    """
    Add proportional (heteroscedastic) Gaussian noise to true measurement
    values, simulating realistic instrument noise that scales with signal
    magnitude. The RNG is injected explicitly rather than using global state,
    so callers control reproducibility.
    """
    if relative_noise_sd < 0:
        raise ScientificInputError("relative_noise_sd must be non-negative")
    if not np.isfinite(true_values).all():
        raise ScientificInputError("true_values contains non-finite entries")

    noise_sd = np.abs(true_values) * relative_noise_sd
    noise = rng.normal(loc=0.0, scale=noise_sd)
    return true_values + noise


def monte_carlo_dose_response(
    ec50: float,
    hill_slope: float,
    dose_mg: np.ndarray,
    n_trials: int,
    param_cv: float,
    rng: np.random.Generator,
) -> np.ndarray:
    """
    Run a Monte Carlo simulation of a Hill-equation dose-response curve where
    EC50 and hill_slope vary trial-to-trial according to a coefficient of
    variation (param_cv), simulating inter-individual pharmacological
    variability.

    Returns an array of shape (n_trials, dose_mg.size) of simulated
    responses in [0, 1].
    """
    if ec50 <= 0 or hill_slope <= 0:
        raise ScientificInputError("ec50 and hill_slope must be positive")
    if n_trials <= 0:
        raise ScientificInputError("n_trials must be positive")
    if param_cv < 0:
        raise ScientificInputError("param_cv must be non-negative")

    # Independent streams per parameter via distinct generator calls on the
    # same injected Generator (deterministic given the same rng state).
    ec50_samples = rng.normal(loc=ec50, scale=ec50 * param_cv, size=n_trials)
    ec50_samples = np.clip(ec50_samples, a_min=1e-6, a_max=None)

    slope_samples = rng.normal(loc=hill_slope, scale=hill_slope * param_cv, size=n_trials)
    slope_samples = np.clip(slope_samples, a_min=1e-3, a_max=None)

    # Broadcast dose (1, n_doses) against per-trial params (n_trials, 1).
    dose = dose_mg[np.newaxis, :]
    ec50_col = ec50_samples[:, np.newaxis]
    slope_col = slope_samples[:, np.newaxis]

    response = 1.0 / (1.0 + (ec50_col / dose) ** slope_col)
    return response


def bootstrap_confidence_interval(
    sample: np.ndarray, statistic: str, n_resamples: int, rng: np.random.Generator, ci: float = 0.95
) -> tuple[float, float, float]:
    """
    Compute a percentile bootstrap confidence interval for the mean or median
    of a small experimental sample (e.g. assay replicate measurements).

    Returns (point_estimate, ci_low, ci_high).
    """
    if sample.ndim != 1 or sample.size < 2:
        raise ScientificInputError("sample must be a 1D array with at least 2 observations")
    if statistic not in {"mean", "median"}:
        raise ScientificInputError("statistic must be 'mean' or 'median'")
    if not (0 < ci < 1):
        raise ScientificInputError("ci must be between 0 and 1")

    stat_fn = np.mean if statistic == "mean" else np.median
    n = sample.size

    # Vectorized resampling: draw all bootstrap indices at once.
    resample_idx = rng.integers(0, n, size=(n_resamples, n))
    resamples = sample[resample_idx]
    boot_stats = stat_fn(resamples, axis=1)

    alpha = 1.0 - ci
    lo, hi = np.percentile(boot_stats, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    point_estimate = float(stat_fn(sample))
    return point_estimate, float(lo), float(hi)


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    rng = make_rng(seed=2024)  # fixed seed -> reproducible run

    true_values = np.array([10.0, 25.0, 50.0, 100.0])
    noisy = simulate_measurement_noise(true_values, relative_noise_sd=0.05, rng=rng)
    print("Noisy measurements:", np.round(noisy, 3))

    doses = np.array([0.1, 1.0, 10.0, 100.0, 1000.0])
    responses = monte_carlo_dose_response(
        ec50=10.0, hill_slope=1.5, dose_mg=doses, n_trials=1000, param_cv=0.15, rng=rng
    )
    logger.info("Monte Carlo response ensemble shape=%s", responses.shape)
    print("Mean response per dose:", np.round(responses.mean(axis=0), 4))
    print("5th/95th pct response at dose=10mg:", np.percentile(responses[:, 2], [5, 95]))

    replicate_sample = np.array([98.2, 101.4, 99.7, 100.9, 97.8, 102.1])
    point, lo, hi = bootstrap_confidence_interval(
        replicate_sample, statistic="mean", n_resamples=5000, rng=rng
    )
    print(f"Bootstrap mean estimate: {point:.3f} (95% CI: [{lo:.3f}, {hi:.3f}])")


if __name__ == "__main__":
    main()
