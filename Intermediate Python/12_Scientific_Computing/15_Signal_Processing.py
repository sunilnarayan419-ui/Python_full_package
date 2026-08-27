"""
15_Signal_Processing.py

Production-oriented scientific signal processing for a noisy physiological
time series (e.g. photoplethysmogram-style pulsatile signal), using
scipy.signal for zero-phase filtering and peak detection with explicit
attention to sampling frequency, filter stability, and edge effects.
"""

from __future__ import annotations

import logging

import numpy as np
from scipy import signal

logger = logging.getLogger(__name__)


class ScientificInputError(ValueError):
    """Raised when scientific input data is invalid."""


def simulate_physiological_signal(
    duration_s: float, sample_rate_hz: float, heart_rate_bpm: float
) -> tuple[np.ndarray, np.ndarray]:
    """
    Simulate a noisy pulsatile physiological signal with a dominant
    heart-rate-driven periodic component plus high-frequency sensor noise
    and slow baseline wander (motion artifact).

    Returns (time_s, signal_values).
    """
    if duration_s <= 0 or sample_rate_hz <= 0 or heart_rate_bpm <= 0:
        raise ScientificInputError("duration_s, sample_rate_hz, heart_rate_bpm must be positive")

    n_samples = int(round(duration_s * sample_rate_hz))
    t = np.arange(n_samples) / sample_rate_hz
    heart_rate_hz = heart_rate_bpm / 60.0

    rng = np.random.default_rng(seed=13)
    pulse = np.abs(np.sin(np.pi * heart_rate_hz * t)) ** 3  # peaked pulsatile shape
    baseline_wander = 0.3 * np.sin(2 * np.pi * 0.05 * t)  # slow motion artifact
    noise = rng.normal(scale=0.08, size=n_samples)

    return t, pulse + baseline_wander + noise


def design_bandpass_filter(
    sample_rate_hz: float, low_hz: float, high_hz: float, order: int = 4
) -> np.ndarray:
    """
    Design a Butterworth bandpass filter as second-order sections (SOS),
    the numerically stable representation preferred over transfer-function
    (b, a) coefficients for filters of order > ~4, where (b, a) form can
    suffer severe coefficient quantization/instability.
    """
    nyquist = sample_rate_hz / 2.0
    if not (0 < low_hz < high_hz < nyquist):
        raise ScientificInputError(
            f"Require 0 < low_hz < high_hz < nyquist ({nyquist} Hz); "
            f"got low={low_hz}, high={high_hz}"
        )

    sos = signal.butter(order, [low_hz, high_hz], btype="bandpass", fs=sample_rate_hz, output="sos")
    return sos


def apply_zero_phase_filter(sos: np.ndarray, raw_signal: np.ndarray) -> np.ndarray:
    """
    Apply the filter using sosfiltfilt for zero-phase filtering: the signal
    is filtered forward and backward, canceling the phase distortion a
    single-pass causal filter (sosfilt) would introduce. This is essential
    when the timing of physiological events (e.g. peak locations) matters.

    Edge effects: sosfiltfilt uses reflected boundary padding by default to
    reduce transient distortion at the start/end of the signal; results near
    the very edges are still less reliable than in the interior.
    """
    if raw_signal.ndim != 1:
        raise ScientificInputError(f"Expected 1D signal; got ndim={raw_signal.ndim}")
    min_len_required = 3 * (2 * sos.shape[0] + 1)  # sosfiltfilt's default padlen heuristic
    if raw_signal.size <= min_len_required:
        raise ScientificInputError(
            f"Signal too short ({raw_signal.size} samples) for stable zero-phase "
            f"filtering with this filter order; need > {min_len_required} samples"
        )
    return signal.sosfiltfilt(sos, raw_signal)


def detect_pulse_peaks(
    filtered_signal: np.ndarray, sample_rate_hz: float, min_heart_rate_bpm: float, max_heart_rate_bpm: float
) -> np.ndarray:
    """
    Detect pulse peaks using scipy.signal.find_peaks with a physiologically
    informed minimum distance constraint (derived from max plausible heart
    rate) to reject spurious noise peaks.
    """
    if min_heart_rate_bpm <= 0 or max_heart_rate_bpm <= min_heart_rate_bpm:
        raise ScientificInputError("Require 0 < min_heart_rate_bpm < max_heart_rate_bpm")

    max_hr_hz = max_heart_rate_bpm / 60.0
    min_distance_samples = int(sample_rate_hz / max_hr_hz)
    if min_distance_samples < 1:
        raise ScientificInputError("Computed min peak distance is less than 1 sample; check sample_rate_hz")

    peak_indices, _properties = signal.find_peaks(
        filtered_signal, distance=min_distance_samples, prominence=0.1
    )
    return peak_indices


def estimate_heart_rate(peak_indices: np.ndarray, sample_rate_hz: float) -> float:
    """Estimate mean heart rate (bpm) from consecutive detected peak intervals."""
    if peak_indices.size < 2:
        raise ScientificInputError("Need at least 2 detected peaks to estimate heart rate")

    intervals_s = np.diff(peak_indices) / sample_rate_hz
    mean_interval_s = intervals_s.mean()
    if mean_interval_s <= 0:
        raise ScientificInputError("Non-positive mean peak interval; invalid peak detection")

    return 60.0 / mean_interval_s


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    sample_rate_hz = 100.0
    t, raw = simulate_physiological_signal(
        duration_s=20.0, sample_rate_hz=sample_rate_hz, heart_rate_bpm=72.0
    )
    logger.info("Simulated %d samples at %.1f Hz", raw.size, sample_rate_hz)

    sos = design_bandpass_filter(sample_rate_hz, low_hz=0.5, high_hz=4.0, order=4)
    filtered = apply_zero_phase_filter(sos, raw)

    peaks = detect_pulse_peaks(
        filtered, sample_rate_hz, min_heart_rate_bpm=40.0, max_heart_rate_bpm=180.0
    )
    print(f"Detected {peaks.size} pulse peaks")

    hr_estimate = estimate_heart_rate(peaks, sample_rate_hz)
    print(f"Estimated heart rate: {hr_estimate:.1f} bpm (true simulated: 72.0 bpm)")

    print(f"Raw signal std: {raw.std():.4f}, filtered signal std: {filtered.std():.4f}")


if __name__ == "__main__":
    main()
