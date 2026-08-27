from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split

RANDOM_STATE: int = 42


class PlantDiseaseClassifier:
    """Classifies plant disease severity from leaf and environmental measurements."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data: pd.DataFrame = data.copy()
        self.feature_columns: list[str] = ["leaf_count", "chlorophyll", "disease_score", "humidity_percent"]
        self.target_column: str = "severity_class"
        self.model: RandomForestClassifier = RandomForestClassifier(
            n_estimators=200, max_depth=5, random_state=RANDOM_STATE
        )
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

    def predict(self, features: pd.DataFrame) -> np.ndarray:
        return self.model.predict(features)

    def predict_probabilities(self, features: pd.DataFrame) -> pd.DataFrame:
        probabilities = self.model.predict_proba(features)
        return pd.DataFrame(probabilities, columns=self.model.classes_, index=features.index)

    def evaluate_model(self) -> dict[str, float]:
        if self.x_test is None or self.y_test is None:
            raise RuntimeError("Data must be prepared before evaluation.")
        predictions = self.model.predict(self.x_test)
        return {
            "accuracy": float(accuracy_score(self.y_test, predictions)),
            "precision_weighted": float(precision_score(self.y_test, predictions, average="weighted", zero_division=0)),
            "recall_weighted": float(recall_score(self.y_test, predictions, average="weighted", zero_division=0)),
            "f1_weighted": float(f1_score(self.y_test, predictions, average="weighted", zero_division=0)),
        }

    def confusion(self) -> np.ndarray:
        if self.x_test is None or self.y_test is None:
            raise RuntimeError("Data must be prepared before computing the confusion matrix.")
        predictions = self.model.predict(self.x_test)
        return confusion_matrix(self.y_test, predictions, labels=self.model.classes_)

    @staticmethod
    def run() -> None:
        data = pd.DataFrame(
            [
                {"leaf_count": 8, "chlorophyll": 41.2, "disease_score": 0.1, "humidity_percent": 55.0, "severity_class": "healthy"},
                {"leaf_count": 7, "chlorophyll": 38.9, "disease_score": 0.2, "humidity_percent": 57.3, "severity_class": "healthy"},
                {"leaf_count": 5, "chlorophyll": 29.4, "disease_score": 1.4, "humidity_percent": 63.1, "severity_class": "mild"},
                {"leaf_count": 6, "chlorophyll": 31.7, "disease_score": 1.6, "humidity_percent": 65.4, "severity_class": "mild"},
                {"leaf_count": 3, "chlorophyll": 18.2, "disease_score": 3.1, "humidity_percent": 72.8, "severity_class": "severe"},
                {"leaf_count": 2, "chlorophyll": 15.6, "disease_score": 3.4, "humidity_percent": 75.2, "severity_class": "severe"},
                {"leaf_count": 9, "chlorophyll": 43.5, "disease_score": 0.1, "humidity_percent": 52.7, "severity_class": "healthy"},
                {"leaf_count": 6, "chlorophyll": 30.5, "disease_score": 1.5, "humidity_percent": 64.0, "severity_class": "mild"},
                {"leaf_count": 3, "chlorophyll": 17.9, "disease_score": 3.2, "humidity_percent": 74.1, "severity_class": "severe"},
                {"leaf_count": 8, "chlorophyll": 40.1, "disease_score": 0.2, "humidity_percent": 54.5, "severity_class": "healthy"},
                {"leaf_count": 5, "chlorophyll": 28.6, "disease_score": 1.7, "humidity_percent": 66.8, "severity_class": "mild"},
                {"leaf_count": 2, "chlorophyll": 14.8, "disease_score": 3.6, "humidity_percent": 76.9, "severity_class": "severe"},
                {"leaf_count": 7, "chlorophyll": 39.4, "disease_score": 0.3, "humidity_percent": 56.2, "severity_class": "healthy"},
                {"leaf_count": 4, "chlorophyll": 27.1, "disease_score": 1.8, "humidity_percent": 67.5, "severity_class": "mild"},
                {"leaf_count": 3, "chlorophyll": 16.4, "disease_score": 3.3, "humidity_percent": 73.6, "severity_class": "severe"},
                {"leaf_count": 8, "chlorophyll": 42.0, "disease_score": 0.1, "humidity_percent": 53.9, "severity_class": "healthy"},
                {"leaf_count": 5, "chlorophyll": 29.9, "disease_score": 1.5, "humidity_percent": 64.7, "severity_class": "mild"},
                {"leaf_count": 2, "chlorophyll": 15.1, "disease_score": 3.5, "humidity_percent": 75.8, "severity_class": "severe"},
                {"leaf_count": 7, "chlorophyll": 37.6, "disease_score": 0.4, "humidity_percent": 58.1, "severity_class": "healthy"},
                {"leaf_count": 4, "chlorophyll": 26.3, "disease_score": 1.9, "humidity_percent": 68.2, "severity_class": "mild"},
                {"leaf_count": 3, "chlorophyll": 17.0, "disease_score": 3.0, "humidity_percent": 71.9, "severity_class": "severe"},
                {"leaf_count": 9, "chlorophyll": 44.1, "disease_score": 0.1, "humidity_percent": 51.8, "severity_class": "healthy"},
            ]
        )

        classifier = PlantDiseaseClassifier(data)
        classifier.prepare_data()
        classifier.train_model()

        metrics = classifier.evaluate_model()
        print("Classification metrics:", metrics)

        predictions = classifier.predict(classifier.x_test)
        print("Predictions:", predictions)

        probabilities = classifier.predict_probabilities(classifier.x_test)
        print("Class probabilities:\n", probabilities)

        print("Confusion matrix:\n", classifier.confusion())


if __name__ == "__main__":
    PlantDiseaseClassifier.run()
