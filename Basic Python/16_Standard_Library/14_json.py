"""Demonstrates the json module for scientific metadata serialization."""

import json
import tempfile
from pathlib import Path


class UniversityJson:
    """Introduces converting between Python objects and JSON strings."""

    def __init__(self, metadata: dict[str, object]) -> None:
        self.metadata = metadata

    def to_json_string(self) -> str:
        return json.dumps(self.metadata, indent=2)

    def from_json_string(self, json_text: str) -> dict[str, object]:
        return json.loads(json_text)

    @staticmethod
    def run() -> None:
        metadata = {"sample_id": "PL-0042", "species": "Arabidopsis thaliana", "height_cm": 24.5}
        demo = UniversityJson(metadata)

        json_text = demo.to_json_string()
        print(f"Serialized metadata:\n{json_text}")

        restored = demo.from_json_string(json_text)
        print(f"Restored metadata: {restored}")


class InterviewJson:
    """Solves a JSON validation problem, handling malformed input defensively."""

    def parse_experiment_config(self, json_text: str) -> dict[str, object]:
        """Parse and validate a JSON experiment configuration string.

        Raises ValueError with a clear message for malformed JSON or a missing
        required field, rather than letting a raw JSONDecodeError or KeyError
        propagate to the caller.
        """
        try:
            config = json.loads(json_text)
        except json.JSONDecodeError as error:
            raise ValueError(f"Invalid JSON configuration: {error}") from error

        if "experiment_name" not in config:
            raise ValueError("Configuration missing required field 'experiment_name'.")

        return config

    @staticmethod
    def run() -> None:
        solver = InterviewJson()

        # Test case 1: valid configuration
        valid_json = '{"experiment_name": "drought_stress_trial", "replicates": 3}'
        print(solver.parse_experiment_config(valid_json))

        # Test case 2: edge case, malformed JSON
        try:
            solver.parse_experiment_config("{experiment_name: invalid}")
        except ValueError as error:
            print(f"Handled malformed JSON: {error}")

        # Test case 3: edge case, missing required field
        try:
            solver.parse_experiment_config('{"replicates": 3}')
        except ValueError as error:
            print(f"Handled missing field: {error}")


class IndustryJson:
    """Scientific metadata persistence utility with safe file-based JSON I/O."""

    def save_metadata(self, metadata: dict[str, object], file_path: Path) -> Path:
        """Persist metadata to a JSON file using UTF-8 encoding."""
        with file_path.open("w", encoding="utf-8") as handle:
            json.dump(metadata, handle, indent=2, sort_keys=True)
        return file_path

    def load_metadata(self, file_path: Path) -> dict[str, object]:
        """Load metadata from a JSON file, raising a clear error if missing or invalid."""
        if not file_path.exists():
            raise FileNotFoundError(f"Metadata file not found: {file_path}")

        with file_path.open("r", encoding="utf-8") as handle:
            try:
                return json.load(handle)
            except json.JSONDecodeError as error:
                raise ValueError(f"Corrupt metadata file '{file_path}': {error}") from error

    def to_serializable(self, record: dict[str, object]) -> dict[str, object]:
        """Convert non-JSON-native values (like sets) into JSON-safe equivalents."""
        safe_record: dict[str, object] = {}
        for key, value in record.items():
            if isinstance(value, set):
                safe_record[key] = sorted(value)
            else:
                safe_record[key] = value
        return safe_record

    @staticmethod
    def run() -> None:
        manager = IndustryJson()

        with tempfile.TemporaryDirectory() as tmp_dir:
            metadata_path = Path(tmp_dir) / "sample_metadata.json"

            raw_record = {
                "sample_id": "PL-0099",
                "detected_genes": {"BRCA1", "TP53"},
                "collection_date": "2026-06-01",
            }
            serializable = manager.to_serializable(raw_record)

            manager.save_metadata(serializable, metadata_path)
            print(f"Saved metadata to: {metadata_path.name}")

            loaded = manager.load_metadata(metadata_path)
            print(f"Loaded metadata: {loaded}")


if __name__ == "__main__":
    UniversityJson.run()
    InterviewJson.run()
    IndustryJson.run()
