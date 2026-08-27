from __future__ import annotations

import numpy as np
from scipy.optimize import curve_fit


class MichaelisMentenKineticsFitter:
    """Fits Michaelis-Menten enzyme kinetics parameters to experimental reaction-rate observations."""

    def __init__(self, substrate_concentration: np.ndarray, reaction_velocity: np.ndarray) -> None:
        self.substrate_concentration: np.ndarray = np.asarray(substrate_concentration, dtype=float)
        self.reaction_velocity: np.ndarray = np.asarray(reaction_velocity, dtype=float)
        if self.substrate_concentration.shape != self.reaction_velocity.shape:
            raise ValueError("Substrate concentration and reaction velocity arrays must share the same shape.")
        self.fitted_parameters: np.ndarray | None = None
        self.parameter_covariance: np.ndarray | None = None

    @staticmethod
    def michaelis_menten_model(substrate_concentration: np.ndarray, v_max: float, k_m: float) -> np.ndarray:
        return (v_max * substrate_concentration) / (k_m + substrate_concentration)

    def fit_model(self) -> dict[str, float]:
        initial_guess = (float(np.max(self.reaction_velocity)) * 1.2, float(np.median(self.substrate_concentration)))
        parameter_bounds = ([0.0, 1e-6], [np.inf, np.inf])

        self.fitted_parameters, self.parameter_covariance = curve_fit(
            f=self.michaelis_menten_model,
            xdata=self.substrate_concentration,
            ydata=self.reaction_velocity,
            p0=initial_guess,
            bounds=parameter_bounds,
            maxfev=5000,
        )

        v_max, k_m = self.fitted_parameters
        parameter_standard_errors = np.sqrt(np.diag(self.parameter_covariance))
        return {
            "v_max": float(v_max),
            "k_m": float(k_m),
            "v_max_std_error": float(parameter_standard_errors[0]),
            "k_m_std_error": float(parameter_standard_errors[1]),
        }

    def predict(self, substrate_concentration: np.ndarray) -> np.ndarray:
        if self.fitted_parameters is None:
            raise RuntimeError("Model must be fit before prediction.")
        return self.michaelis_menten_model(np.asarray(substrate_concentration, dtype=float), *self.fitted_parameters)

    def residual_analysis(self) -> dict[str, float]:
        predicted_velocity = self.predict(self.substrate_concentration)
        residuals = self.reaction_velocity - predicted_velocity
        total_sum_squares = float(np.sum((self.reaction_velocity - np.mean(self.reaction_velocity)) ** 2))
        residual_sum_squares = float(np.sum(residuals**2))
        r_squared = 1.0 - (residual_sum_squares / total_sum_squares) if total_sum_squares > 0.0 else 0.0
        return {
            "residual_sum_squares": residual_sum_squares,
            "max_absolute_residual": float(np.max(np.abs(residuals))),
            "r_squared": float(r_squared),
        }

    @staticmethod
    def run() -> None:
        rng = np.random.default_rng(42)

        substrate_concentration = np.array([0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0, 15.0, 20.0, 30.0])
        true_v_max, true_k_m = 95.0, 4.5
        noise = rng.normal(loc=0.0, scale=1.8, size=substrate_concentration.shape[0])
        reaction_velocity = MichaelisMentenKineticsFitter.michaelis_menten_model(
            substrate_concentration, true_v_max, true_k_m
        ) + noise

        fitter = MichaelisMentenKineticsFitter(substrate_concentration, reaction_velocity)
        fit_results = fitter.fit_model()
        print("Fitted kinetic parameters:", fit_results)

        goodness_of_fit = fitter.residual_analysis()
        print("Goodness-of-fit metrics:", goodness_of_fit)

        predicted_velocity = fitter.predict(substrate_concentration)
        print("Predicted velocities:", predicted_velocity)


if __name__ == "__main__":
    MichaelisMentenKineticsFitter.run()
