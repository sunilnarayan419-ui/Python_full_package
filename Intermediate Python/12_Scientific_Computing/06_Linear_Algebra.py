"""
06_Linear_Algebra.py

Production-oriented numerical linear algebra for a compartmental modeling and
molecular-descriptor regression workflow, using NumPy's linalg module and
stable solve/least-squares primitives rather than explicit matrix inversion.
"""

from __future__ import annotations

import logging

import numpy as np

logger = logging.getLogger(__name__)


class ScientificInputError(ValueError):
    """Raised when scientific input data is invalid."""


class NumericalConvergenceError(RuntimeError):
    """Raised when a numerical algorithm fails to converge or is ill-posed."""


def solve_steady_state_compartments(
    rate_matrix: np.ndarray, input_vector: np.ndarray
) -> np.ndarray:
    """
    Solve for the steady-state compartment concentrations x in the linear
    system A x = b, where A encodes inter-compartment rate constants and b
    encodes constant infusion/input rates.

    Uses np.linalg.solve rather than computing A^-1 explicitly: solve() uses
    an LU factorization internally and is both faster and more numerically
    stable than forming the inverse.
    """
    if rate_matrix.ndim != 2 or rate_matrix.shape[0] != rate_matrix.shape[1]:
        raise ScientificInputError("rate_matrix must be square (n_compartments x n_compartments)")
    if input_vector.shape != (rate_matrix.shape[0],):
        raise ScientificInputError("input_vector shape must match rate_matrix dimension")
    if not np.isfinite(rate_matrix).all() or not np.isfinite(input_vector).all():
        raise ScientificInputError("rate_matrix/input_vector contain non-finite values")

    condition_number = np.linalg.cond(rate_matrix)
    if condition_number > 1e12:
        raise NumericalConvergenceError(
            f"rate_matrix is ill-conditioned (cond={condition_number:.3e}); "
            "steady-state solution would be numerically unreliable"
        )

    try:
        solution = np.linalg.solve(rate_matrix, input_vector)
    except np.linalg.LinAlgError as exc:
        raise NumericalConvergenceError(f"Linear system is singular: {exc}") from exc

    return solution


def fit_molecular_descriptor_model(
    descriptor_matrix: np.ndarray, activity: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """
    Fit a linear QSAR-style model (activity ~ descriptors) via ordinary
    least squares using np.linalg.lstsq, which is numerically robust to
    rank-deficient or overdetermined descriptor matrices (unlike solving the
    normal equations directly).

    Returns (coefficients, residuals_sum_of_squares).
    """
    n_samples, n_features = descriptor_matrix.shape
    if activity.shape != (n_samples,):
        raise ScientificInputError("activity vector must have one value per sample row")
    if n_samples < n_features:
        logger.warning(
            "Underdetermined system: n_samples=%d < n_features=%d; "
            "lstsq will return a minimum-norm solution",
            n_samples,
            n_features,
        )

    # Add an intercept column (bias term) explicitly.
    design = np.column_stack([np.ones(n_samples), descriptor_matrix])

    coefficients, residuals, rank, singular_values = np.linalg.lstsq(
        design, activity, rcond=None
    )

    if rank < design.shape[1]:
        logger.warning(
            "Design matrix is rank-deficient (rank=%d of %d); coefficients "
            "may not be unique",
            rank,
            design.shape[1],
        )

    return coefficients, residuals


def compute_reaction_network_modes(stoichiometry_matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute eigenvalues/eigenvectors of a linear reaction-network Jacobian to
    characterize relaxation modes toward equilibrium.

    Eigen-decomposition is appropriate here (rather than SVD) because the
    matrix represents a square linear dynamical system A in dx/dt = A x, and
    the eigenvalues directly give the decay/growth rates of each mode.
    """
    if stoichiometry_matrix.ndim != 2 or stoichiometry_matrix.shape[0] != stoichiometry_matrix.shape[1]:
        raise ScientificInputError("stoichiometry_matrix must be square")

    eigenvalues, eigenvectors = np.linalg.eig(stoichiometry_matrix)
    return eigenvalues, eigenvectors


def reduce_expression_dimensionality(expression_matrix: np.ndarray, n_components: int) -> np.ndarray:
    """
    Reduce a (n_samples, n_genes) expression matrix to `n_components` using
    the SVD of the mean-centered data (a standard PCA-via-SVD pattern),
    appropriate because SVD is numerically stable and avoids forming the
    covariance matrix explicitly.
    """
    n_samples, n_genes = expression_matrix.shape
    if n_components < 1 or n_components > min(n_samples, n_genes):
        raise ScientificInputError("n_components out of valid range for SVD")

    centered = expression_matrix - expression_matrix.mean(axis=0)
    u, singular_values, vt = np.linalg.svd(centered, full_matrices=False)

    scores = u[:, :n_components] * singular_values[:n_components]
    return scores


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    # Two-compartment PK model: gut -> plasma, with elimination from plasma.
    rate_matrix = np.array(
        [
            [1.5, 0.0],   # gut absorption + no return
            [-1.5, 0.8],  # plasma gains from gut, loses via elimination
        ]
    )
    input_vector = np.array([2.0, 0.0])  # constant infusion into gut compartment
    steady_state = solve_steady_state_compartments(rate_matrix, input_vector)
    print("Steady-state compartment amounts (mg):", steady_state)

    rng = np.random.default_rng(seed=3)
    descriptors = rng.normal(size=(20, 4))  # e.g. logP, MW, TPSA, HBD
    true_coeffs = np.array([0.5, -1.2, 0.3, 2.0])
    activity = descriptors @ true_coeffs + rng.normal(scale=0.1, size=20)
    coeffs, residuals = fit_molecular_descriptor_model(descriptors, activity)
    print("Fitted QSAR coefficients (intercept + 4 descriptors):", np.round(coeffs, 4))

    reaction_jacobian = np.array([[-0.5, 0.2], [0.3, -0.7]])
    eigvals, eigvecs = compute_reaction_network_modes(reaction_jacobian)
    print("Reaction-network eigenvalues (relaxation rates):", eigvals)

    expr = rng.normal(size=(15, 50))
    scores = reduce_expression_dimensionality(expr, n_components=2)
    print("PCA-via-SVD scores shape:", scores.shape)


if __name__ == "__main__":
    main()
