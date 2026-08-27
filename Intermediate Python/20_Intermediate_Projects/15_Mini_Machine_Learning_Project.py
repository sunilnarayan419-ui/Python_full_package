from __future__ import annotations

import logging
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

RANDOM_STATE = 42
NUMERIC_FEATURES = ("leaf_lesion_percent", "humidity_percent", "temperature_c", "days_since_planting")
CATEGORICAL_FEATURES = ("species", "soil_type")
TARGET_COLUMN = "disease_present"


class DatasetValidationError(Exception):
    """Raised when the training dataset fails schema validation."""


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    accuracy: float
    precision: float
    recall: float
    f1: float
    confusion: tuple[tuple[int, int], ...]


class DatasetValidator:
    """Validates the raw dataset schema before it enters the ML pipeline."""

    def validate(self, df: pd.DataFrame) -> None:
        required = set(NUMERIC_FEATURES) | set(CATEGORICAL_FEATURES) | {TARGET_COLUMN}
        missing = required - set(df.columns)
        if missing:
            raise DatasetValidationError(f"Dataset missing required columns: {sorted(missing)}")
        if df[TARGET_COLUMN].nunique() < 2:
            raise DatasetValidationError("Target column must contain at least two classes.")


class PlantDiseaseClassifier:
    """End-to-end plant disease classification workflow using a scikit-learn pipeline."""

    def __init__(self) -> None:
        self._validator = DatasetValidator()
        self._pipeline = self._build_pipeline()
        self._is_fitted = False

    def _build_pipeline(self) -> Pipeline:
        preprocessor = ColumnTransformer(
            transformers=[
                ("numeric", StandardScaler(), list(NUMERIC_FEATURES)),
                ("categorical", OneHotEncoder(handle_unknown="ignore"), list(CATEGORICAL_FEATURES)),
            ]
        )
        classifier = RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE)
        return Pipeline(steps=[("preprocessor", preprocessor), ("classifier", classifier)])

    def fit(self, X_train: pd.DataFrame, y_train: pd.Series) -> None:
        self._pipeline.fit(X_train, y_train)
        self._is_fitted = True

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        if not self._is_fitted:
            raise RuntimeError("Model must be fitted before calling predict().")
        return self._pipeline.predict(X)

    def evaluate(self, X_test: pd.DataFrame, y_test: pd.Series) -> EvaluationResult:
        predictions = self.predict(X_test)
        cm = confusion_matrix(y_test, predictions)
        return EvaluationResult(
            accuracy=round(float(accuracy_score(y_test, predictions)), 4),
            precision=round(float(precision_score(y_test, predictions, zero_division=0)), 4),
            recall=round(float(recall_score(y_test, predictions, zero_division=0)), 4),
            f1=round(float(f1_score(y_test, predictions, zero_division=0)), 4),
            confusion=tuple(tuple(int(v) for v in row) for row in cm),
        )


class MlWorkflow:
    """Orchestrates dataset validation, splitting, training, and evaluation."""

    def __init__(self, validator: DatasetValidator | None = None) -> None:
        self._validator = validator or DatasetValidator()

    def run(self, df: pd.DataFrame) -> EvaluationResult:
        self._validator.validate(df)

        feature_columns = list(NUMERIC_FEATURES) + list(CATEGORICAL_FEATURES)
        X = df[feature_columns]
        y = df[TARGET_COLUMN]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, random_state=RANDOM_STATE, stratify=y
        )

        classifier = PlantDiseaseClassifier()
        classifier.fit(X_train, y_train)
        return classifier.evaluate(X_test, y_test)


def _build_sample_dataset() -> pd.DataFrame:
    """Builds a deterministic synthetic plant-disease dataset for demonstration."""
    rng = np.random.default_rng(RANDOM_STATE)
    n_samples = 400

    species = rng.choice(["Zea mays", "Glycine max", "Arabidopsis thaliana"], size=n_samples)
    soil_type = rng.choice(["loam", "clay", "sandy"], size=n_samples)
    humidity = rng.normal(65, 12, n_samples).clip(20, 100)
    temperature = rng.normal(24, 5, n_samples)
    days_since_planting = rng.integers(10, 120, n_samples)

    disease_score = (
        0.04 * humidity
        + 0.02 * (temperature - 20).clip(min=0)
        - 0.01 * days_since_planting
        + rng.normal(0, 1.5, n_samples)
    )
    disease_present = (disease_score > np.median(disease_score)).astype(int)
    leaf_lesion_percent = np.where(
        disease_present == 1,
        rng.normal(35, 10, n_samples).clip(0, 100),
        rng.normal(5, 4, n_samples).clip(0, 100),
    )

    return pd.DataFrame(
        {
            "species": species,
            "soil_type": soil_type,
            "leaf_lesion_percent": leaf_lesion_percent.round(2),
            "humidity_percent": humidity.round(2),
            "temperature_c": temperature.round(2),
            "days_since_planting": days_since_planting,
            "disease_present": disease_present,
        }
    )


def run() -> EvaluationResult:
    """Runs the full plant-disease classification workflow on synthetic data."""
    df = _build_sample_dataset()
    workflow = MlWorkflow()
    result = workflow.run(df)

    logger.info("Accuracy: %.4f", result.accuracy)
    logger.info("Precision: %.4f", result.precision)
    logger.info("Recall: %.4f", result.recall)
    logger.info("F1: %.4f", result.f1)
    logger.info("Confusion matrix: %s", result.confusion)

    return result


if __name__ == "__main__":
    run()
