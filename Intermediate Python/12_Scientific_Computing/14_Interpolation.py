"""
14_Interpolation.py

Production-oriented interpolation of sparse scientific measurements: plant
growth trajectories sampled on irregular days, using scipy.interpolate with
explicit handling of monotonicity and extrapolation risk.
"""

from __future__ import annotations

import logging

import numpy as np
from scipy import interpolate

logger = logging.getLogger(__name__)


class ScientificInputError(ValueError):
    """Raised when scientific input data is invalid."""


class ExtrapolationError(ValueError):
    """Raised when a query point falls outside the observed measurement domain."""


def load_growth_measurements() -> tuple[np.ndarray, np.ndarray]:
    """
    Return sparse (day, stem_height_cm) measurements collected on irregular
    days -- a realistic pattern for manual/destructive plant phenotyping
    where daily measurement is impractical.
    """
    day = np.array([0, 3, 7, 14, 21, 30])
    height_cm = np.array([2.0, 4.5, 9.8, 18.2, 25.1, 29.5])
    return day, height_cm


def validate_measurement_grid(x: np.ndarray, y: np.ndarray) -> None:
    if x.shape != y.shape:
        raise ScientificInputError("x and y must have matching shapes")
    if x.size < 2:
        raise ScientificInputError("Need at least 2 points to interpolate")
    if not np.all(np.diff(x) > 0):
        raise ScientificInputError("x values must be strictly increasing for these interpolators")
    if not np.isfinite(x).all() or not np.isfinite(y).all():
        raise ScientificInputError("x/y contain non-finite values")


def build_pchip_interpolator(day: np.ndarray, height_cm: np.ndarray) -> interpolate.PchipInterpolator:
    """
    Build a PCHIP (Piecewise Cubic Hermite Interpolating Polynomial)
    interpolator, chosen because plant growth is expected to be monotonic
    (non-decreasing) over time and PCHIP preserves monotonicity of the input
    data, unlike a natural cubic spline which can overshoot and introduce
    spurious non-monotonic wiggles between sparse points.

    extrapolate=False makes out-of-domain queries return NaN rather than
    silently extrapolating.
    """
    validate_measurement_grid(day, height_cm)
    if not np.all(np.diff(height_cm) >= 0):
        logger.warning(
            "height_cm is not monotonically non-decreasing; PCHIP will still "
            "fit but the monotonicity guarantee assumption does not hold for "
            "this dataset"
        )
    return interpolate.PchipInterpolator(day, height_cm, extrapolate=False)


def build_cubic_spline_interpolator(day: np.ndarray, height_cm: np.ndarray) -> interpolate.CubicSpline:
    """
    Build a natural cubic spline interpolator for comparison. Cubic splines
    minimize curvature and are appropriate for smooth physical quantities
    without a strict monotonicity requirement, but can overshoot between
    sparse points for monotonic biological data -- included here to
    illustrate the tradeoff against PCHIP, not as the primary recommendation.
    """
    validate_measurement_grid(day, height_cm)
    return interpolate.CubicSpline(day, height_cm, bc_type="natural", extrapolate=False)


def evaluate_within_domain(
    interpolator: interpolate.PchipInterpolator | interpolate.CubicSpline,
    query_days: np.ndarray,
    domain: tuple[float, float],
) -> np.ndarray:
    """
    Evaluate an interpolator at query points, explicitly rejecting queries
    outside the observed domain rather than silently extrapolating (a common
    source of scientifically invalid results).
    """
    lo, hi = domain
    out_of_domain = (query_days < lo) | (query_days > hi)
    if np.any(out_of_domain):
        bad_points = query_days[out_of_domain]
        raise ExtrapolationError(
            f"Query points outside observed domain [{lo}, {hi}]: {bad_points.tolist()}. "
            "Extrapolation risk: biological growth curves are not reliably "
            "extrapolable beyond the measured range."
        )
    return interpolator(query_days)


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    day, height_cm = load_growth_measurements()
    domain = (float(day.min()), float(day.max()))

    pchip = build_pchip_interpolator(day, height_cm)
    spline = build_cubic_spline_interpolator(day, height_cm)

    query_days = np.linspace(day.min(), day.max(), 15)
    pchip_values = evaluate_within_domain(pchip, query_days, domain)
    spline_values = evaluate_within_domain(spline, query_days, domain)

    print("Day  | PCHIP (cm) | CubicSpline (cm)")
    for d, p, s in zip(query_days, pchip_values, spline_values):
        print(f"{d:5.1f} | {p:10.3f} | {s:16.3f}")

    print("\nPCHIP monotonic (non-decreasing):", np.all(np.diff(pchip_values) >= -1e-9))
    print("CubicSpline monotonic (non-decreasing):", np.all(np.diff(spline_values) >= -1e-9))

    try:
        evaluate_within_domain(pchip, np.array([45.0]), domain)
    except ExtrapolationError as exc:
        print(f"\nExpected extrapolation rejection: {exc}")


if __name__ == "__main__":
    main()
