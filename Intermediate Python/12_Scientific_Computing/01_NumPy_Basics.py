"""
01_NumPy_Basics.py

Production-oriented introduction to NumPy fundamentals using a realistic
plant-phenotyping dataset (stem height, leaf area, chlorophyll index) collected
across multiple specimens and multiple measurement days.

Demonstrates ndarray core attributes, vectorized aggregation, and why NumPy
arrays are the correct data structure for numerical scientific workloads
instead of native Python lists.
"""

from __future__ import annotations

import logging

import numpy as np

logger = logging.getLogger(__name__)


class ScientificInputError(ValueError):
    """Raised when scientific input data is invalid."""


def load_plant_measurements() -> np.ndarray:
    """
    Return a (n_specimens, n_days, n_traits) float64 array of plant phenotyping
    measurements.

    Traits (axis=-1): [stem_height_cm, leaf_area_cm2, chlorophyll_index]
    """
    # In production this would come from a LIMS/instrument export; here we use
    # a small, deterministic, hand-specified dataset for reproducible execution.
    data = np.array(
        [
            # specimen 0: day0, day1, day2
            [[5.1, 2.3, 34.2], [6.4, 3.1, 36.0], [7.8, 4.0, 37.5]],
            # specimen 1
            [[4.8, 2.0, 33.0], [5.9, 2.7, 34.8], [7.1, 3.6, 36.1]],
            # specimen 2
            [[5.5, 2.6, 35.0], [6.9, 3.4, 37.2], [8.4, 4.4, 38.9]],
        ],
        dtype=np.float64,
    )
    return data


def validate_measurements(data: np.ndarray) -> None:
    """Validate that the measurement tensor has the expected rank and is finite."""
    if data.ndim != 3:
        raise ScientificInputError(
            f"Expected a 3D array (specimens, days, traits); got ndim={data.ndim}"
        )
    if not np.isfinite(data).all():
        raise ScientificInputError("Measurement array contains non-finite values")
    if data.shape[-1] != 3:
        raise ScientificInputError(
            f"Expected 3 traits per observation; got {data.shape[-1]}"
        )


def summarize_dataset(data: np.ndarray) -> dict[str, np.ndarray]:
    """
    Compute per-trait summary statistics across all specimens and days.

    Uses axis-aware aggregation rather than manual Python loops: reducing over
    axes (0, 1) collapses specimen and day, leaving one value per trait.
    """
    validate_measurements(data)

    trait_axis = (0, 1)
    summary = {
        "mean": data.mean(axis=trait_axis),
        "std": data.std(axis=trait_axis),
        "min": data.min(axis=trait_axis),
        "max": data.max(axis=trait_axis),
    }
    return summary


def growth_rate_per_specimen(data: np.ndarray) -> np.ndarray:
    """
    Compute the day-over-day growth rate for each specimen and trait using
    vectorized differencing (np.diff) along the day axis.

    Returns an array of shape (n_specimens, n_days - 1, n_traits).
    """
    validate_measurements(data)
    return np.diff(data, axis=1)


def list_vs_array_cost_illustration(n: int = 100_000) -> tuple[float, int]:
    """
    Illustrate why ndarrays are preferred over Python lists for numerical
    workloads: a contiguous, homogeneously-typed buffer allows vectorized
    elementwise operations without per-element Python object overhead.

    Returns (result_sum, itemsize_bytes) for a simple elementwise transform.
    """
    values = np.arange(n, dtype=np.float64)
    # Vectorized transform: no explicit Python-level loop over elements.
    transformed = values * 1.8 + 32.0  # e.g. Celsius -> Fahrenheit style scaling
    return float(transformed.sum()), values.itemsize


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    data = load_plant_measurements()
    logger.info(
        "Loaded measurement tensor: shape=%s dtype=%s ndim=%d size=%d",
        data.shape,
        data.dtype,
        data.ndim,
        data.size,
    )

    summary = summarize_dataset(data)
    trait_names = ("stem_height_cm", "leaf_area_cm2", "chlorophyll_index")
    for i, trait in enumerate(trait_names):
        print(
            f"{trait}: mean={summary['mean'][i]:.3f} "
            f"std={summary['std'][i]:.3f} "
            f"min={summary['min'][i]:.3f} "
            f"max={summary['max'][i]:.3f}"
        )

    rates = growth_rate_per_specimen(data)
    print("Per-specimen day-over-day growth rate shape:", rates.shape)
    print("Specimen 0 growth (day0->day1, day1->day2):\n", rates[0])

    total, itemsize = list_vs_array_cost_illustration()
    print(f"Vectorized transform sum={total:.1f}, itemsize={itemsize} bytes/element")


if __name__ == "__main__":
    main()
