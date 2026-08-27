"""
11_SciPy_Overview.py

Production-oriented, cohesive scientific workflow demonstrating how several
SciPy modules combine in a realistic pipeline: given noisy, sparsely sampled
enzyme-kinetics measurements, we (1) interpolate/smooth with
scipy.interpolate, (2) fit a Michaelis-Menten model with scipy.optimize,
(3) integrate the fitted rate curve with scipy.integrate for cumulative
product formation, and (4) summarize residual statistics with scipy.stats.

Each module is used where it provides functionality NumPy alone does not.
"""

from __future__ import annotations

import logging

import numpy as np
from scipy import integrate, interpolate, optimize, stats

logger = logging.getLogger(__name__)


class ScientificInputError(ValueError):
    """Raised when scientific input data is invalid."""


class NumericalConvergenceError(RuntimeError):
    """Raised when a numerical algorithm fails to converge."""


def load_kinetics_measurements() -> tuple[np.ndarray, np.ndarray]:
    """
    Return sparse (substrate_concentration_mM, reaction_velocity_uM_per_min)
    measurements from an enzyme kinetics assay.
    """
    substrate = np.array([0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0])
    velocity = np.array([2.1, 3.6, 5.8, 8.2, 10.5, 12.1, 13.0])
    return substrate, velocity


def smooth_measurement_curve(
    substrate: np.ndarray, velocity: np.ndarray, n_eval_points: int = 200
) -> tuple[np.ndarray, np.ndarray]:
    """
    scipy.interpolate: build a monotone-respecting PCHIP interpolant through
    sparse measurements for visualization/smoothing purposes (NumPy has no
    interpolation primitives beyond simple linear np.interp).
    """
    if substrate.shape != velocity.shape:
        raise ScientificInputError("substrate and velocity must have matching shapes")
    if not np.all(np.diff(substrate) > 0):
        raise ScientificInputError("substrate values must be strictly increasing")

    pchip = interpolate.PchipInterpolator(substrate, velocity, extrapolate=False)
    eval_points = np.linspace(substrate.min(), substrate.max(), n_eval_points)
    return eval_points, pchip(eval_points)


def michaelis_menten(substrate: np.ndarray, vmax: float, km: float) -> np.ndarray:
    """Standard Michaelis-Menten rate law."""
    return (vmax * substrate) / (km + substrate)


def fit_kinetics_model(substrate: np.ndarray, velocity: np.ndarray) -> tuple[float, float]:
    """
    scipy.optimize: fit Vmax and Km via nonlinear least squares (NumPy alone
    provides only linear least squares via lstsq, insufficient for this
    nonlinear model).
    """
    def residuals(params: np.ndarray) -> np.ndarray:
        vmax, km = params
        return michaelis_menten(substrate, vmax, km) - velocity

    initial_guess = np.array([velocity.max() * 1.2, substrate[len(substrate) // 2]])
    bounds = ([0.0, 1e-6], [np.inf, np.inf])

    result = optimize.least_squares(residuals, initial_guess, bounds=bounds)
    if not result.success:
        raise NumericalConvergenceError(f"Kinetics fit failed to converge: {result.message}")

    vmax_fit, km_fit = result.x
    return float(vmax_fit), float(km_fit)


def cumulative_product_formation(vmax: float, km: float, t_end_min: float) -> tuple[float, float]:
    """
    scipy.integrate: compute cumulative product formation over time by
    numerically integrating the (simplified) rate law with respect to time,
    assuming substrate is held at a saturating reference concentration for
    this illustrative cumulative-exposure calculation.

    Returns (integral_value, estimated_absolute_error).
    """
    reference_substrate = 10.0  # mM, illustrative fixed condition

    def rate_at_time(t: float) -> float:
        # Rate law here is time-independent (steady substrate assumption);
        # quad still requires a callable of t.
        return michaelis_menten(np.array([reference_substrate]), vmax, km)[0]

    value, abs_error = integrate.quad(rate_at_time, 0.0, t_end_min)
    return value, abs_error


def evaluate_fit_quality(substrate: np.ndarray, velocity: np.ndarray, vmax: float, km: float) -> dict[str, float]:
    """
    scipy.stats: summarize residual normality via a Shapiro-Wilk test, which
    NumPy does not provide, to sanity-check the least-squares fit
    assumptions on this small sample.
    """
    predicted = michaelis_menten(substrate, vmax, km)
    residuals = velocity - predicted

    if residuals.size < 3:
        raise ScientificInputError("Need at least 3 residuals for a normality test")

    shapiro_result = stats.shapiro(residuals)
    return {
        "rmse": float(np.sqrt(np.mean(residuals**2))),
        "shapiro_statistic": float(shapiro_result.statistic),
        "shapiro_pvalue": float(shapiro_result.pvalue),
    }


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    substrate, velocity = load_kinetics_measurements()

    eval_points, smoothed = smooth_measurement_curve(substrate, velocity)
    logger.info("Interpolated curve over %d evaluation points", eval_points.size)

    vmax, km = fit_kinetics_model(substrate, velocity)
    print(f"Fitted Vmax={vmax:.3f} uM/min, Km={km:.3f} mM")

    integral_value, abs_error = cumulative_product_formation(vmax, km, t_end_min=30.0)
    print(f"Cumulative product formation over 30 min: {integral_value:.3f} uM (abs err ~{abs_error:.2e})")

    fit_quality = evaluate_fit_quality(substrate, velocity, vmax, km)
    print("Fit quality:", {k: round(v, 4) for k, v in fit_quality.items()})


if __name__ == "__main__":
    main()
