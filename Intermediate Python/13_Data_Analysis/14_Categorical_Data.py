from __future__ import annotations

import pandas as pd


class DiseaseSeverityCategorizer:
    """Manages categorical encoding of treatment and disease-severity fields."""

    SEVERITY_ORDER: list[str] = ["none", "mild", "moderate", "severe"]

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data.copy()

    def convert_treatment_to_category(self) -> pd.DataFrame:
        """Convert the treatment column to an unordered categorical dtype for memory efficiency."""
        converted = self.data.copy()
        converted["treatment"] = converted["treatment"].astype("category")
        return converted

    def convert_severity_to_ordered_category(self) -> pd.DataFrame:
        """Convert disease_severity into an ordered categorical dtype."""
        converted = self.data.copy()
        severity_dtype = pd.CategoricalDtype(categories=self.SEVERITY_ORDER, ordered=True)
        converted["disease_severity"] = converted["disease_severity"].astype(severity_dtype)
        return converted

    def rename_categories(self, frame: pd.DataFrame) -> pd.DataFrame:
        """Rename severity categories to standardized reporting labels."""
        renamed = frame.copy()
        renamed["disease_severity"] = renamed["disease_severity"].cat.rename_categories(
            {"none": "no_symptoms", "mild": "mild_symptoms", "moderate": "moderate_symptoms", "severe": "severe_symptoms"}
        )
        return renamed

    def add_new_category(self, frame: pd.DataFrame, new_category: str) -> pd.DataFrame:
        """Add a previously unused category (e.g. for future observations)."""
        updated = frame.copy()
        updated["disease_severity"] = updated["disease_severity"].cat.add_categories([new_category])
        return updated

    def remove_unused_categories(self, frame: pd.DataFrame) -> pd.DataFrame:
        """Remove categories that have no observations, reducing memory footprint."""
        trimmed = frame.copy()
        trimmed["disease_severity"] = trimmed["disease_severity"].cat.remove_unused_categories()
        return trimmed

    def reorder_categories(self, frame: pd.DataFrame, new_order: list[str]) -> pd.DataFrame:
        """Reorder categories to reflect a desired reporting sequence."""
        reordered = frame.copy()
        reordered["disease_severity"] = reordered["disease_severity"].cat.reorder_categories(
            new_order, ordered=True
        )
        return reordered

    def severity_above_moderate(self, frame: pd.DataFrame) -> pd.DataFrame:
        """Return records with severity greater than 'moderate_symptoms', relying on category order."""
        return frame[frame["disease_severity"] > "moderate_symptoms"]

    def memory_usage_comparison(self) -> pd.Series:
        """Compare memory usage of the treatment column before and after categorical conversion."""
        as_object = self.data["treatment"].astype("object").memory_usage(deep=True)
        as_category = self.data["treatment"].astype("category").memory_usage(deep=True)
        return pd.Series({"object_dtype_bytes": as_object, "category_dtype_bytes": as_category})

    @staticmethod
    def run() -> None:
        data = pd.DataFrame(
            [
                {"sample_id": "S001", "treatment": "control", "disease_severity": "none"},
                {"sample_id": "S002", "treatment": "nitrogen_high", "disease_severity": "mild"},
                {"sample_id": "S003", "treatment": "drought_stress", "disease_severity": "severe"},
                {"sample_id": "S004", "treatment": "drought_stress", "disease_severity": "moderate"},
                {"sample_id": "S005", "treatment": "control", "disease_severity": "mild"},
                {"sample_id": "S006", "treatment": "nitrogen_high", "disease_severity": "none"},
            ]
        )

        categorizer = DiseaseSeverityCategorizer(data)

        with_treatment_category = categorizer.convert_treatment_to_category()
        print(with_treatment_category.dtypes)

        with_severity = categorizer.convert_severity_to_ordered_category()
        renamed = categorizer.rename_categories(with_severity)
        with_new_category = categorizer.add_new_category(renamed, "critical")
        trimmed = categorizer.remove_unused_categories(with_new_category)
        reordered = categorizer.reorder_categories(
            trimmed,
            ["no_symptoms", "mild_symptoms", "moderate_symptoms", "severe_symptoms"],
        )

        print(reordered)
        print(categorizer.severity_above_moderate(reordered))
        print(categorizer.memory_usage_comparison())


if __name__ == "__main__":
    DiseaseSeverityCategorizer.run()
