"""The raise statement: raising, validating, chaining, and re-raising exceptions."""

from __future__ import annotations

from dataclasses import dataclass


class UniversityRaise:
    """Demonstrates raising built-in exceptions with meaningful messages."""

    @staticmethod
    def validate_plant_height(height_cm: float) -> float:
        if height_cm < 0:
            raise ValueError(f"Plant height cannot be negative: {height_cm}")
        if height_cm > 10000:
            raise ValueError(f"Plant height exceeds plausible range: {height_cm}")
        return height_cm

    @staticmethod
    def run() -> None:
        print("--- UniversityRaise ---")
        for candidate in (45.2, -3.0, 25000.0):
            try:
                validated = UniversityRaise.validate_plant_height(candidate)
                print(f"Accepted plant height: {validated} cm")
            except ValueError as exc:
                print(f"Rejected plant height: {exc}")


class InterviewRaise:
    """Demonstrates input validation and exception chaining in realistic scenarios."""

    VALID_BASES = frozenset("ACGU")

    @staticmethod
    def validate_rna_sequence(sequence: str) -> str:
        if not sequence:
            raise ValueError("RNA sequence cannot be empty")
        invalid_bases = set(sequence.upper()) - InterviewRaise.VALID_BASES
        if invalid_bases:
            raise ValueError(f"RNA sequence contains invalid bases: {sorted(invalid_bases)}")
        return sequence.upper()

    @staticmethod
    def load_configured_threshold(raw_config: dict[str, str]) -> float:
        try:
            return float(raw_config["expression_threshold"])
        except KeyError as exc:
            raise KeyError("Experiment configuration missing 'expression_threshold'") from exc
        except ValueError as exc:
            raise ValueError(
                f"Invalid expression_threshold value: {raw_config['expression_threshold']!r}"
            ) from exc

    @staticmethod
    def run() -> None:
        print("--- InterviewRaise ---")
        for sequence in ("ACGU", "ACGTX", ""):
            try:
                print(f"Valid RNA sequence: {InterviewRaise.validate_rna_sequence(sequence)}")
            except ValueError as exc:
                print(f"Invalid RNA sequence: {exc}")

        for config in ({"expression_threshold": "2.5"}, {}, {"expression_threshold": "high"}):
            try:
                threshold = InterviewRaise.load_configured_threshold(config)
                print(f"Loaded threshold: {threshold}")
            except (KeyError, ValueError) as exc:
                print(f"Configuration error: {exc}")


@dataclass(frozen=True)
class CompoundProperty:
    compound_id: str
    property_name: str
    value: float


class UnsupportedCompoundPropertyError(ValueError):
    """Raised when a requested compound property is not supported by the pipeline."""


class IndustryRaise:
    """Demonstrates deliberate API validation rather than incidental exception raising."""

    SUPPORTED_PROPERTIES = frozenset({"molecular_weight", "logP", "melting_point_c"})

    @staticmethod
    def build_compound_property(
        compound_id: str, property_name: str, raw_value: str
    ) -> CompoundProperty:
        if property_name not in IndustryRaise.SUPPORTED_PROPERTIES:
            raise UnsupportedCompoundPropertyError(
                f"Unsupported property {property_name!r} for compound {compound_id}"
            )
        try:
            value = float(raw_value)
        except ValueError as exc:
            raise ValueError(
                f"Non-numeric value for {property_name} on {compound_id}: {raw_value!r}"
            ) from exc
        return CompoundProperty(compound_id, property_name, value)

    @staticmethod
    def run() -> None:
        print("--- IndustryRaise ---")
        requests = [
            ("D001", "molecular_weight", "342.3"),
            ("D002", "boiling_point_c", "210.5"),
            ("D003", "logP", "not_numeric"),
        ]
        for compound_id, property_name, raw_value in requests:
            try:
                built = IndustryRaise.build_compound_property(
                    compound_id, property_name, raw_value
                )
                print(f"Built compound property: {built}")
            except UnsupportedCompoundPropertyError as exc:
                print(f"Rejected due to unsupported property: {exc}")
            except ValueError as exc:
                print(f"Rejected due to invalid value: {exc}")


if __name__ == "__main__":
    UniversityRaise.run()
    InterviewRaise.run()
    IndustryRaise.run()
