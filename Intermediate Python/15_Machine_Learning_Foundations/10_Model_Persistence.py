from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

RANDOM_STATE: int = 42
ARTIFACT_DIRECTORY: Path = Path("artifacts")
MODEL_PATH: Path = ARTIFACT_DIRECTORY / "treatment_response_pipeline.joblib"


class TreatmentResponseModelPersistence:
    """Trains, persists, reloads, and verifies a treatment-response classification pipeline."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data: pd.DataFrame = data.copy()
        self.numerical_columns: list[str] = ["concentration_mg_l", "cell_viability", "temperature_c"]
        self.categorical_columns: list[str] = ["species", "treatment"]
        self.target_column: str = "response_category"
        self.pipeline: Pipeline = self._build_pipeline()
        self.x_train: pd.DataFrame | None = None
        self.x_test: pd.DataFrame | None = None
        self.y_train: pd.Series | None = None
        self.y_test: pd.Series | None = None
        self.loaded_pipeline: Pipeline | None = None

    def _build_pipeline(self) -> Pipeline:
        numerical_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
            ]
        )
        categorical_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("encoder", OneHotEncoder(handle_unknown="ignore")),
            ]
        )
        preprocessor = ColumnTransformer(
            transformers=[
                ("numerical", numerical_pipeline, self.numerical_columns),
                ("categorical", categorical_pipeline, self.categorical_columns),
            ]
        )
        return Pipeline(
            steps=[
                ("preprocessing", preprocessor),
                ("classifier", GradientBoostingClassifier(n_estimators=150, max_depth=3, random_state=RANDOM_STATE)),
            ]
        )

    def prepare_data(self, test_size: float = 0.3) -> None:
        features = self.data[self.numerical_columns + self.categorical_columns]
        target = self.data[self.target_column]
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            features, target, test_size=test_size, random_state=RANDOM_STATE, stratify=target
        )

    def train(self) -> None:
        if self.x_train is None or self.y_train is None:
            raise RuntimeError("Data must be prepared before training.")
        self.pipeline.fit(self.x_train, self.y_train)

    def save_model(self, path: Path = MODEL_PATH) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.pipeline, path)

    def load_model(self, path: Path = MODEL_PATH) -> None:
        if not path.exists():
            raise FileNotFoundError(f"No persisted model found at {path}.")
        self.loaded_pipeline = joblib.load(path)

    def predict_with_loaded_model(self, features: pd.DataFrame) -> pd.Series:
        if self.loaded_pipeline is None:
            raise RuntimeError("Model must be loaded before running inference.")
        predictions = self.loaded_pipeline.predict(features)
        return pd.Series(predictions, index=features.index, name="predicted_response_category")

    def verify_consistency(self) -> bool:
        if self.x_test is None:
            raise RuntimeError("Data must be prepared before verifying consistency.")
        original_predictions = self.pipeline.predict(self.x_test)
        loaded_predictions = self.predict_with_loaded_model(self.x_test).to_numpy()
        return bool((original_predictions == loaded_predictions).all())

    @staticmethod
    def run() -> None:
        data = pd.DataFrame(
            [
                {"species": "wheat", "treatment": "drug_a", "concentration_mg_l": 5.0, "cell_viability": 92.1, "temperature_c": 37.0, "response_category": "low"},
                {"species": "wheat", "treatment": "drug_b", "concentration_mg_l": 18.0, "cell_viability": 74.3, "temperature_c": 37.0, "response_category": "high"},
                {"species": "maize", "treatment": "drug_a", "concentration_mg_l": 8.0, "cell_viability": 87.6, "temperature_c": 36.8, "response_category": "low"},
                {"species": "maize", "treatment": "drug_b", "concentration_mg_l": 22.0, "cell_viability": 68.1, "temperature_c": 37.2, "response_category": "high"},
                {"species": "soybean", "treatment": "drug_a", "concentration_mg_l": 6.0, "cell_viability": 90.4, "temperature_c": 37.0, "response_category": "low"},
                {"species": "soybean", "treatment": "drug_b", "concentration_mg_l": 20.0, "cell_viability": 70.9, "temperature_c": 37.1, "response_category": "high"},
                {"species": "wheat", "treatment": "drug_a", "concentration_mg_l": 12.0, "cell_viability": 81.2, "temperature_c": 36.9, "response_category": "moderate"},
                {"species": "maize", "treatment": "drug_b", "concentration_mg_l": 25.0, "cell_viability": 61.5, "temperature_c": 37.4, "response_category": "high"},
                {"species": "wheat", "treatment": "drug_b", "concentration_mg_l": 14.0, "cell_viability": 78.9, "temperature_c": 37.0, "response_category": "moderate"},
                {"species": "soybean", "treatment": "drug_a", "concentration_mg_l": 9.0, "cell_viability": 86.0, "temperature_c": 36.7, "response_category": "low"},
                {"species": "maize", "treatment": "drug_a", "concentration_mg_l": 7.0, "cell_viability": 89.3, "temperature_c": 36.9, "response_category": "low"},
                {"species": "wheat", "treatment": "drug_b", "concentration_mg_l": 24.0, "cell_viability": 63.7, "temperature_c": 37.3, "response_category": "high"},
                {"species": "soybean", "treatment": "drug_b", "concentration_mg_l": 16.0, "cell_viability": 76.4, "temperature_c": 37.1, "response_category": "moderate"},
                {"species": "maize", "treatment": "drug_a", "concentration_mg_l": 13.0, "cell_viability": 80.1, "temperature_c": 36.8, "response_category": "moderate"},
                {"species": "wheat", "treatment": "drug_a", "concentration_mg_l": 4.0, "cell_viability": 93.5, "temperature_c": 37.0, "response_category": "low"},
                {"species": "soybean", "treatment": "drug_b", "concentration_mg_l": 21.0, "cell_viability": 69.2, "temperature_c": 37.2, "response_category": "high"},
                {"species": "maize", "treatment": "drug_b", "concentration_mg_l": 15.0, "cell_viability": 77.8, "temperature_c": 37.0, "response_category": "moderate"},
                {"species": "wheat", "treatment": "drug_a", "concentration_mg_l": 10.0, "cell_viability": 84.6, "temperature_c": 36.9, "response_category": "moderate"},
                {"species": "soybean", "treatment": "drug_a", "concentration_mg_l": 5.5, "cell_viability": 91.7, "temperature_c": 37.0, "response_category": "low"},
                {"species": "maize", "treatment": "drug_b", "concentration_mg_l": 26.0, "cell_viability": 59.8, "temperature_c": 37.5, "response_category": "high"},
            ]
        )

        manager = TreatmentResponseModelPersistence(data)
        manager.prepare_data()
        manager.train()
        manager.save_model()
        manager.load_model()

        predictions = manager.predict_with_loaded_model(manager.x_test)
        print("Predictions from reloaded model:\n", predictions)

        is_consistent = manager.verify_consistency()
        print("Predictions consistent after reload:", is_consistent)


if __name__ == "__main__":
    TreatmentResponseModelPersistence.run()
