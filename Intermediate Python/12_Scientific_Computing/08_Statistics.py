"""
08_Statistics.py

Production-oriented statistical analysis of experimental assay data,
including missing-value handling, small-sample awareness, and appropriate
use of SciPy statistical tools alongside NumPy.
"""

from __future__ import annotations

import logging

import numpy as np
from scipy import stats

logger = logging.getLogger(__name__)


class ScientificInputError(ValueError):
    """Raised when scientific input data is invalid."""


def load_assay_replicates() -> np.ndarray:
    """
    Return a (n_conditions, n_replicates) matrix of assay readouts, with some
    missing values (np.nan) representing failed/excluded replicate wells --
    a common real-world occurrence in laboratory data.
    """
    data = np.array(
        [
            [12.1, 11.8, 12.4, np.nan, 12.0],
            [15.3, 15.9, np.nan, 15.5, 15.7],
            [9.8, 10.1, 10.0, 9.9, np.nan],
        ]
    )
    return data


def describe_with_missing_values(matrix: np.ndarray) -> dict[str, np.ndarray]:
    """
    Compute per-condition summary statistics that correctly ignore NaN
    (missing) entries. np.mean/np.std would silently propagate NaN across an
    entire row; np.nanmean/np.nanstd exclude missing entries explicitly.
    """
    if matrix.ndim != 2:
        raise ScientificInputError(f"Expected 2D matrix; got ndim={matrix.ndim}")

    n_valid = np.sum(~np.isnan(matrix), axis=1)
    if np.any(n_valid < 2):
        logger.warning(
            "One or more conditions have fewer than 2 valid replicates; "
            "variance estimates for those rows are unreliable"
        )

    return {
        "mean": np.nanmean(matrix, axis=1),
        "std": np.nanstd(matrix, axis=1, ddof=1),
        "median": np.nanmedian(matrix, axis=1),
        "n_valid": n_valid,
    }


def robust_percentiles(matrix: np.ndarray, percentiles: tuple[float, ...] = (25, 50, 75)) -> np.ndarray:
    """
    Compute percentiles per condition, ignoring NaNs, using
    np.nanpercentile. Percentiles are more robust to outliers than mean/std
    for small, noisy experimental samples.
    """
    return np.nanpercentile(matrix, percentiles, axis=1)


def analyte_correlation(analyte_a: np.ndarray, analyte_b: np.ndarray) -> tuple[float, float]:
    """
    Compute the Pearson correlation coefficient between two analyte
    measurement series and its associated p-value using SciPy.

    A correlation, however strong, does NOT establish that one analyte
    causes changes in the other -- both may be driven by a shared upstream
    biological or experimental factor. Report correlation as an association,
    not a causal claim.
    """
    if analyte_a.shape != analyte_b.shape:
        raise ScientificInputError("analyte_a and analyte_b must have matching shapes")
    if analyte_a.size < 3:
        raise ScientificInputError("Need at least 3 paired observations for a meaningful correlation")

    result = stats.pearsonr(analyte_a, analyte_b)
    return float(result.statistic), float(result.pvalue)


def covariance_matrix(feature_matrix: np.ndarray) -> np.ndarray:
    """
    Compute the covariance matrix across features (columns) of a
    (n_samples, n_features) matrix using np.cov, which expects variables as
    rows by default -- we transpose explicitly and document the convention
    to avoid a common shape-related bug.
    """
    if feature_matrix.ndim != 2:
        raise ScientificInputError(f"Expected 2D matrix; got ndim={feature_matrix.ndim}")
    if feature_matrix.shape[0] < 2:
        raise ScientificInputError("Need at least 2 samples to estimate covariance")

    return np.cov(feature_matrix, rowvar=False)


def compare_treatment_groups(control: np.ndarray, treated: np.ndarray) -> dict[str, float]:
    """
    Perform an independent two-sample t-test (Welch's, unequal variance
    assumed) comparing control vs treated group measurements using SciPy,
    appropriate when equal-variance cannot be assumed a priori.
    """
    if control.size < 2 or treated.size < 2:
        raise ScientificInputError("Each group needs at least 2 observations")

    result = stats.ttest_ind(control, treated, equal_var=False, nan_policy="raise")
    return {
        "t_statistic": float(result.statistic),
        "p_value": float(result.pvalue),
        "control_mean": float(np.mean(control)),
        "treated_mean": float(np.mean(treated)),
    }


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    matrix = load_assay_replicates()
    summary = describe_with_missing_values(matrix)
    for i in range(matrix.shape[0]):
        print(
            f"Condition {i}: mean={summary['mean'][i]:.3f} "
            f"std={summary['std'][i]:.3f} "
            f"median={summary['median'][i]:.3f} "
            f"n_valid={summary['n_valid'][i]}"
        )

    pct = robust_percentiles(matrix)
    print("25/50/75th percentiles per condition:\n", np.round(pct, 3))

    rng = np.random.default_rng(seed=1)
    analyte_a = rng.normal(size=30)
    analyte_b = 0.7 * analyte_a + rng.normal(scale=0.5, size=30)
    r, p = analyte_correlation(analyte_a, analyte_b)
    print(f"Pearson r={r:.3f}, p={p:.4f} (association only, not causal)")

    features = rng.normal(size=(50, 3))
    cov = covariance_matrix(features)
    print("Feature covariance matrix:\n", np.round(cov, 3))

    control = rng.normal(loc=10.0, scale=1.0, size=8)
    treated = rng.normal(loc=12.5, scale=1.2, size=8)
    ttest_result = compare_treatment_groups(control, treated)
    print("Welch's t-test result:", {k: round(v, 4) for k, v in ttest_result.items()})


if __name__ == "__main__":
    main()
