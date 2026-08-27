"""
04_Broadcasting.py

Production-oriented NumPy broadcasting for instrument calibration and
per-feature normalization of a biomedical assay measurement matrix
(rows = samples, columns = analytes/features).
"""

from __future__ import annotations

import logging

import numpy as np

logger = logging.getLogger(__name__)


class ScientificInputError(ValueError):
    """Raised when scientific input data is invalid."""


def load_assay_matrix() -> np.ndarray:
    """Return a (n_samples, n_analytes) raw absorbance matrix."""
    rng = np.random.default_rng(seed=7)
    return rng.normal(loc=1.0, scale=0.15, size=(12, 4))


def validate_broadcast_shapes(matrix: np.ndarray, vector: np.ndarray) -> None:
    """
    Validate that `vector` can legally broadcast against the last axis of
    `matrix`. This makes shape-compatibility explicit rather than relying on
    NumPy to raise an opaque error deep inside a computation.
    """
    if matrix.ndim != 2:
        raise ScientificInputError(f"Expected 2D matrix; got ndim={matrix.ndim}")
    if vector.ndim != 1 or vector.shape[0] != matrix.shape[-1]:
        raise ScientificInputError(
            f"Calibration vector shape {vector.shape} is not broadcast-"
            f"compatible with matrix last axis {matrix.shape[-1]}"
        )


def apply_scalar_offset(matrix: np.ndarray, background: float) -> np.ndarray:
    """
    Scalar broadcasting: subtract a single instrument background/blank
    reading from every measurement in the matrix.
    """
    return matrix - background


def apply_per_analyte_calibration(
    matrix: np.ndarray, gain: np.ndarray, offset: np.ndarray
) -> np.ndarray:
    """
    Vector-to-matrix broadcasting: apply a per-analyte (per-column) linear
    calibration `y = gain * x + offset` without looping over rows.

    `gain` and `offset` have shape (n_analytes,); NumPy broadcasts them
    against every row of `matrix` (n_samples, n_analytes) automatically
    because their trailing dimension matches.
    """
    validate_broadcast_shapes(matrix, gain)
    validate_broadcast_shapes(matrix, offset)
    return matrix * gain + offset


def z_score_normalize(matrix: np.ndarray) -> np.ndarray:
    """
    Per-feature (per-column) z-score normalization using broadcasting of
    column means and column standard deviations (each shape (n_analytes,))
    against the full (n_samples, n_analytes) matrix.
    """
    if matrix.ndim != 2:
        raise ScientificInputError(f"Expected 2D matrix; got ndim={matrix.ndim}")

    col_mean = matrix.mean(axis=0)
    col_std = matrix.std(axis=0)
    if np.any(col_std == 0):
        raise ScientificInputError("Zero-variance analyte column cannot be z-normalized")

    return (matrix - col_mean) / col_std


def convert_units_absorbance_to_concentration(
    matrix: np.ndarray, molar_extinction_coeffs: np.ndarray, path_length_cm: float
) -> np.ndarray:
    """
    Apply the Beer-Lambert relation (A = eps * c * l  =>  c = A / (eps * l))
    per analyte using broadcasting, converting absorbance units to molar
    concentration units (mol/L).
    """
    validate_broadcast_shapes(matrix, molar_extinction_coeffs)
    if path_length_cm <= 0:
        raise ScientificInputError("path_length_cm must be positive")
    if np.any(molar_extinction_coeffs <= 0):
        raise ScientificInputError("Extinction coefficients must be positive")

    denom = molar_extinction_coeffs * path_length_cm  # shape (n_analytes,)
    return matrix / denom  # broadcasts against (n_samples, n_analytes)


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    raw = load_assay_matrix()
    logger.info("Raw assay matrix shape=%s", raw.shape)

    blanked = apply_scalar_offset(raw, background=0.05)
    print("Blank-subtracted (scalar broadcast) sample row 0:", np.round(blanked[0], 4))

    gain = np.array([1.02, 0.98, 1.05, 1.00])
    offset = np.array([-0.01, 0.00, 0.02, -0.02])
    calibrated = apply_per_analyte_calibration(blanked, gain, offset)
    print("Calibrated (vector broadcast) sample row 0:", np.round(calibrated[0], 4))

    normalized = z_score_normalize(calibrated)
    print("Z-normalized column means (~0):", np.round(normalized.mean(axis=0), 6))
    print("Z-normalized column stds (~1):", np.round(normalized.std(axis=0), 6))

    eps = np.array([15000.0, 8200.0, 21000.0, 12500.0])  # M^-1 cm^-1
    concentration = convert_units_absorbance_to_concentration(
        calibrated, eps, path_length_cm=1.0
    )
    print("Molar concentration (mol/L), sample row 0:", concentration[0])


if __name__ == "__main__":
    main()
