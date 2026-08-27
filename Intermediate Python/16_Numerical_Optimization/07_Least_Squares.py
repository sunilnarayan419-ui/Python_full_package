from __future__ import annotations

import numpy as np
from scipy.optimize import least_squares


class LogisticGrowthLeastSquaresEstimator:
    """Estimates logistic plant-growth model parameters using nonlinear least squares."""

    def __init__(self, days: np.ndarray, observed_height_cm: np.ndarray) -> None:
        self.days: np.ndarray = np.asarray(days, dtype=float)
        self.observed_height_cm: np.ndarray = np.asarray(observed_height_cm, dtype=float)
        if self.days.shape != self.observed_height_cm.shape:
            raise ValueError("Days and observed height arrays must share the same shape.")
        self.parameter_bounds: tuple[np.ndarray, np.ndarray] = (
            np.array([0.0, 0.0, 0.0]),
            np.array([200.0, 2.0, 60.0]),
        )
        self.fitted_parameters: np.ndarray | None = None

    @staticmethod
    def logistic_growth_model(days: np.ndarray, carrying_capacity_cm: float, growth_rate: float, midpoint_day: float) -> np.ndarray:
        return carrying_capacity_cm / (1.0 + np.exp(-growth_rate * (days - midpoint_day)))

    def residual_function(self, parameters: np.ndarray) -> np.ndarray:
        carrying_capacity_cm, growth_rate, midpoint_day = parameters
        predicted_height_cm = self.logistic_growth_model(self.days, carrying_capacity_cm, growth_rate, midpoint_day)
        return predicted_height_cm - self.observed_height_cm

    def estimate_parameters(self) -> dict[str, float | int | bool | str]:
        initial_guess = np.array(
            [float(np.max(self.observed_height_cm)) * 1.1, 0.2, float(np.median(self.days))]
        )

        result = least_squares(
            fun=self.residual_function,
            x0=initial_guess,
            bounds=self.parameter_bounds,
            method="trf",
            xtol=1e-12,
            ftol=1e-12,
        )

        if not result.success:
            raise RuntimeError(f"Least-squares optimization failed: {result.message}")

        self.fitted_parameters = result.x
        return {
            "success": bool(result.success),
            "carrying_capacity_cm": float(result.x[0]),
            "growth_rate": float(result.x[1]),
            "midpoint_day": float(result.x[2]),
            "cost": float(result.cost),
            "n_function_evaluations": int(result.nfev),
        }

    def validate_solution(self, residual_tolerance: float = 5.0) -> bool:
        if self.fitted_parameters is None:
            raise RuntimeError("Parameters must be estimated before validation.")
        residuals = self.residual_function(self.fitted_parameters)
        max_absolute_residual = float(np.max(np.abs(residuals)))
        within_bounds = bool(
            np.all(self.fitted_parameters >= self.parameter_bounds[0])
            and np.all(self.fitted_parameters <= self.parameter_bounds[1])
        )
        return bool(max_absolute_residual < residual_tolerance and within_bounds)

    @staticmethod
    def run() -> None:
        rng = np.random.default_rng(42)

        days = np.linspace(0.0, 40.0, 25)
        true_capacity, true_rate, true_midpoint = 85.0, 0.22, 18.0
        noise = rng.normal(loc=0.0, scale=1.2, size=days.shape[0])
        observed_height_cm = LogisticGrowthLeastSquaresEstimator.logistic_growth_model(
            days, true_capacity, true_rate, true_midpoint
        ) + noise

        estimator = LogisticGrowthLeastSquaresEstimator(days, observed_height_cm)
        estimation_result = estimator.estimate_parameters()
        print("Estimation result:", estimation_result)

        is_valid = estimator.validate_solution()
        print("Solution validated:", is_valid)


if __name__ == "__main__":
    LogisticGrowthLeastSquaresEstimator.run()
