from __future__ import annotations

import numpy as np
from scipy import optimize


class EnzymeActivityConditionOptimizer:
    """Optimizes temperature and pH to maximize nonlinear enzyme activity subject to nonlinear constraints."""

    def __init__(
        self,
        optimal_temperature_c: float = 37.0,
        optimal_ph: float = 7.0,
        temperature_sensitivity: float = 0.015,
        ph_sensitivity: float = 0.35,
    ) -> None:
        self.optimal_temperature_c: float = optimal_temperature_c
        self.optimal_ph: float = optimal_ph
        self.temperature_sensitivity: float = temperature_sensitivity
        self.ph_sensitivity: float = ph_sensitivity
        self.temperature_bounds: tuple[float, float] = (20.0, 55.0)
        self.ph_bounds: tuple[float, float] = (4.0, 9.0)

    def _enzyme_activity(self, parameters: np.ndarray) -> float:
        temperature_c, ph = parameters
        temperature_penalty = self.temperature_sensitivity * (temperature_c - self.optimal_temperature_c) ** 2
        ph_penalty = self.ph_sensitivity * (ph - self.optimal_ph) ** 2
        return float(100.0 * np.exp(-(temperature_penalty + ph_penalty)))

    def objective(self, parameters: np.ndarray) -> float:
        return -self._enzyme_activity(parameters)

    def _substrate_stability_constraint(self, parameters: np.ndarray) -> float:
        temperature_c, ph = parameters
        return 60.0 - (0.6 * temperature_c + 4.0 * (ph - 4.0) ** 2)

    def optimize(self) -> dict[str, np.ndarray | float | bool | str]:
        initial_guess = np.array([30.0, 6.0])
        constraints = [{"type": "ineq", "fun": self._substrate_stability_constraint}]
        bounds = [self.temperature_bounds, self.ph_bounds]

        result = optimize.minimize(
            fun=self.objective,
            x0=initial_guess,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
            options={"ftol": 1e-10, "maxiter": 500},
        )

        if not result.success:
            raise RuntimeError(f"Nonlinear optimization failed: {result.message}")

        return {
            "success": bool(result.success),
            "optimal_temperature_c": float(result.x[0]),
            "optimal_ph": float(result.x[1]),
            "maximum_enzyme_activity": float(-result.fun),
            "message": str(result.message),
        }

    def validate_solution(self, parameters: np.ndarray) -> bool:
        temperature_c, ph = parameters
        within_temperature_bounds = self.temperature_bounds[0] <= temperature_c <= self.temperature_bounds[1]
        within_ph_bounds = self.ph_bounds[0] <= ph <= self.ph_bounds[1]
        constraint_satisfied = self._substrate_stability_constraint(parameters) >= -1e-6
        return bool(within_temperature_bounds and within_ph_bounds and constraint_satisfied)

    @staticmethod
    def run() -> None:
        optimizer = EnzymeActivityConditionOptimizer()
        optimization_result = optimizer.optimize()

        print("Optimization result:", optimization_result)

        solution_parameters = np.array(
            [optimization_result["optimal_temperature_c"], optimization_result["optimal_ph"]]
        )
        is_valid = optimizer.validate_solution(solution_parameters)
        print("Solution satisfies constraints and bounds:", is_valid)


if __name__ == "__main__":
    EnzymeActivityConditionOptimizer.run()
