from __future__ import annotations

import numpy as np
from scipy import optimize

RANDOM_STATE: int = 42


class RegularizedGrowthModelOptimizer:
    """Minimizes a convex ridge-regularized objective for a plant growth-rate model."""

    def __init__(self, features: np.ndarray, targets: np.ndarray, regularization_strength: float = 1.0) -> None:
        self.features: np.ndarray = np.asarray(features, dtype=float)
        self.targets: np.ndarray = np.asarray(targets, dtype=float)
        if self.features.shape[0] != self.targets.shape[0]:
            raise ValueError("Feature and target row counts do not match.")
        if regularization_strength < 0.0:
            raise ValueError("Regularization strength must be non-negative.")
        self.regularization_strength: float = regularization_strength
        self.n_samples: int = self.features.shape[0]
        self.n_features: int = self.features.shape[1]

    def objective(self, parameters: np.ndarray) -> float:
        predictions = self.features @ parameters
        residuals = predictions - self.targets
        data_term = float(np.sum(residuals**2) / self.n_samples)
        penalty_term = float(self.regularization_strength * np.sum(parameters**2))
        return data_term + penalty_term

    def gradient(self, parameters: np.ndarray) -> np.ndarray:
        predictions = self.features @ parameters
        residuals = predictions - self.targets
        data_gradient = (2.0 / self.n_samples) * (self.features.T @ residuals)
        penalty_gradient = 2.0 * self.regularization_strength * parameters
        return data_gradient + penalty_gradient

    def closed_form_solution(self) -> np.ndarray:
        identity = np.eye(self.n_features)
        gram_matrix = self.features.T @ self.features
        regularized_matrix = gram_matrix + self.n_samples * self.regularization_strength * identity
        return np.linalg.solve(regularized_matrix, self.features.T @ self.targets)

    def optimize(self) -> dict[str, np.ndarray | float | bool]:
        initial_parameters = np.zeros(self.n_features)
        result = optimize.minimize(
            fun=self.objective,
            x0=initial_parameters,
            jac=self.gradient,
            method="L-BFGS-B",
            options={"gtol": 1e-10, "maxiter": 2000},
        )
        if not result.success:
            raise RuntimeError(f"Convex optimization failed: {result.message}")
        return {
            "parameters": result.x,
            "objective_value": float(result.fun),
            "success": bool(result.success),
        }

    def validate_solution(self, parameters: np.ndarray, tolerance: float = 1e-4) -> bool:
        reference_solution = self.closed_form_solution()
        max_deviation = float(np.max(np.abs(parameters - reference_solution)))
        return max_deviation < tolerance

    @staticmethod
    def run() -> None:
        rng = np.random.default_rng(RANDOM_STATE)

        soil_ph = rng.uniform(5.5, 7.5, size=60)
        humidity_percent = rng.uniform(40.0, 80.0, size=60)
        noise = rng.normal(loc=0.0, scale=0.3, size=60)

        growth_rate = 0.4 * soil_ph + 0.02 * humidity_percent + noise
        features = np.column_stack([soil_ph, humidity_percent])

        optimizer = RegularizedGrowthModelOptimizer(features, growth_rate, regularization_strength=0.05)
        optimization_result = optimizer.optimize()

        print("Optimization result:", optimization_result)

        is_valid = optimizer.validate_solution(optimization_result["parameters"])
        print("Matches closed-form ridge solution:", is_valid)
        print("Closed-form solution:", optimizer.closed_form_solution())


if __name__ == "__main__":
    RegularizedGrowthModelOptimizer.run()
