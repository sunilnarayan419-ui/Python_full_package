from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import KFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

RANDOM_STATE: int = 42


class CropYieldCrossValidator:
    """Validates a crop-yield regression model using k-fold cross-validation inside a pipeline."""

    def __init__(self, data: pd.DataFrame, n_splits: int = 5) -> None:
        self.data: pd.DataFrame = data.copy()
        self.feature_columns: list[str] = ["soil_ph", "temperature_c", "humidity_percent", "soil_moisture"]
        self.target_column: str = "yield_g"
        self.n_splits: int = n_splits
        self.pipeline: Pipeline = self._build_pipeline()
        self.cv_strategy: KFold = KFold(n_splits=n_splits, shuffle=True, random_state=RANDOM_STATE)

    def _build_pipeline(self) -> Pipeline:
        return Pipeline(
            steps=[
                ("scaler", StandardScaler()),
                ("regressor", GradientBoostingRegressor(n_estimators=150, max_depth=3, random_state=RANDOM_STATE)),
            ]
        )

    def get_features_target(self) -> tuple[pd.DataFrame, pd.Series]:
        features = self.data[self.feature_columns]
        target = self.data[self.target_column]
        return features, target

    def cross_validate_model(self) -> dict[str, float]:
        features, target = self.get_features_target()
        scoring = ["neg_mean_absolute_error", "r2"]
        results = cross_validate(
            self.pipeline, features, target, cv=self.cv_strategy, scoring=scoring, return_train_score=False
        )
        mae_scores = -results["test_neg_mean_absolute_error"]
        r2_scores = results["test_r2"]
        return {
            "mae_mean": float(np.mean(mae_scores)),
            "mae_std": float(np.std(mae_scores)),
            "r2_mean": float(np.mean(r2_scores)),
            "r2_std": float(np.std(r2_scores)),
        }

    @staticmethod
    def run() -> None:
        data = pd.DataFrame(
            [
                {"soil_ph": 6.1, "temperature_c": 21.5, "humidity_percent": 54.0, "soil_moisture": 26.4, "yield_g": 410.2},
                {"soil_ph": 6.4, "temperature_c": 23.0, "humidity_percent": 58.5, "soil_moisture": 29.1, "yield_g": 465.8},
                {"soil_ph": 5.8, "temperature_c": 19.8, "humidity_percent": 51.2, "soil_moisture": 23.7, "yield_g": 372.4},
                {"soil_ph": 6.7, "temperature_c": 24.6, "humidity_percent": 61.9, "soil_moisture": 32.5, "yield_g": 512.6},
                {"soil_ph": 6.2, "temperature_c": 22.1, "humidity_percent": 55.8, "soil_moisture": 27.3, "yield_g": 428.9},
                {"soil_ph": 6.9, "temperature_c": 25.9, "humidity_percent": 64.3, "soil_moisture": 34.8, "yield_g": 548.1},
                {"soil_ph": 5.6, "temperature_c": 18.4, "humidity_percent": 48.7, "soil_moisture": 21.2, "yield_g": 341.7},
                {"soil_ph": 6.5, "temperature_c": 23.7, "humidity_percent": 59.6, "soil_moisture": 30.4, "yield_g": 489.3},
                {"soil_ph": 6.0, "temperature_c": 20.6, "humidity_percent": 52.9, "soil_moisture": 24.9, "yield_g": 396.5},
                {"soil_ph": 6.8, "temperature_c": 25.2, "humidity_percent": 63.1, "soil_moisture": 33.6, "yield_g": 530.4},
                {"soil_ph": 6.3, "temperature_c": 22.8, "humidity_percent": 57.0, "soil_moisture": 28.5, "yield_g": 452.0},
                {"soil_ph": 5.9, "temperature_c": 19.2, "humidity_percent": 49.8, "soil_moisture": 22.3, "yield_g": 358.6},
                {"soil_ph": 6.6, "temperature_c": 24.1, "humidity_percent": 60.7, "soil_moisture": 31.2, "yield_g": 501.7},
                {"soil_ph": 6.1, "temperature_c": 21.0, "humidity_percent": 53.4, "soil_moisture": 25.8, "yield_g": 405.3},
                {"soil_ph": 7.0, "temperature_c": 26.4, "humidity_percent": 65.8, "soil_moisture": 35.9, "yield_g": 562.8},
                {"soil_ph": 5.7, "temperature_c": 18.9, "humidity_percent": 49.1, "soil_moisture": 21.8, "yield_g": 349.2},
                {"soil_ph": 6.4, "temperature_c": 23.3, "humidity_percent": 58.9, "soil_moisture": 29.7, "yield_g": 474.5},
                {"soil_ph": 6.2, "temperature_c": 21.9, "humidity_percent": 55.1, "soil_moisture": 26.9, "yield_g": 421.8},
                {"soil_ph": 6.7, "temperature_c": 24.9, "humidity_percent": 62.5, "soil_moisture": 33.1, "yield_g": 521.9},
                {"soil_ph": 6.0, "temperature_c": 20.2, "humidity_percent": 51.9, "soil_moisture": 24.1, "yield_g": 388.7},
                {"soil_ph": 6.9, "temperature_c": 26.0, "humidity_percent": 64.7, "soil_moisture": 35.2, "yield_g": 553.6},
                {"soil_ph": 5.8, "temperature_c": 19.5, "humidity_percent": 50.3, "soil_moisture": 22.9, "yield_g": 364.1},
                {"soil_ph": 6.3, "temperature_c": 22.4, "humidity_percent": 56.4, "soil_moisture": 27.9, "yield_g": 439.6},
                {"soil_ph": 6.6, "temperature_c": 24.4, "humidity_percent": 61.1, "soil_moisture": 31.7, "yield_g": 507.3},
                {"soil_ph": 6.1, "temperature_c": 21.3, "humidity_percent": 54.6, "soil_moisture": 26.8, "yield_g": 416.5},
            ]
        )

        validator = CropYieldCrossValidator(data, n_splits=5)
        cv_results = validator.cross_validate_model()
        print("Cross-validation results:", cv_results)


if __name__ == "__main__":
    CropYieldCrossValidator.run()
