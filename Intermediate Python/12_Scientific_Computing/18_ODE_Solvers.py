"""
18_ODE_Solvers.py

Production-oriented ordinary differential equation solving using
scipy.integrate.solve_ivp for a two-compartment pharmacokinetic model
(non-stiff, RK45) and a stiff enzyme-reaction kinetics system (BDF), with
explicit solver-success validation.
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


def two_compartment_pk_rhs(t: float, y: np.ndarray, ka: float, ke: float, k12: float, k21: float) -> np.ndarray:
    """
    Right-hand side for a two-compartment oral PK model:
    y[0] = gut amount (mg), y[1] = central (plasma) amount (mg),
    y[2] = peripheral (tissue) amount (mg).
    """
    gut, central, peripheral = y
    d_gut = -ka * gut
    d_central = ka * gut - ke * central - k12 * central + k21 * peripheral
    d_peripheral = k12 * central - k21 * peripheral
    return np.array([d_gut, d_central, d_peripheral])


def simulate_two_compartment_pk(
    dose_mg: float, ka: float, ke: float, k12: float, k21: float, t_end_h: float, n_eval: int
) -> integrate.OdeResult:
    """
    Simulate the two-compartment PK model with solve_ivp using RK45
    (the default explicit Runge-Kutta method), appropriate here because the
    rate constants are of comparable magnitude and the system is non-stiff.
    """
    if dose_mg <= 0:
        raise ScientificInputError("dose_mg must be positive")
    if any(rate <= 0 for rate in (ka, ke, k12, k21)):
        raise ScientificInputError("All rate constants must be strictly positive")
    if t_end_h <= 0 or n_eval < 2:
        raise ScientificInputError("t_end_h must be positive and n_eval >= 2")

    y0 = np.array([dose_mg, 0.0, 0.0])
    if not np.isfinite(y0).all():
        raise ScientificInputError("Initial state contains non-finite values")

    t_eval = np.linspace(0.0, t_end_h, n_eval)

    solution = integrate.solve_ivp(
        two_compartment_pk_rhs,
        t_span=(0.0, t_end_h),
        y0=y0,
        method="RK45",
        t_eval=t_eval,
        args=(ka, ke, k12, k21),
        rtol=1e-6,
        atol=1e-9,
    )

    validate_solution(solution, "two-compartment PK (RK45)")
    return solution


def stiff_enzyme_kinetics_rhs(t: float, y: np.ndarray, k1: float, k_minus1: float, k2: float) -> np.ndarray:
    """
    Right-hand side for the Michaelis-Menten mechanistic ODE system
    (substrate S, enzyme E, complex ES, product P), which becomes stiff when
    k1/k_minus1 (fast binding equilibrium) are much larger than k2 (slow
    catalysis) -- a common scenario in real enzyme kinetics.
    """
    s, e, es, p = y
    d_s = -k1 * s * e + k_minus1 * es
    d_e = -k1 * s * e + k_minus1 * es + k2 * es
    d_es = k1 * s * e - k_minus1 * es - k2 * es
    d_p = k2 * es
    return np.array([d_s, d_e, d_es, d_p])


def simulate_stiff_enzyme_kinetics(
    s0: float, e0: float, k1: float, k_minus1: float, k2: float, t_end_s: float, n_eval: int
) -> integrate.OdeResult:
    """
    Simulate the stiff enzyme-kinetics system using the BDF (Backward
    Differentiation Formula) implicit method, appropriate because the fast
    binding/unbinding rates (k1, k_minus1) relative to the slow catalytic
    step (k2) make this system numerically stiff -- RK45 would require an
    impractically small step size to remain stable, whereas BDF (and Radau)
    handle stiff systems efficiently via implicit stepping.
    """
    if s0 <= 0 or e0 <= 0:
        raise ScientificInputError("s0 and e0 must be strictly positive")
    if any(rate <= 0 for rate in (k1, k_minus1, k2)):
        raise ScientificInputError("All rate constants must be strictly positive")
    if t_end_s <= 0 or n_eval < 2:
        raise ScientificInputError("t_end_s must be positive and n_eval >= 2")

    y0 = np.array([s0, e0, 0.0, 0.0])
    t_eval = np.linspace(0.0, t_end_s, n_eval)

    solution = integrate.solve_ivp(
        stiff_enzyme_kinetics_rhs,
        t_span=(0.0, t_end_s),
        y0=y0,
        method="BDF",
        t_eval=t_eval,
        args=(k1, k_minus1, k2),
        rtol=1e-8,
        atol=1e-10,
    )

    validate_solution(solution, "stiff enzyme kinetics (BDF)")
    return solution


def validate_solution(solution: integrate.OdeResult, description: str) -> None:
    """
    Inspect solver success and solution finiteness rather than blindly
    trusting solve_ivp's output -- a silently failed or partially integrated
    solution is a common source of downstream scientific errors.
    """
    if not solution.success:
        raise NumericalConvergenceError(
            f"{description} ODE solve failed: status={solution.status}, message={solution.message}"
        )
    if not np.isfinite(solution.y).all():
        raise NumericalConvergenceError(f"{description} solution contains non-finite values")
    logger.info(
        "%s solved successfully: nfev=%d, njev=%d, nsteps~%d",
        description, solution.nfev, getattr(solution, "njev", 0), solution.t.size,
    )


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    pk_solution = simulate_two_compartment_pk(
        dose_mg=500.0, ka=1.2, ke=0.2, k12=0.3, k21=0.15, t_end_h=24.0, n_eval=25
    )
    print("Two-compartment PK plasma amounts (mg) at evaluation times:")
    print(np.round(pk_solution.y[1], 3))
    print(f"Peak plasma amount: {pk_solution.y[1].max():.3f} mg at t={pk_solution.t[np.argmax(pk_solution.y[1])]:.2f}h")

    kinetics_solution = simulate_stiff_enzyme_kinetics(
        s0=100.0, e0=5.0, k1=50.0, k_minus1=20.0, k2=1.0, t_end_s=10.0, n_eval=25
    )
    print("\nStiff enzyme kinetics product formation (P) over time:")
    print(np.round(kinetics_solution.y[3], 3))
    final_conversion = kinetics_solution.y[3, -1] / 100.0
    print(f"Final substrate-to-product conversion: {final_conversion * 100:.1f}%")

    print(
        "\nNote: RK45 was appropriate for the non-stiff PK system; BDF was "
        "required for the stiff kinetics system. Neither method is "
        "universally best -- method selection depends on system stiffness."
    )


if __name__ == "__main__":
    main()
