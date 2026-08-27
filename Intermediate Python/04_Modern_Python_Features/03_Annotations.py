from __future__ import annotations

import inspect
from dataclasses import dataclass, fields


class UniversityAnnotations:
    """Show basic annotations on variables, parameters, and return
    values for a plant growth record."""

    species: str
    height_cm: float

    def __init__(self, species: str, height_cm: float) -> None:
        self.species = species
        self.height_cm = height_cm

    def grow(self, additional_cm: float) -> float:
        """Parameter and return annotations describe intent only;
        Python does not enforce them at runtime.

        Time: O(1)
        """
        self.height_cm += additional_cm
        return self.height_cm

    @staticmethod
    def run() -> None:
        plant = UniversityAnnotations("Fern", 10.0)
        new_height = plant.grow(2.5)
        print("University: new height ->", new_height)
        print("University: class __annotations__ ->", UniversityAnnotations.__annotations__)


class InterviewAnnotations:
    """Inspect annotations programmatically using __annotations__ and
    inspect.signature, over a lab-result processing function."""

    @staticmethod
    def process_result(sample_id: str, ph_level: float, is_valid: bool = True) -> dict[str, object]:
        """Time: O(1)."""
        return {"sample_id": sample_id, "ph_level": ph_level, "is_valid": is_valid}

    @staticmethod
    def describe_function_signature(func: object) -> dict[str, str]:
        """Extract parameter names and their annotated types as strings.

        Time: O(p) where p is the number of parameters
        """
        signature = inspect.signature(func)  # type: ignore[arg-type]
        described: dict[str, str] = {}
        for name, parameter in signature.parameters.items():
            annotation = parameter.annotation
            described[name] = annotation.__name__ if hasattr(annotation, "__name__") else str(annotation)
        return described

    @staticmethod
    def run() -> None:
        described = InterviewAnnotations.describe_function_signature(InterviewAnnotations.process_result)
        print("Interview: parameter annotations ->", described)
        print("Interview: function __annotations__ ->", InterviewAnnotations.process_result.__annotations__)

        result = InterviewAnnotations.process_result("S042", 7.1)
        print("Interview: processed result ->", result)


@dataclass(slots=True)
class AssayConfigSchema:
    """Field annotations here double as a lightweight schema definition
    that can be inspected at runtime - useful for building configuration
    validators, though the annotations themselves still perform no
    validation on their own; the validate() method below does that work.
    """

    assay_name: str
    temperature_celsius: float
    duration_minutes: int
    replicate_count: int = 3


class SchemaValidationError(ValueError):
    """Raised when a value does not match its declared annotation type."""


class IndustryAnnotations:
    """Use dataclass field annotations as inspectable schema metadata
    for a scientific assay configuration system, with explicit runtime
    validation performed separately from the annotations themselves.
    """

    @staticmethod
    def schema_field_types() -> dict[str, type]:
        """Extract the declared type for every schema field.

        Time: O(f) where f is the number of fields
        """
        return {field.name: field.type for field in fields(AssayConfigSchema)}  # type: ignore[misc]

    @staticmethod
    def validate(config: AssayConfigSchema) -> None:
        """Explicitly validate values against business rules - the
        annotations alone never guarantee these constraints.

        Time: O(1)
        Raises SchemaValidationError on an invalid configuration.
        """
        if config.temperature_celsius < -80 or config.temperature_celsius > 100:
            raise SchemaValidationError(
                f"temperature_celsius out of realistic lab range: {config.temperature_celsius}"
            )
        if config.duration_minutes <= 0:
            raise SchemaValidationError("duration_minutes must be positive")
        if config.replicate_count < 1:
            raise SchemaValidationError("replicate_count must be at least 1")

    @staticmethod
    def run() -> None:
        field_types = IndustryAnnotations.schema_field_types()
        print("Industry: schema field annotations ->", field_types)

        config = AssayConfigSchema(assay_name="ELISA", temperature_celsius=37.0, duration_minutes=90)
        IndustryAnnotations.validate(config)
        print("Industry: valid config accepted ->", config)

        try:
            bad_config = AssayConfigSchema(assay_name="ELISA", temperature_celsius=500.0, duration_minutes=90)
            IndustryAnnotations.validate(bad_config)
        except SchemaValidationError as error:
            print("Industry: validation caught ->", error)


if __name__ == "__main__":
    UniversityAnnotations.run()
    InterviewAnnotations.run()
    IndustryAnnotations.run()
