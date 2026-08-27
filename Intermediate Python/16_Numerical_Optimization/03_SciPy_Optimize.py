from __future__ import annotations

import numpy as np
from scipy import optimize


class GrowthModelCalibrator:
    """Calibrates plant growth-rate model parameters against observed field data using scipy.optimize.minimize."""

    def __init__(self, temperature_c: np.ndarray, humidity_percent: np.ndarray, observed_growth_rate: np.ndarray) -> None:
        self.temperature_c: np.ndarray = np.asarray(temperature_c, dtype=float)
        self.humidity_percent: np.ndarray = np.asarray(humidity_percent, dtype=float)
        self.observed_growth_rate: np.ndarray = np.asarray(observed_growth_rate, dtype=float)
        if not (self.temperature_c.shape == self.humidity_percent.shape == self.observed_growth_rate.shape):
            raise ValueError("Input arrays must share the same shape.")
        self.parameter_bounds: list[tuple[float, float]] = [(0.0, 5.0), (0.0, 5.0), (-2.0, 2.0)]

    def _predict_growth_rate(self, parameters: np.ndarray) -> np.ndarray:
        temperature_coefficient, humidity_coefficient, intercept = parameters
        return temperature_coefficient * self.temperature_c + humidity_coefficient * self.humidity_percent + intercept

    def objective(self, parameters: np.ndarray) -> float:
        predicted = self._predict_growth_rate(parameters)
        residuals = predicted - self.observed_growth_rate
        return float(np.mean(residuals**2))

    def calibrate(self) -> dict[str, np.ndarray | float | bool | str]:
        initial_guess = np.array([0.1, 0.1, 0.0])
        result = optimize.minimize(
            fun=self.objective,
            x0=initial_guess,
            method="L-BFGS-B",
            bounds=self.parameter_bounds,
            options={"ftol": 1e-12, "maxiter": 1000},
        )
        if not result.success:
            raise RuntimeError(f"Calibration failed to converge: {result.message}")
        return {
            "parameters": result.x,
            "objective_value": float(result.fun),
            "success": bool(result.success),
            "message": str(result.message),
        }

    def validate_solution(self, parameters: np.ndarray) -> bool:
        within_bounds = all(
            lower <= value <= upper for value, (lower, upper) in zip(parameters, self.parameter_bounds)
        )
        residual_magnitude = float(np.max(np.abs(self._predict_growth_rate(parameters) - self.observed_growth_rate)))
        return bool(within_bounds and residual_magnitude < 1.0)

    @staticmethod
    def run() -> None:
        rng = np.random.default_rng(42)

        temperature_c = rng.uniform(18.0, 30.0, size=50)
        humidity_percent = rng.uniform(40.0, 75.0, size=50)
        noise = rng.normal(loc=0.0, scale=0.15, size=50)

        observed_growth_rate = 0.08 * temperature_c + 0.03 * humidity_percent - 1.2 + noise

        calibrator = GrowthModelCalibrator(temperature_c, humidity_percent, observed_growth_rate)
        calibration_result = calibrator.calibrate()

        print("Calibration result:", calibration_result)

        is_valid = calibrator.validate_solution(calibration_result["parameters"])
        print("Solution validated:", is_valid)


if __name__ == "__main__":
    GrowthModelCalibrator.run()
