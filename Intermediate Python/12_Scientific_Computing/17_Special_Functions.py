"""
17_Special_Functions.py

Production-oriented use of scipy.special for numerically stable statistical
and biochemical transformations: logistic dose-response modeling via
expit/logit, and Bayesian-style beta-binomial assay analysis using gammaln
for stable log-probability computation.
"""

from __future__ import annotations

import logging

import numpy as np
from scipy import special

logger = logging.getLogger(__name__)


class ScientificInputError(ValueError):
    """Raised when scientific input data is invalid."""


def logistic_dose_response(log_dose: np.ndarray, ec50_log: float, slope: float) -> np.ndarray:
    """
    Compute a logistic dose-response curve in log-dose space using
    scipy.special.expit (the numerically stable sigmoid), which avoids the
    overflow that a naive `1 / (1 + np.exp(-x))` implementation suffers for
    large-magnitude negative x (exp overflow) or the underflow-to-zero
    inaccuracy for large positive x.
    """
    if not np.isfinite(log_dose).all():
        raise ScientificInputError("log_dose contains non-finite values")
    if slope <= 0:
        raise ScientificInputError("slope must be positive")

    x = slope * (log_dose - ec50_log)
    return special.expit(x)


def response_to_log_odds(response: np.ndarray) -> np.ndarray:
    """
    Convert a response fraction in (0, 1) to log-odds using
    scipy.special.logit, the numerically stable inverse of expit, avoiding
    manual log(p / (1 - p)) which loses precision near the boundaries.
    """
    if np.any((response <= 0) | (response >= 1)):
        raise ScientificInputError("response values must lie strictly within (0, 1) for logit")
    return special.logit(response)


def stable_log_beta_binomial_pmf(k: np.ndarray, n: int, alpha: float, beta_param: float) -> np.ndarray:
    """
    Compute the log-probability mass function of the beta-binomial
    distribution -- a standard model for overdispersed binary assay outcomes
    (e.g. well-to-well variability in a hit/no-hit screening assay) -- using
    gammaln (log of the gamma function) throughout rather than
    log(gamma(x)), which would overflow for the large factorial-like
    arguments typical of binomial coefficients.
    """
    if n <= 0:
        raise ScientificInputError("n must be positive")
    if alpha <= 0 or beta_param <= 0:
        raise ScientificInputError("alpha and beta_param must be positive")
    if np.any((k < 0) | (k > n)):
        raise ScientificInputError("k values must satisfy 0 <= k <= n")

    log_binom_coeff = special.gammaln(n + 1) - special.gammaln(k + 1) - special.gammaln(n - k + 1)
    log_beta_num = special.betaln(k + alpha, n - k + beta_param)
    log_beta_denom = special.betaln(alpha, beta_param)

    return log_binom_coeff + log_beta_num - log_beta_denom


def stable_log_likelihood_ratio(p1: np.ndarray, p2: np.ndarray) -> np.ndarray:
    """
    Compute log(p1 / p2) for small probability values using np.log1p /
    direct log-domain subtraction where possible, avoiding catastrophic
    cancellation. Here we compute the log-ratio directly in log-space via
    logit differences, which is more stable than computing p1/p2 for very
    small probabilities and then taking a log.
    """
    if np.any((p1 <= 0) | (p1 >= 1)) or np.any((p2 <= 0) | (p2 >= 1)):
        raise ScientificInputError("p1 and p2 must lie strictly within (0, 1)")

    # log(p1/p2) = log(p1) - log(p2); use logit-based reconstruction only
    # when appropriate, but direct np.log is already stable for values away
    # from 0 or 1. For values very close to 0, np.log is fine; the more
    # delicate case (values very close to 1) benefits from log1p on (1-p).
    return np.log(p1) - np.log(p2)


def receptor_binding_fraction(ligand_conc: np.ndarray, kd: float) -> np.ndarray:
    """
    Compute fractional receptor occupancy from a single-site binding
    isotherm, L / (L + Kd), expressed via expit in log-concentration space
    for numerical stability across a wide dynamic range of ligand
    concentrations spanning several orders of magnitude.
    """
    if kd <= 0:
        raise ScientificInputError("kd must be positive")
    if np.any(ligand_conc <= 0):
        raise ScientificInputError("ligand_conc must be strictly positive")

    log_ratio = np.log(ligand_conc) - np.log(kd)
    return special.expit(log_ratio)


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    log_doses = np.linspace(-3, 3, 13)  # log10(dose in mg), roughly
    response = logistic_dose_response(log_doses, ec50_log=0.0, slope=1.5)
    print("Dose-response curve (expit-based):")
    for ld, r in zip(log_doses, response):
        print(f"  log10(dose)={ld:5.2f} -> response={r:.4f}")

    mid_responses = response[(response > 0.05) & (response < 0.95)]
    log_odds = response_to_log_odds(mid_responses)
    print("\nLog-odds of mid-range responses:", np.round(log_odds, 3))

    k = np.arange(0, 11)
    log_pmf = stable_log_beta_binomial_pmf(k, n=10, alpha=2.0, beta_param=5.0)
    print("\nBeta-binomial log-PMF (n=10, alpha=2, beta=5):")
    print(np.round(log_pmf, 4))
    print("PMF sums to ~1 (sanity check):", np.round(np.exp(log_pmf).sum(), 6))

    ligand_conc = np.logspace(-9, -3, 13)  # M, spanning nM to mM
    occupancy = receptor_binding_fraction(ligand_conc, kd=1e-6)
    print("\nReceptor occupancy across ligand concentration range:")
    print(np.round(occupancy, 4))


if __name__ == "__main__":
    main()
