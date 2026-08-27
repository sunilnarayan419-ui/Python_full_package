from __future__ import annotations

import logging
from dataclasses import dataclass

import numpy as np

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")


class SimulationParameterError(Exception):
    """Raised when simulation parameters are physically or mathematically invalid."""


@dataclass(frozen=True, slots=True)
class DrugDecayParameters:
    """Parameters for a single-compartment first-order drug elimination model."""

    initial_concentration_mg_l: float
    elimination_rate_constant_per_hour: float
    time_step_hours: float
    total_duration_hours: float

    def validate(self) -> None:
        if self.initial_concentration_mg_l <= 0:
            raise SimulationParameterError("initial_concentration_mg_l must be positive.")
        if self.elimination_rate_constant_per_hour <= 0:
            raise SimulationParameterError("elimination_rate_constant_per_hour must be positive.")
        if self.time_step_hours <= 0:
            raise SimulationParameterError("time_step_hours must be positive.")
        if self.total_duration_hours <= 0:
            raise SimulationParameterError("total_duration_hours must be positive.")
        if self.time_step_hours > self.total_duration_hours:
            raise SimulationParameterError("time_step_hours cannot exceed total_duration_hours.")


@dataclass(frozen=True, slots=True)
class SimulationResult:
    time_hours: np.ndarray
    concentration_mg_l: np.ndarray
    half_life_hours: float
    time_below_threshold_hours: float | None


class DrugConcentrationSimulator:
    """Simulates first-order drug elimination using a vectorized analytical solution.

    Models concentration decay as C(t) = C0 * exp(-k * t), the standard
    single-compartment first-order elimination model.
    """

    def simulate(self, params: DrugDecayParameters) -> SimulationResult:
        params.validate()

        n_steps = int(round(params.total_duration_hours / params.time_step_hours)) + 1
        time_hours = np.linspace(0.0, params.total_duration_hours, n_steps)
        concentration = params.initial_concentration_mg_l * np.exp(
            -params.elimination_rate_constant_per_hour * time_hours
        )

        half_life_hours = np.log(2) / params.elimination_rate_constant_per_hour

        return SimulationResult(
            time_hours=time_hours,
            concentration_mg_l=concentration,
            half_life_hours=round(float(half_life_hours), 3),
            time_below_threshold_hours=None,
        )

    def time_to_threshold(self, params: DrugDecayParameters, threshold_mg_l: float) -> float | None:
        if threshold_mg_l <= 0:
            raise SimulationParameterError("threshold_mg_l must be positive.")
        if threshold_mg_l >= params.initial_concentration_mg_l:
            return 0.0
        time_hours = np.log(params.initial_concentration_mg_l / threshold_mg_l) / (
            params.elimination_rate_constant_per_hour
        )
        return round(float(time_hours), 3)


def _summarize(result: SimulationResult) -> dict[str, float]:
    return {
        "final_concentration_mg_l": round(float(result.concentration_mg_l[-1]), 4),
        "mean_concentration_mg_l": round(float(result.concentration_mg_l.mean()), 4),
        "half_life_hours": result.half_life_hours,
    }


def run() -> dict[str, float]:
    """Runs a deterministic drug-concentration decay simulation."""
    params = DrugDecayParameters(
        initial_concentration_mg_l=50.0,
        elimination_rate_constant_per_hour=0.15,
        time_step_hours=0.5,
        total_duration_hours=48.0,
    )

    simulator = DrugConcentrationSimulator()
    result = simulator.simulate(params)
    summary = _summarize(result)

    threshold_time = simulator.time_to_threshold(params, threshold_mg_l=1.0)

    logger.info("Half-life: %.3f hours", result.half_life_hours)
    logger.info("Final concentration: %.4f mg/L", summary["final_concentration_mg_l"])
    logger.info("Mean concentration: %.4f mg/L", summary["mean_concentration_mg_l"])
    logger.info("Time to reach 1.0 mg/L: %.3f hours", threshold_time)

    return summary


if __name__ == "__main__":
    run()
