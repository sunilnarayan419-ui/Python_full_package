"""
12_Optimization.py

Production-oriented numerical optimization for dose-response curve fitting
and kinetic parameter estimation using scipy.optimize, with explicit
validation of bounds, initial parameters, and convergence diagnostics.
"""

from __future__ import annotations

import logging

import numpy as np
from scipy import optimize

logger = logging.getLogger(__name__)


class ScientificInputError(ValueError):
    """Raised when scientific input data is invalid."""


class NumericalConvergenceError(RuntimeError):
    """Raised when a numerical algorithm fails to converge."""


def load_dose_response_data() -> tuple[np.ndarray, np.ndarray]:
    """
    Return (dose_mg, response_fraction) measurements from a dose-response
    assay, response bounded in [0, 1] (e.g. fraction of maximal effect).
    """
    dose = np.array([0.01, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0])
    response = np.array([0.02, 0.05, 0.15, 0.38, 0.62, 0.83, 0.93, 0.97])
    return dose, response


def four_param_logistic(dose: np.ndarray, bottom: float, top: float, ec50: float, hill: float) -> np.ndarray:
    """Standard 4-parameter logistic (4PL) dose-response model."""
    return bottom + (top - bottom) / (1.0 + (ec50 / dose) ** hill)


def validate_fit_inputs(dose: np.ndarray, response: np.ndarray) -> None:
    if dose.shape != response.shape:
        raise ScientificInputError("dose and response must have matching shapes")
    if np.any(dose <= 0):
        raise ScientificInputError("dose values must be strictly positive (used in EC50 ratio)")
    if not np.isfinite(dose).all() or not np.isfinite(response).all():
        raise ScientificInputError("dose/response contain non-finite values")
    if dose.size < 4:
        raise ScientificInputError("Need at least 4 points to fit a 4-parameter model")


def fit_dose_response_local(
    dose: np.ndarray, response: np.ndarray
) -> optimize.OptimizeResult:
    """
    Fit the 4PL model via local least-squares optimization (Levenberg-
    Marquardt-style trust region via scipy.optimize.least_squares), starting
    from a data-informed initial guess and explicit physically meaningful
    bounds.

    Local optimization converges quickly but can settle in a poor local
    minimum if the initial guess is far from the true parameters -- see
    fit_dose_response_global below for a comparison on a harder case.
    """
    validate_fit_inputs(dose, response)

    def residuals(params: np.ndarray) -> np.ndarray:
        bottom, top, ec50, hill = params
        return four_param_logistic(dose, bottom, top, ec50, hill) - response

    initial_guess = np.array(
        [response.min(), response.max(), np.median(dose), 1.0]
    )
    bounds = (
        [0.0, 0.0, dose.min() * 0.01, 0.1],
        [1.0, 1.5, dose.max() * 100.0, 10.0],
    )

    result = optimize.least_squares(residuals, initial_guess, bounds=bounds)

    if not result.success:
        raise NumericalConvergenceError(
            f"Local dose-response fit failed: status={result.status}, message={result.message}"
        )
    logger.info(
        "Local fit converged: cost=%.6f, nfev=%d, status=%s",
        result.cost, result.nfev, result.status,
    )
    return result


def fit_dose_response_global(dose: np.ndarray, response: np.ndarray) -> optimize.OptimizeResult:
    """
    Fit the same 4PL model using a global optimizer (differential_evolution)
    over the same physically meaningful bounds, without requiring an initial
    guess. Global optimization explores the full bounded parameter space and
    is more robust to poor initial guesses, at higher computational cost.
    """
    validate_fit_inputs(dose, response)

    def sum_squared_error(params: np.ndarray) -> float:
        bottom, top, ec50, hill = params
        pred = four_param_logistic(dose, bottom, top, ec50, hill)
        return float(np.sum((pred - response) ** 2))

    bounds = [
        (0.0, 1.0),
        (0.0, 1.5),
        (dose.min() * 0.01, dose.max() * 100.0),
        (0.1, 10.0),
    ]

    result = optimize.differential_evolution(
        sum_squared_error, bounds, seed=42, tol=1e-8, maxiter=1000
    )

    if not result.success:
        raise NumericalConvergenceError(
            f"Global dose-response fit failed: message={result.message}"
        )
    logger.info("Global fit converged: fun=%.8f, nit=%d", result.fun, result.nit)
    return result


def estimate_ec50_from_result(result: optimize.OptimizeResult) -> float:
    """Extract EC50 (third parameter) from an optimize result, with a sanity check."""
    params = result.x
    if params.size != 4:
        raise ScientificInputError("Expected a 4-parameter result vector")
    ec50 = float(params[2])
    if not np.isfinite(ec50) or ec50 <= 0:
        raise NumericalConvergenceError(f"Fitted EC50 is not physically valid: {ec50}")
    return ec50


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    dose, response = load_dose_response_data()

    local_result = fit_dose_response_local(dose, response)
    local_ec50 = estimate_ec50_from_result(local_result)
    print(f"Local fit params [bottom, top, EC50, hill]: {np.round(local_result.x, 4)}")
    print(f"Local fit EC50: {local_ec50:.4f} mg")

    global_result = fit_dose_response_global(dose, response)
    global_ec50 = estimate_ec50_from_result(global_result)
    print(f"Global fit params [bottom, top, EC50, hill]: {np.round(global_result.x, 4)}")
    print(f"Global fit EC50: {global_ec50:.4f} mg")

    print(
        "Note: for this well-behaved, data-informed initial guess, local and "
        "global optimization should agree closely; global optimization is "
        "most valuable when the objective surface has multiple local minima."
    )


if __name__ == "__main__":
    main()
