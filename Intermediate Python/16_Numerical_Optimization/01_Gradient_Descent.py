from __future__ import annotations

import numpy as np

RANDOM_STATE: int = 42


class DrugResponseGradientDescent:
    """Fits a linear drug-response model via explicit gradient descent."""

    def __init__(
        self,
        features: np.ndarray,
        targets: np.ndarray,
        learning_rate: float = 0.05,
        max_iterations: int = 5000,
        tolerance: float = 1e-8,
    ) -> None:
        self.features: np.ndarray = np.asarray(features, dtype=float)
        self.targets: np.ndarray = np.asarray(targets, dtype=float)
        if self.features.shape[0] != self.targets.shape[0]:
            raise ValueError("Feature and target row counts do not match.")
        self.learning_rate: float = learning_rate
        self.max_iterations: int = max_iterations
        self.tolerance: float = tolerance
        self.n_samples: int = self.features.shape[0]
        self.n_features: int = self.features.shape[1]
        self.weights: np.ndarray = np.zeros(self.n_features)
        self.bias: float = 0.0
        self.loss_history: list[float] = []

    def _design_predictions(self, weights: np.ndarray, bias: float) -> np.ndarray:
        return self.features @ weights + bias

    def loss_function(self, weights: np.ndarray, bias: float) -> float:
        predictions = self._design_predictions(weights, bias)
        residuals = predictions - self.targets
        return float(np.mean(residuals**2))

    def gradient(self, weights: np.ndarray, bias: float) -> tuple[np.ndarray, float]:
        predictions = self._design_predictions(weights, bias)
        residuals = predictions - self.targets
        weight_gradient = (2.0 / self.n_samples) * (self.features.T @ residuals)
        bias_gradient = float((2.0 / self.n_samples) * np.sum(residuals))
        return weight_gradient, bias_gradient

    def fit(self) -> dict[str, float | int]:
        previous_loss = self.loss_function(self.weights, self.bias)
        self.loss_history.append(previous_loss)

        iteration = 0
        for iteration in range(1, self.max_iterations + 1):
            weight_gradient, bias_gradient = self.gradient(self.weights, self.bias)
            self.weights -= self.learning_rate * weight_gradient
            self.bias -= self.learning_rate * bias_gradient

            current_loss = self.loss_function(self.weights, self.bias)
            self.loss_history.append(current_loss)

            gradient_norm = float(np.linalg.norm(weight_gradient))
            loss_improvement = abs(previous_loss - current_loss)

            if gradient_norm < self.tolerance or loss_improvement < self.tolerance:
                break

            previous_loss = current_loss

        return {
            "iterations": iteration,
            "final_loss": self.loss_history[-1],
            "gradient_norm": float(np.linalg.norm(self.gradient(self.weights, self.bias)[0])),
        }

    def predict(self, features: np.ndarray) -> np.ndarray:
        features = np.asarray(features, dtype=float)
        return self._design_predictions(self.weights, self.bias)

    @staticmethod
    def run() -> None:
        rng = np.random.default_rng(RANDOM_STATE)

        dose_mg = np.linspace(1.0, 20.0, 40)
        temperature_c = np.linspace(35.0, 39.0, 40)
        noise = rng.normal(loc=0.0, scale=1.5, size=40)

        response_percent = 3.2 * dose_mg + 1.1 * temperature_c + noise
        features = np.column_stack([dose_mg, temperature_c])
        features = (features - features.mean(axis=0)) / features.std(axis=0)

        model = DrugResponseGradientDescent(features, response_percent, learning_rate=0.1, max_iterations=10000)
        fit_summary = model.fit()

        print("Fit summary:", fit_summary)
        print("Learned weights:", model.weights)
        print("Learned bias:", model.bias)

        predictions = model.predict(features[:5])
        print("Sample predictions:", predictions)
        print("Sample targets:", response_percent[:5])


if __name__ == "__main__":
    DrugResponseGradientDescent.run()
