"""
bioutils.stats_tools

Reusable statistical summary utilities for laboratory measurements.
"""

import statistics


def summarize_measurements(values: list[float]) -> dict[str, float]:
    """Return a summary of mean, stdev, min, and max for a measurement set."""
    if not values:
        raise ValueError("values must contain at least one measurement.")

    return {
        "mean": statistics.mean(values),
        "stdev": statistics.stdev(values) if len(values) > 1 else 0.0,
        "min": min(values),
        "max": max(values),
    }
