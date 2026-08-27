from __future__ import annotations

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.model_selection import train_test_split

RANDOM_STATE: int = 42


class CropYieldRegressor:
    """Predicts crop yield from environmental and soil measurements using a random forest."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data: pd.DataFrame = data.copy()
        self.feature_columns: list[str] = ["soil_ph", "temperature_c", "humidity_percent", "soil_moisture"]
        self.target_column: str = "yield_g"
        self.model: RandomForestRegressor = RandomForestRegressor(
            n_estimators=200, max_depth=6, random_state=RANDOM_STATE
        )
        self.x_train: pd.DataFrame | None = None
        self.x_test: pd.DataFrame | None = None
        self.y_train: pd.Series | None = None
        self.y_test: pd.Series | None = None

    def prepare_data(self, test_size: float = 0.25) -> None:
        features = self.data[self.feature_columns]
        target = self.data[self.target_column]
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            features, target, test_size=test_size, random_state=RANDOM_STATE
        )

    def train_model(self) -> None:
        if self.x_train is None or self.y_train is None:
            raise RuntimeError("Data must be prepared before training.")
        self.model.fit(self.x_train, self.y_train)

    def predict(self, features: pd.DataFrame) -> pd.Series:
        predictions = self.model.predict(features)
        return pd.Series(predictions, index=features.index, name="predicted_yield_g")

    def evaluate_model(self) -> dict[str, float]:
        if self.x_test is None or self.y_test is None:
            raise RuntimeError("Data must be prepared before evaluation.")
        predictions = self.model.predict(self.x_test)
        return {
            "mae": float(mean_absolute_error(self.y_test, predictions)),
            "rmse": float(root_mean_squared_error(self.y_test, predictions)),
            "r2": float(r2_score(self.y_test, predictions)),
        }

    def feature_importances(self) -> dict[str, float]:
        return dict(zip(self.feature_columns, self.model.feature_importances_.tolist()))

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
            ]
        )

        regressor = CropYieldRegressor(data)
        regressor.prepare_data()
        regressor.train_model()

        metrics = regressor.evaluate_model()
        print("Regression metrics:", metrics)

        predictions = regressor.predict(regressor.x_test)
        print("Sample predictions:\n", predictions)

        print("Feature importances:", regressor.feature_importances())


if __name__ == "__main__":
    CropYieldRegressor.run()
