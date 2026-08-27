from __future__ import annotations

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.model_selection import train_test_split

RANDOM_STATE: int = 42


class PlantBiomassEstimator:
    """Production-style estimator predicting plant biomass from phenotype measurements."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data: pd.DataFrame = data.copy()
        self.feature_columns: list[str] = ["height_cm", "leaf_count", "chlorophyll"]
        self.target_column: str = "biomass_g"
        self.model: LinearRegression = LinearRegression()
        self.x_train: pd.DataFrame | None = None
        self.x_test: pd.DataFrame | None = None
        self.y_train: pd.Series | None = None
        self.y_test: pd.Series | None = None

    def prepare_features_target(self) -> tuple[pd.DataFrame, pd.Series]:
        features = self.data[self.feature_columns]
        target = self.data[self.target_column]
        return features, target

    def split_data(self, test_size: float = 0.25) -> None:
        features, target = self.prepare_features_target()
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            features, target, test_size=test_size, random_state=RANDOM_STATE
        )

    def fit(self) -> None:
        if self.x_train is None or self.y_train is None:
            raise RuntimeError("Data must be split before fitting the model.")
        self.model.fit(self.x_train, self.y_train)

    def predict(self, features: pd.DataFrame) -> pd.Series:
        predictions = self.model.predict(features)
        return pd.Series(predictions, index=features.index, name="predicted_biomass_g")

    def evaluate(self) -> dict[str, float]:
        if self.x_test is None or self.y_test is None:
            raise RuntimeError("Data must be split before evaluation.")
        predictions = self.model.predict(self.x_test)
        return {
            "mae": float(mean_absolute_error(self.y_test, predictions)),
            "rmse": float(root_mean_squared_error(self.y_test, predictions)),
            "r2": float(r2_score(self.y_test, predictions)),
        }

    def inspect_coefficients(self) -> dict[str, float]:
        return dict(zip(self.feature_columns, self.model.coef_.tolist()))

    @staticmethod
    def run() -> None:
        data = pd.DataFrame(
            [
                {"height_cm": 12.4, "leaf_count": 5, "chlorophyll": 32.1, "biomass_g": 4.8},
                {"height_cm": 18.7, "leaf_count": 7, "chlorophyll": 38.4, "biomass_g": 7.9},
                {"height_cm": 9.1, "leaf_count": 4, "chlorophyll": 27.6, "biomass_g": 3.1},
                {"height_cm": 22.3, "leaf_count": 8, "chlorophyll": 41.2, "biomass_g": 9.6},
                {"height_cm": 15.6, "leaf_count": 6, "chlorophyll": 35.0, "biomass_g": 6.4},
                {"height_cm": 27.9, "leaf_count": 9, "chlorophyll": 44.8, "biomass_g": 11.8},
                {"height_cm": 11.2, "leaf_count": 5, "chlorophyll": 29.9, "biomass_g": 4.2},
                {"height_cm": 20.5, "leaf_count": 7, "chlorophyll": 39.7, "biomass_g": 8.7},
                {"height_cm": 14.8, "leaf_count": 6, "chlorophyll": 33.5, "biomass_g": 5.9},
                {"height_cm": 25.1, "leaf_count": 8, "chlorophyll": 43.0, "biomass_g": 10.5},
                {"height_cm": 8.3, "leaf_count": 3, "chlorophyll": 24.4, "biomass_g": 2.6},
                {"height_cm": 19.4, "leaf_count": 7, "chlorophyll": 37.9, "biomass_g": 8.1},
                {"height_cm": 16.9, "leaf_count": 6, "chlorophyll": 36.1, "biomass_g": 6.9},
                {"height_cm": 23.6, "leaf_count": 8, "chlorophyll": 42.3, "biomass_g": 9.9},
                {"height_cm": 10.5, "leaf_count": 4, "chlorophyll": 28.8, "biomass_g": 3.7},
                {"height_cm": 29.2, "leaf_count": 9, "chlorophyll": 46.1, "biomass_g": 12.6},
                {"height_cm": 13.7, "leaf_count": 5, "chlorophyll": 31.4, "biomass_g": 5.2},
                {"height_cm": 21.8, "leaf_count": 8, "chlorophyll": 40.6, "biomass_g": 9.1},
                {"height_cm": 17.3, "leaf_count": 6, "chlorophyll": 34.9, "biomass_g": 7.0},
                {"height_cm": 26.4, "leaf_count": 9, "chlorophyll": 45.0, "biomass_g": 11.2},
            ]
        )

        estimator = PlantBiomassEstimator(data)
        estimator.split_data()
        estimator.fit()

        metrics = estimator.evaluate()
        print("Evaluation metrics:", metrics)

        sample_predictions = estimator.predict(estimator.x_test)
        print("Sample predictions:\n", sample_predictions)

        print("Feature coefficients:", estimator.inspect_coefficients())


if __name__ == "__main__":
    PlantBiomassEstimator.run()
