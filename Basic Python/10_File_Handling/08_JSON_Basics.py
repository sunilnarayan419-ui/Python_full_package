"""File-handling curriculum: Python's built-in json module."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any


class UniversityJSONBasics:
    """Teaches basic serialization/deserialization using
    json.dumps()/json.loads() and json.dump()/json.load() with a plant
    sample record."""

    @staticmethod
    def run() -> None:
        demo_dir = Path(tempfile.mkdtemp(prefix="university_json_"))
        json_file = demo_dir / "plant_sample.json"

        plant_sample: dict[str, Any] = {
            "sample_id": "P001",
            "species": "Wheat",
            "height_cm": 28.5,
        }

        json_text = json.dumps(plant_sample)
        print(f"[University] json.dumps() output: {json_text}")

        parsed_back = json.loads(json_text)
        print(f"[University] json.loads() output: {parsed_back}")

        with open(json_file, mode="w", encoding="utf-8") as file_handle:
            json.dump(plant_sample, file_handle)

        with open(json_file, mode="r", encoding="utf-8") as file_handle:
            loaded_sample = json.load(file_handle)
        print(f"[University] Loaded from file: {loaded_sample}")

        json_file.unlink()
        demo_dir.rmdir()


class InterviewJSONBasics:
    """Handles nested biological records and basic validation using
    gene-expression experiment metadata."""

    @staticmethod
    def _validate_experiment_record(record: dict[str, Any]) -> bool:
        required_keys = {"experiment_id", "genes"}
        if not required_keys.issubset(record.keys()):
            return False
        if not isinstance(record["genes"], list):
            return False
        return all(
            isinstance(gene, dict) and "gene_id" in gene and "expression_level" in gene
            for gene in record["genes"]
        )

    @staticmethod
    def run() -> None:
        demo_dir = Path(tempfile.mkdtemp(prefix="interview_json_"))
        json_file = demo_dir / "experiment_metadata.json"

        experiment_record: dict[str, Any] = {
            "experiment_id": "EXP001",
            "genes": [
                {"gene_id": "BRCA1", "expression_level": 4.2},
                {"gene_id": "TP53", "expression_level": 7.8},
            ],
        }

        with open(json_file, mode="w", encoding="utf-8") as file_handle:
            json.dump(experiment_record, file_handle, indent=2)

        with open(json_file, mode="r", encoding="utf-8") as file_handle:
            loaded_record = json.load(file_handle)

        is_valid = InterviewJSONBasics._validate_experiment_record(loaded_record)
        print(f"[Interview] Loaded nested record: {loaded_record}")
        print(f"[Interview] Record is valid: {is_valid}")

        invalid_record = {"experiment_id": "EXP002", "genes": "not_a_list"}
        print(
            f"[Interview] Invalid record rejected: "
            f"{not InterviewJSONBasics._validate_experiment_record(invalid_record)}"
        )

        json_file.unlink()
        demo_dir.rmdir()


class IndustryJSONBasics:
    """A small configuration/report component demonstrating clean
    serialization, validation, explicit encoding, and safe file
    operations for computational experiment configuration."""

    _REQUIRED_FIELDS = ("experiment_id", "compound_id", "parameters")

    def __init__(self, config_path: Path) -> None:
        self._config_path = config_path

    def save_configuration(self, config: dict[str, Any]) -> None:
        missing_fields = [field for field in self._REQUIRED_FIELDS if field not in config]
        if missing_fields:
            raise ValueError(f"Missing required configuration fields: {missing_fields}")

        with open(self._config_path, mode="w", encoding="utf-8") as file_handle:
            json.dump(config, file_handle, indent=2, ensure_ascii=False)

    def load_configuration(self) -> dict[str, Any]:
        """Load and validate a saved configuration.

        Raises:
            FileNotFoundError: if the configuration file is missing.
            json.JSONDecodeError: if the file contains malformed JSON.
            ValueError: if required fields are missing after loading.
        """
        if not self._config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self._config_path}")

        with open(self._config_path, mode="r", encoding="utf-8") as file_handle:
            config = json.load(file_handle)

        missing_fields = [field for field in self._REQUIRED_FIELDS if field not in config]
        if missing_fields:
            raise ValueError(f"Loaded configuration missing fields: {missing_fields}")

        return config

    @staticmethod
    def run() -> None:
        demo_dir = Path(tempfile.mkdtemp(prefix="industry_json_"))
        config_path = demo_dir / "docking_experiment_config.json"
        manager = IndustryJSONBasics(config_path)

        configuration = {
            "experiment_id": "DOCK001",
            "compound_id": "CMP001",
            "parameters": {"exhaustiveness": 8, "num_modes": 9},
        }
        manager.save_configuration(configuration)

        loaded_configuration = manager.load_configuration()
        print(f"[Industry] Loaded validated configuration: {loaded_configuration}")

        print("[Industry] Rejecting configuration with missing fields:")
        try:
            manager.save_configuration({"experiment_id": "DOCK002"})
        except ValueError as error:
            print(f"Caught expected error: {error}")

        malformed_path = demo_dir / "malformed_config.json"
        malformed_path.write_text("{invalid json", encoding="utf-8")
        malformed_manager = IndustryJSONBasics(malformed_path)
        print("[Industry] Handling malformed JSON content:")
        try:
            malformed_manager.load_configuration()
        except json.JSONDecodeError as error:
            print(f"Caught expected error: {error}")

        config_path.unlink()
        malformed_path.unlink()
        demo_dir.rmdir()


if __name__ == "__main__":
    UniversityJSONBasics.run()
    InterviewJSONBasics.run()
    IndustryJSONBasics.run()
