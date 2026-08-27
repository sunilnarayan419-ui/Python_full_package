from __future__ import annotations

import pandas as pd
from sklearn.model_selection import train_test_split

RANDOM_STATE: int = 42


class DiseaseSeverityDataset:
    """Constructs, validates, and splits a biological classification dataset."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data: pd.DataFrame = data.copy()
        self.feature_columns: list[str] = ["leaf_count", "chlorophyll", "disease_score", "humidity_percent"]
        self.target_column: str = "severity_class"
        self.x_train: pd.DataFrame | None = None
        self.x_test: pd.DataFrame | None = None
        self.y_train: pd.Series | None = None
        self.y_test: pd.Series | None = None

    def validate_schema(self) -> None:
        required_columns = set(self.feature_columns + [self.target_column])
        missing_columns = required_columns - set(self.data.columns)
        if missing_columns:
            raise ValueError(f"Dataset is missing required columns: {sorted(missing_columns)}")
        if self.data[self.feature_columns].isnull().any().any():
            raise ValueError("Feature columns contain unexpected missing values.")

    def feature_target_split(self) -> tuple[pd.DataFrame, pd.Series]:
        features = self.data[self.feature_columns]
        target = self.data[self.target_column]
        if features.shape[0] != target.shape[0]:
            raise ValueError("Feature and target row counts do not match.")
        return features, target

    def train_test_split_stratified(self, test_size: float = 0.25) -> None:
        features, target = self.feature_target_split()
        class_counts = target.value_counts()
        if class_counts.min() < 2:
            raise ValueError("Each class must have at least two samples for stratified splitting.")
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            features, target, test_size=test_size, random_state=RANDOM_STATE, stratify=target
        )

    def describe_split(self) -> dict[str, tuple[int, int]]:
        if self.x_train is None or self.x_test is None:
            raise RuntimeError("Split has not been performed yet.")
        return {
            "train_shape": (self.x_train.shape[0], self.x_train.shape[1]),
            "test_shape": (self.x_test.shape[0], self.x_test.shape[1]),
        }

    def class_distribution(self) -> dict[str, dict[str, int]]:
        if self.y_train is None or self.y_test is None:
            raise RuntimeError("Split has not been performed yet.")
        return {
            "train": self.y_train.value_counts().to_dict(),
            "test": self.y_test.value_counts().to_dict(),
        }

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
            ]
        )

        dataset = DiseaseSeverityDataset(data)
        dataset.validate_schema()
        dataset.train_test_split_stratified()

        print("Split shapes:", dataset.describe_split())
        print("Class distribution:", dataset.class_distribution())


if __name__ == "__main__":
    DiseaseSeverityDataset.run()
