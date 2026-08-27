"""
09_Fourier_Transform.py

Production-oriented Fourier analysis of a biological oscillation signal
(e.g. circadian reporter fluorescence sampled at fixed intervals), using
scipy.fft for the modern SciPy FFT workflow.
"""

from __future__ import annotations

import logging

import numpy as np
from scipy import fft as scipy_fft

logger = logging.getLogger(__name__)


class ScientificInputError(ValueError):
    """Raised when scientific input data is invalid."""


def simulate_oscillation_signal(
    duration_hours: float, sample_interval_hours: float, true_period_hours: float
) -> tuple[np.ndarray, np.ndarray]:
    """
    Simulate a noisy biological oscillator (e.g. circadian clock reporter)
    sampled at a fixed interval.

    Returns (time_hours, signal).
    """
    if duration_hours <= 0 or sample_interval_hours <= 0:
        raise ScientificInputError("duration_hours and sample_interval_hours must be positive")
    if true_period_hours <= 0:
        raise ScientificInputError("true_period_hours must be positive")

    n_samples = int(round(duration_hours / sample_interval_hours))
    t = np.arange(n_samples) * sample_interval_hours

    rng = np.random.default_rng(seed=5)
    clean = 3.0 * np.sin(2 * np.pi * t / true_period_hours) + 10.0
    noise = rng.normal(scale=0.4, size=n_samples)
    return t, clean + noise


def compute_amplitude_spectrum(
    signal: np.ndarray, sample_interval_hours: float
) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute the single-sided amplitude spectrum of a real-valued signal.

    Sampling frequency fs = 1 / sample_interval_hours (in cycles/hour).
    Frequency resolution df = fs / N.
    Nyquist frequency = fs / 2 -- the highest frequency representable
    without aliasing given this sampling interval.

    Returns (frequencies_per_hour, amplitude).
    """
    if signal.ndim != 1:
        raise ScientificInputError(f"Expected 1D signal; got ndim={signal.ndim}")
    if sample_interval_hours <= 0:
        raise ScientificInputError("sample_interval_hours must be positive")

    n = signal.shape[0]
    fs = 1.0 / sample_interval_hours
    nyquist = fs / 2.0
    df = fs / n
    logger.info(
        "FFT setup: n=%d, fs=%.4f cycles/hr, df=%.5f cycles/hr, nyquist=%.4f cycles/hr",
        n, fs, df, nyquist,
    )

    # Use scipy.fft.rfft for real-valued input: returns only the
    # non-negative-frequency half of the spectrum (the other half is the
    # complex conjugate mirror image and carries no extra information).
    spectrum = scipy_fft.rfft(signal)
    freqs = scipy_fft.rfftfreq(n, d=sample_interval_hours)  # cycles per hour

    # Normalize magnitude by N; double all but DC/Nyquist bins to recover
    # single-sided amplitude for a real signal.
    amplitude = np.abs(spectrum) / n
    amplitude[1:-1] *= 2.0

    return freqs, amplitude


def find_dominant_period(freqs: np.ndarray, amplitude: np.ndarray) -> float:
    """
    Identify the dominant oscillation period (in hours) by finding the peak
    of the amplitude spectrum, excluding the DC (0 Hz) component which
    represents the signal's mean offset, not an oscillation.
    """
    if freqs.shape != amplitude.shape:
        raise ScientificInputError("freqs and amplitude must have matching shapes")
    if freqs.size < 2:
        raise ScientificInputError("Spectrum too short to identify a dominant frequency")

    # Exclude index 0 (DC component).
    ac_freqs = freqs[1:]
    ac_amplitude = amplitude[1:]

    peak_idx = np.argmax(ac_amplitude)
    dominant_freq = ac_freqs[peak_idx]
    if dominant_freq == 0:
        raise ScientificInputError("Dominant frequency resolved to 0; check signal length/sampling")

    return 1.0 / dominant_freq


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    t, signal = simulate_oscillation_signal(
        duration_hours=120.0, sample_interval_hours=0.5, true_period_hours=24.0
    )
    logger.info("Simulated %d samples over %.1f hours", signal.size, t[-1])

    freqs, amplitude = compute_amplitude_spectrum(signal, sample_interval_hours=0.5)
    print("Frequency axis units: cycles/hour")
    print(f"First 5 frequency bins: {np.round(freqs[:5], 5)}")

    dominant_period = find_dominant_period(freqs, amplitude)
    print(f"Dominant estimated period: {dominant_period:.3f} hours (true period: 24.0 hours)")

    peak_idx = np.argmax(amplitude[1:]) + 1
    print(f"Peak amplitude: {amplitude[peak_idx]:.3f} a.u. at {freqs[peak_idx]:.5f} cycles/hour")


if __name__ == "__main__":
    main()
