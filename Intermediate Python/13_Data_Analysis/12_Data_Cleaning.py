from __future__ import annotations

import pandas as pd


class ExperimentDataCleaner:
    """Implements a full cleaning pipeline for raw, inconsistently-entered lab data."""

    VALID_PH_RANGE: tuple[float, float] = (3.0, 9.0)

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data.copy()

    def normalize_column_names(self) -> pd.DataFrame:
        """Return data with lowercased, underscore-separated column names."""
        normalized = self.data.copy()
        normalized.columns = (
            normalized.columns.str.strip().str.lower().str.replace(" ", "_", regex=False)
        )
        return normalized

    def normalize_whitespace(self, frame: pd.DataFrame) -> pd.DataFrame:
        """Return data with leading/trailing whitespace stripped from string columns."""
        cleaned = frame.copy()
        string_cols = cleaned.select_dtypes(exclude="number").columns
        for col in string_cols:
            cleaned[col] = cleaned[col].str.strip()
        return cleaned

    def remove_duplicates(self, frame: pd.DataFrame) -> pd.DataFrame:
        """Return data with exact duplicate rows removed, keeping the first occurrence."""
        return frame.drop_duplicates(keep="first").reset_index(drop=True)

    def convert_dtypes(self, frame: pd.DataFrame) -> pd.DataFrame:
        """Return data with numeric columns coerced to proper dtypes."""
        converted = frame.copy()
        for col in ["height_cm", "biomass_g", "soil_ph"]:
            converted[col] = pd.to_numeric(converted[col], errors="coerce")
        return converted

    def normalize_categorical_values(self, frame: pd.DataFrame) -> pd.DataFrame:
        """Return data with treatment labels standardized to lowercase snake_case."""
        cleaned = frame.copy()
        cleaned["treatment"] = (
            cleaned["treatment"].str.strip().str.lower().str.replace(" ", "_", regex=False)
        )
        return cleaned

    def enforce_valid_ranges(self, frame: pd.DataFrame) -> pd.DataFrame:
        """Return data with out-of-range soil_ph values set to missing for review."""
        validated = frame.copy()
        low, high = self.VALID_PH_RANGE
        out_of_range = ~validated["soil_ph"].between(low, high)
        validated.loc[out_of_range, "soil_ph"] = pd.NA
        return validated

    def handle_missing_values(self, frame: pd.DataFrame) -> pd.DataFrame:
        """Return data with missing numeric measurements imputed by column median."""
        filled = frame.copy()
        for col in ["height_cm", "biomass_g", "soil_ph"]:
            filled[col] = filled[col].fillna(filled[col].median())
        return filled

    def run_pipeline(self) -> pd.DataFrame:
        """Execute the full cleaning pipeline in the correct order and return clean data."""
        result = self.normalize_column_names()
        result = self.normalize_whitespace(result)
        result = self.remove_duplicates(result)
        result = self.convert_dtypes(result)
        result = self.normalize_categorical_values(result)
        result = self.enforce_valid_ranges(result)
        result = self.handle_missing_values(result)
        return result

    @staticmethod
    def run() -> None:
        data = pd.DataFrame(
            [
                {"Sample_ID ": " S001", "Treatment": " Control ", "height_cm": "22.1", "biomass_g": "4.0", "soil_ph": "6.2"},
                {"Sample_ID ": " S002", "Treatment": "Nitrogen High", "height_cm": "30.4", "biomass_g": "abc", "soil_ph": "6.4"},
                {"Sample_ID ": "S002", "Treatment": "Nitrogen High", "height_cm": "30.4", "biomass_g": "abc", "soil_ph": "6.4"},
                {"Sample_ID ": " S003", "Treatment": " Drought_Stress", "height_cm": "15.9", "biomass_g": "2.1", "soil_ph": "14.2"},
                {"Sample_ID ": " S004", "Treatment": "control", "height_cm": None, "biomass_g": "5.5", "soil_ph": "6.0"},
            ]
        )

        cleaner = ExperimentDataCleaner(data)
        clean_data = cleaner.run_pipeline()

        print(clean_data)
        print(clean_data.dtypes)


if __name__ == "__main__":
    ExperimentDataCleaner.run()
