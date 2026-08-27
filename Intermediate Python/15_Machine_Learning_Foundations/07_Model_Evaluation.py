from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    precision_score,
    r2_score,
    recall_score,
    roc_auc_score,
    root_mean_squared_error,
)
from sklearn.model_selection import train_test_split

RANDOM_STATE: int = 42


class TreatmentResponseEvaluator:
    """Reusable evaluation utility for regression and binary-classification biological models."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data: pd.DataFrame = data.copy()
        self.feature_columns: list[str] = ["concentration_mg_l", "cell_viability", "temperature_c"]
        self.target_column: str = "responder"
        self.model: LogisticRegression = LogisticRegression(random_state=RANDOM_STATE, max_iter=1000)
        self.x_train: pd.DataFrame | None = None
        self.x_test: pd.DataFrame | None = None
        self.y_train: pd.Series | None = None
        self.y_test: pd.Series | None = None

    def prepare_data(self, test_size: float = 0.3) -> None:
        features = self.data[self.feature_columns]
        target = self.data[self.target_column]
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            features, target, test_size=test_size, random_state=RANDOM_STATE, stratify=target
        )

    def train_model(self) -> None:
        if self.x_train is None or self.y_train is None:
            raise RuntimeError("Data must be prepared before training.")
        self.model.fit(self.x_train, self.y_train)

    @staticmethod
    def evaluate_regression(y_true: pd.Series, y_pred: np.ndarray) -> dict[str, float]:
        return {
            "mae": float(mean_absolute_error(y_true, y_pred)),
            "rmse": float(root_mean_squared_error(y_true, y_pred)),
            "r2": float(r2_score(y_true, y_pred)),
        }

    @staticmethod
    def evaluate_classification(
        y_true: pd.Series, y_pred: np.ndarray, y_proba: np.ndarray | None = None
    ) -> dict[str, float]:
        metrics: dict[str, float] = {
            "accuracy": float(accuracy_score(y_true, y_pred)),
            "precision": float(precision_score(y_true, y_pred, zero_division=0)),
            "recall": float(recall_score(y_true, y_pred, zero_division=0)),
            "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        }
        if y_proba is not None:
            metrics["roc_auc"] = float(roc_auc_score(y_true, y_proba))
        return metrics

    def run_evaluation(self) -> dict[str, float]:
        if self.x_test is None or self.y_test is None:
            raise RuntimeError("Data must be prepared before evaluation.")
        predictions = self.model.predict(self.x_test)
        probabilities = self.model.predict_proba(self.x_test)[:, 1]
        return self.evaluate_classification(self.y_test, predictions, probabilities)

    def confusion(self) -> np.ndarray:
        if self.x_test is None or self.y_test is None:
            raise RuntimeError("Data must be prepared before computing the confusion matrix.")
        predictions = self.model.predict(self.x_test)
        return confusion_matrix(self.y_test, predictions)

    @staticmethod
    def run() -> None:
        data = pd.DataFrame(
            [
                {"concentration_mg_l": 5.0, "cell_viability": 92.1, "temperature_c": 37.0, "responder": 0},
                {"concentration_mg_l": 10.0, "cell_viability": 85.4, "temperature_c": 37.0, "responder": 0},
                {"concentration_mg_l": 20.0, "cell_viability": 71.2, "temperature_c": 37.0, "responder": 1},
                {"concentration_mg_l": 25.0, "cell_viability": 63.8, "temperature_c": 37.0, "responder": 1},
                {"concentration_mg_l": 8.0, "cell_viability": 88.7, "temperature_c": 36.5, "responder": 0},
                {"concentration_mg_l": 30.0, "cell_viability": 55.6, "temperature_c": 37.5, "responder": 1},
                {"concentration_mg_l": 12.0, "cell_viability": 81.9, "temperature_c": 36.8, "responder": 0},
                {"concentration_mg_l": 22.0, "cell_viability": 68.4, "temperature_c": 37.2, "responder": 1},
                {"concentration_mg_l": 6.0, "cell_viability": 90.3, "temperature_c": 37.0, "responder": 0},
                {"concentration_mg_l": 28.0, "cell_viability": 58.1, "temperature_c": 37.4, "responder": 1},
                {"concentration_mg_l": 15.0, "cell_viability": 77.5, "temperature_c": 36.9, "responder": 0},
                {"concentration_mg_l": 24.0, "cell_viability": 65.2, "temperature_c": 37.1, "responder": 1},
                {"concentration_mg_l": 9.0, "cell_viability": 87.0, "temperature_c": 36.7, "responder": 0},
                {"concentration_mg_l": 27.0, "cell_viability": 59.9, "temperature_c": 37.3, "responder": 1},
                {"concentration_mg_l": 11.0, "cell_viability": 83.6, "temperature_c": 36.8, "responder": 0},
                {"concentration_mg_l": 21.0, "cell_viability": 69.7, "temperature_c": 37.0, "responder": 1},
                {"concentration_mg_l": 7.0, "cell_viability": 89.5, "temperature_c": 37.0, "responder": 0},
                {"concentration_mg_l": 26.0, "cell_viability": 61.3, "temperature_c": 37.2, "responder": 1},
                {"concentration_mg_l": 13.0, "cell_viability": 79.8, "temperature_c": 36.6, "responder": 0},
                {"concentration_mg_l": 23.0, "cell_viability": 66.9, "temperature_c": 37.1, "responder": 1},
            ]
        )

        evaluator = TreatmentResponseEvaluator(data)
        evaluator.prepare_data()
        evaluator.train_model()

        metrics = evaluator.run_evaluation()
        print("Structured evaluation metrics:", metrics)
        print("Confusion matrix:\n", evaluator.confusion())


if __name__ == "__main__":
    TreatmentResponseEvaluator.run()
