"""
13_Integration.py

Production-oriented numerical integration using scipy.integrate for a
pharmacokinetic area-under-curve (AUC) calculation and a population growth
accumulation problem, with explicit tolerance and convergence handling.

Numerical integration (computing a definite integral of a known function or
sampled curve) is distinguished from ODE solving (finding a function that
satisfies a differential equation) -- see 18_ODE_Solvers.py for the latter.
"""

from __future__ import annotations

import logging

import numpy as np
from scipy import integrate

logger = logging.getLogger(__name__)


class ScientificInputError(ValueError):
    """Raised when scientific input data is invalid."""


class NumericalConvergenceError(RuntimeError):
    """Raised when a numerical algorithm fails to converge."""


def one_compartment_concentration(t: float, dose_mg: float, ka: float, ke: float, v_l: float) -> float:
    """
    Plasma concentration (mg/L) at time t (hours) for a one-compartment
    oral-dose pharmacokinetic model with first-order absorption (ka) and
    elimination (ke), volume of distribution v_l (liters).
    """
    if ka == ke:
        # Degenerate case of the closed-form solution; not handled here.
        raise ScientificInputError("ka must differ from ke for this closed-form model")
    return (dose_mg * ka) / (v_l * (ka - ke)) * (np.exp(-ke * t) - np.exp(-ka * t))


def compute_auc_quad(
    dose_mg: float, ka: float, ke: float, v_l: float, t_end_h: float
) -> tuple[float, float]:
    """
    Compute the area under the plasma concentration-time curve (AUC), a
    standard pharmacokinetic exposure metric, via adaptive quadrature
    (scipy.integrate.quad).

    Returns (auc_mg_h_per_L, estimated_absolute_error).
    """
    if dose_mg <= 0 or ka <= 0 or ke <= 0 or v_l <= 0:
        raise ScientificInputError("dose_mg, ka, ke, v_l must all be strictly positive")
    if t_end_h <= 0:
        raise ScientificInputError("t_end_h must be positive")

    def concentration(t: float) -> float:
        return one_compartment_concentration(t, dose_mg, ka, ke, v_l)

    auc, abs_error = integrate.quad(concentration, 0.0, t_end_h, epsabs=1e-6, epsrel=1e-6)

    relative_error = abs_error / auc if auc != 0 else np.inf
    if relative_error > 1e-3:
        logger.warning(
            "AUC quadrature relative error %.2e exceeds 1e-3 tolerance; "
            "result may be imprecise",
            relative_error,
        )

    return auc, abs_error


def compute_auc_to_infinity(dose_mg: float, ka: float, ke: float, v_l: float) -> tuple[float, float]:
    """
    Compute AUC(0-inf) by integrating to numerical infinity, letting quad's
    adaptive algorithm handle the improper integral (valid because the
    concentration decays exponentially to zero).
    """
    if dose_mg <= 0 or ka <= 0 or ke <= 0 or v_l <= 0:
        raise ScientificInputError("dose_mg, ka, ke, v_l must all be strictly positive")

    def concentration(t: float) -> float:
        return one_compartment_concentration(t, dose_mg, ka, ke, v_l)

    auc, abs_error = integrate.quad(concentration, 0.0, np.inf)
    return auc, abs_error


def logistic_growth_rate(t: float, r: float, k_capacity: float, n0: float) -> float:
    """
    Instantaneous growth rate dN/dt for logistic population growth, evaluated
    via the closed-form solution's derivative -- used here as the integrand
    for a cumulative-growth calculation distinct from directly solving the
    ODE (see 18_ODE_Solvers.py for solving the ODE itself).
    """
    n_t = (k_capacity * n0 * np.exp(r * t)) / (k_capacity + n0 * (np.exp(r * t) - 1.0))
    return r * n_t * (1.0 - n_t / k_capacity)


def cumulative_growth(r: float, k_capacity: float, n0: float, t_end: float) -> tuple[float, float]:
    """
    Integrate the instantaneous growth rate over [0, t_end] to obtain total
    population increase (should closely match N(t_end) - N(0) analytically;
    used here to illustrate quadrature applied to a nontrivial integrand).
    """
    if r <= 0 or k_capacity <= 0 or n0 <= 0:
        raise ScientificInputError("r, k_capacity, n0 must be strictly positive")
    if not (0 < n0 < k_capacity):
        raise ScientificInputError("n0 must be strictly between 0 and k_capacity")
    if t_end <= 0:
        raise ScientificInputError("t_end must be positive")

    def rate(t: float) -> float:
        return logistic_growth_rate(t, r, k_capacity, n0)

    increase, abs_error = integrate.quad(rate, 0.0, t_end)
    if abs_error > 1e-4 * max(abs(increase), 1.0):
        raise NumericalConvergenceError(
            f"Growth integral did not converge to sufficient precision: abs_error={abs_error:.2e}"
        )
    return increase, abs_error


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    dose_mg, ka, ke, v_l = 500.0, 1.2, 0.15, 40.0

    auc_24h, err_24h = compute_auc_quad(dose_mg, ka, ke, v_l, t_end_h=24.0)
    print(f"AUC(0-24h) = {auc_24h:.4f} mg*h/L (abs err ~{err_24h:.2e})")

    auc_inf, err_inf = compute_auc_to_infinity(dose_mg, ka, ke, v_l)
    print(f"AUC(0-inf) = {auc_inf:.4f} mg*h/L (abs err ~{err_inf:.2e})")

    increase, err = cumulative_growth(r=0.3, k_capacity=1000.0, n0=10.0, t_end=20.0)
    print(f"Cumulative population increase over 20 time units: {increase:.3f} (abs err ~{err:.2e})")


if __name__ == "__main__":
    main()
