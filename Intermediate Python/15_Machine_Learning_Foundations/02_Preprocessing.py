from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

RANDOM_STATE: int = 42


class SoilSamplePreprocessor:
    """Builds a leakage-free preprocessing pipeline for mixed-type soil/plant sample data."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data: pd.DataFrame = data.copy()
        self.numerical_columns: list[str] = ["temperature_c", "humidity_percent", "soil_ph", "soil_moisture"]
        self.categorical_columns: list[str] = ["species", "treatment"]
        self.target_column: str = "growth_rate"
        self.preprocessor: ColumnTransformer = self._build_preprocessor()
        self.x_train: pd.DataFrame | None = None
        self.x_test: pd.DataFrame | None = None
        self.y_train: pd.Series | None = None
        self.y_test: pd.Series | None = None

    def _build_preprocessor(self) -> ColumnTransformer:
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
        return ColumnTransformer(
            transformers=[
                ("numerical", numerical_pipeline, self.numerical_columns),
                ("categorical", categorical_pipeline, self.categorical_columns),
            ]
        )

    def split_data(self, test_size: float = 0.25) -> None:
        features = self.data[self.numerical_columns + self.categorical_columns]
        target = self.data[self.target_column]
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            features, target, test_size=test_size, random_state=RANDOM_STATE
        )

    def fit_transform_train(self) -> np.ndarray:
        if self.x_train is None:
            raise RuntimeError("Data must be split before fitting the preprocessor.")
        return self.preprocessor.fit_transform(self.x_train)

    def transform_test(self) -> np.ndarray:
        if self.x_test is None:
            raise RuntimeError("Data must be split before transforming the test set.")
        return self.preprocessor.transform(self.x_test)

    def get_feature_names(self) -> list[str]:
        return list(self.preprocessor.get_feature_names_out())

    @staticmethod
    def run() -> None:
        data = pd.DataFrame(
            [
                {"species": "wheat", "treatment": "control", "temperature_c": 22.5, "humidity_percent": 55.0, "soil_ph": 6.4, "soil_moisture": 28.1, "growth_rate": 1.8},
                {"species": "wheat", "treatment": "fertilizer_a", "temperature_c": 24.1, "humidity_percent": 60.5, "soil_ph": 6.6, "soil_moisture": 31.4, "growth_rate": 2.3},
                {"species": "maize", "treatment": "control", "temperature_c": np.nan, "humidity_percent": 58.2, "soil_ph": 6.1, "soil_moisture": 27.0, "growth_rate": 1.6},
                {"species": "maize", "treatment": "fertilizer_b", "temperature_c": 26.3, "humidity_percent": 62.0, "soil_ph": np.nan, "soil_moisture": 33.8, "growth_rate": 2.7},
                {"species": "soybean", "treatment": "control", "temperature_c": 21.9, "humidity_percent": 53.4, "soil_ph": 6.3, "soil_moisture": 25.9, "growth_rate": 1.5},
                {"species": "soybean", "treatment": "fertilizer_a", "temperature_c": 23.4, "humidity_percent": 57.8, "soil_ph": 6.5, "soil_moisture": 29.6, "growth_rate": 2.1},
                {"species": "wheat", "treatment": "fertilizer_b", "temperature_c": 25.6, "humidity_percent": 61.2, "soil_ph": 6.7, "soil_moisture": 32.9, "growth_rate": 2.6},
                {"species": "maize", "treatment": "control", "temperature_c": 20.8, "humidity_percent": 51.7, "soil_ph": 6.0, "soil_moisture": 24.5, "growth_rate": 1.4},
                {"species": None, "treatment": "fertilizer_a", "temperature_c": 23.9, "humidity_percent": 59.1, "soil_ph": 6.4, "soil_moisture": 30.2, "growth_rate": 2.2},
                {"species": "soybean", "treatment": "fertilizer_b", "temperature_c": 26.8, "humidity_percent": 63.5, "soil_ph": 6.8, "soil_moisture": 34.7, "growth_rate": 2.9},
                {"species": "wheat", "treatment": "control", "temperature_c": 22.0, "humidity_percent": 54.3, "soil_ph": 6.2, "soil_moisture": 26.8, "growth_rate": 1.7},
                {"species": "maize", "treatment": "fertilizer_a", "temperature_c": 24.7, "humidity_percent": 60.9, "soil_ph": 6.5, "soil_moisture": 31.9, "growth_rate": 2.4},
                {"species": "soybean", "treatment": "control", "temperature_c": 21.4, "humidity_percent": 52.6, "soil_ph": 6.1, "soil_moisture": 25.3, "growth_rate": 1.5},
                {"species": "wheat", "treatment": "fertilizer_b", "temperature_c": 25.2, "humidity_percent": 60.4, "soil_ph": 6.6, "soil_moisture": 32.1, "growth_rate": 2.5},
                {"species": "maize", "treatment": "fertilizer_b", "temperature_c": 26.0, "humidity_percent": 61.8, "soil_ph": 6.7, "soil_moisture": 33.2, "growth_rate": 2.8},
                {"species": "soybean", "treatment": "fertilizer_a", "temperature_c": 23.1, "humidity_percent": 56.9, "soil_ph": 6.4, "soil_moisture": 28.7, "growth_rate": 2.0},
            ]
        )

        preprocessor = SoilSamplePreprocessor(data)
        preprocessor.split_data()

        transformed_train = preprocessor.fit_transform_train()
        transformed_test = preprocessor.transform_test()

        print("Transformed training shape:", transformed_train.shape)
        print("Transformed test shape:", transformed_test.shape)
        print("Output feature names:", preprocessor.get_feature_names())


if __name__ == "__main__":
    SoilSamplePreprocessor.run()
