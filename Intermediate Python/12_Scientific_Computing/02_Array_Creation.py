"""
02_Array_Creation.py

Production-oriented patterns for constructing NumPy arrays used as scientific
grids: sampling time vectors, dose/concentration ranges, and simulation state
vectors for a simple pharmacokinetic-style model.
"""

from __future__ import annotations

import logging

import numpy as np

logger = logging.getLogger(__name__)


class ScientificInputError(ValueError):
    """Raised when scientific input data is invalid."""


def build_time_grid(duration_s: float, sample_rate_hz: float) -> np.ndarray:
    """
    Build a uniformly spaced time grid in seconds using np.arange.

    np.arange is appropriate here because the grid is defined by a fixed
    step size (1 / sample_rate_hz); floating-point endpoints from arange can
    be off by one sample due to rounding, so we compute n_samples explicitly
    rather than relying on arange's stop bound.
    """
    if duration_s <= 0 or sample_rate_hz <= 0:
        raise ScientificInputError("duration_s and sample_rate_hz must be positive")

    n_samples = int(round(duration_s * sample_rate_hz))
    dt = 1.0 / sample_rate_hz
    return np.arange(n_samples, dtype=np.float64) * dt


def build_dose_range(low_mg: float, high_mg: float, n_points: int) -> np.ndarray:
    """
    Build a dose-response concentration grid using np.linspace.

    np.linspace is preferred over np.arange when the number of points and the
    inclusive endpoints matter more than a fixed step size -- exactly the case
    for a dose-response curve where we want n_points from low_mg to high_mg
    inclusive, regardless of floating-point step accumulation.
    """
    if n_points < 2:
        raise ScientificInputError("n_points must be >= 2 to include both endpoints")
    if high_mg <= low_mg:
        raise ScientificInputError("high_mg must be greater than low_mg")

    return np.linspace(low_mg, high_mg, num=n_points, dtype=np.float64)


def build_log_dose_range(
    low_mg: float, high_mg: float, n_points: int
) -> np.ndarray:
    """
    Build a logarithmically spaced dose range using np.logspace, appropriate
    for dose-response studies spanning multiple orders of magnitude.
    """
    if low_mg <= 0 or high_mg <= 0:
        raise ScientificInputError("logspace doses must be strictly positive")
    if high_mg <= low_mg:
        raise ScientificInputError("high_mg must be greater than low_mg")

    return np.logspace(np.log10(low_mg), np.log10(high_mg), num=n_points)


def initialize_compartment_state(n_compartments: int) -> np.ndarray:
    """
    Initialize a zero-filled pharmacokinetic compartment state vector
    (e.g. [gut, plasma, tissue] drug amounts in mg).

    np.zeros is preferred over np.empty here because the state vector is a
    physical quantity (drug amount) that must start at a known, valid value.
    """
    if n_compartments <= 0:
        raise ScientificInputError("n_compartments must be positive")
    return np.zeros(n_compartments, dtype=np.float64)


def preallocate_simulation_buffer(
    n_steps: int, n_compartments: int
) -> np.ndarray:
    """
    Preallocate a simulation output buffer using np.empty for performance,
    with the explicit contract that every element will be overwritten by the
    caller before being read (the first row is set immediately below).

    Using np.empty here is safe only because we guarantee full initialization
    of row 0 before returning; callers filling subsequent rows during
    integration must not read uninitialized rows.
    """
    if n_steps <= 0 or n_compartments <= 0:
        raise ScientificInputError("n_steps and n_compartments must be positive")

    buffer = np.empty((n_steps, n_compartments), dtype=np.float64)
    buffer[0] = 0.0  # initial condition: all compartments empty at t=0
    return buffer


def replicate_baseline(baseline: np.ndarray, n_replicates: int) -> np.ndarray:
    """
    Build a matrix of replicate measurements from a baseline vector using
    np.full-style broadcasting via np.tile, simulating an assay plate layout.
    """
    if n_replicates <= 0:
        raise ScientificInputError("n_replicates must be positive")
    return np.tile(baseline, (n_replicates, 1))


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    t = build_time_grid(duration_s=2.0, sample_rate_hz=500.0)
    logger.info("Time grid: n=%d, dt=%.5f s, span=%.3f s", t.size, t[1] - t[0], t[-1])

    linear_doses = build_dose_range(low_mg=1.0, high_mg=100.0, n_points=10)
    log_doses = build_log_dose_range(low_mg=0.1, high_mg=1000.0, n_points=7)
    print("Linear dose grid (mg):", np.round(linear_doses, 3))
    print("Log-spaced dose grid (mg):", np.round(log_doses, 4))

    state0 = initialize_compartment_state(n_compartments=3)
    print("Initial compartment state (mg):", state0)

    sim_buffer = preallocate_simulation_buffer(n_steps=5, n_compartments=3)
    print("Preallocated buffer shape:", sim_buffer.shape)
    print("Row 0 (initial condition, guaranteed set):", sim_buffer[0])

    baseline = np.array([0.5, 1.2, 3.4])
    plate = replicate_baseline(baseline, n_replicates=4)
    print("Replicate plate:\n", plate)


if __name__ == "__main__":
    main()
