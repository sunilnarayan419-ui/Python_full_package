"""
01_Classes.py

Concept: Classes
A class is a reusable blueprint that defines the attributes and behavior
shared by every object created from it. This file demonstrates the concept
at three levels of engineering maturity: University, Interview, Industry.
"""

from __future__ import annotations


# --------------------------------------------------------------------------- #
# University Level
# --------------------------------------------------------------------------- #
class UniversityClasses:
    """A minimal class representing a single plant sample.

    Purpose: show that a class defines attributes (data) and methods
    (behavior) that every object built from it will share.
    """

    species: str
    height_cm: float

    def __init__(self, species: str, height_cm: float) -> None:
        self.species = species
        self.height_cm = height_cm

    def describe(self) -> str:
        return f"{self.species} plant, height {self.height_cm:.1f} cm"

    @staticmethod
    def run() -> None:
        print("--- UniversityClasses ---")
        sample = UniversityClasses(species="Arabidopsis thaliana", height_cm=12.4)
        print(sample.describe())


# --------------------------------------------------------------------------- #
# Interview Level
# --------------------------------------------------------------------------- #
class InterviewClasses:
    """Models a small collection of biological samples with useful behavior.

    Purpose: demonstrate that a class can encapsulate a group of related
    objects and expose operations (aggregation, filtering) over them.
    """

    def __init__(self, lab_name: str) -> None:
        if not lab_name.strip():
            raise ValueError("lab_name cannot be empty")
        self.lab_name = lab_name
        self._samples: list[UniversityClasses] = []

    def add_sample(self, sample: UniversityClasses) -> None:
        self._samples.append(sample)

    def average_height(self) -> float:
        if not self._samples:
            return 0.0
        return sum(s.height_cm for s in self._samples) / len(self._samples)

    def tallest(self) -> UniversityClasses | None:
        if not self._samples:
            return None
        return max(self._samples, key=lambda s: s.height_cm)

    @staticmethod
    def run() -> None:
        print("--- InterviewClasses ---")
        lab = InterviewClasses(lab_name="Plant Genetics Lab")
        lab.add_sample(UniversityClasses("Oryza sativa", 34.2))
        lab.add_sample(UniversityClasses("Zea mays", 58.7))
        lab.add_sample(UniversityClasses("Oryza sativa", 29.9))
        print(f"Average height: {lab.average_height():.2f} cm")
        tallest = lab.tallest()
        if tallest is not None:
            print(f"Tallest sample: {tallest.describe()}")


# --------------------------------------------------------------------------- #
# Industry Level
# --------------------------------------------------------------------------- #
class IndustryClasses:
    """A maintainable domain object representing a single scientific
    measurement record.

    Purpose: show a class designed with a single, clear responsibility
    (holding and validating one experimental record), suitable for use
    inside a larger scientific data pipeline.
    """

    def __init__(
        self,
        sample_id: str,
        gene_symbol: str,
        expression_level: float,
    ) -> None:
        self._sample_id = self._validate_id(sample_id)
        self._gene_symbol = self._validate_gene_symbol(gene_symbol)
        self._expression_level = self._validate_expression(expression_level)

    @staticmethod
    def _validate_id(sample_id: str) -> str:
        if not sample_id.strip():
            raise ValueError("sample_id cannot be empty")
        return sample_id

    @staticmethod
    def _validate_gene_symbol(gene_symbol: str) -> str:
        if not gene_symbol.strip():
            raise ValueError("gene_symbol cannot be empty")
        return gene_symbol.upper()

    @staticmethod
    def _validate_expression(expression_level: float) -> float:
        if expression_level < 0:
            raise ValueError("expression_level cannot be negative")
        return expression_level

    @property
    def sample_id(self) -> str:
        return self._sample_id

    @property
    def gene_symbol(self) -> str:
        return self._gene_symbol

    @property
    def expression_level(self) -> float:
        return self._expression_level

    def as_record(self) -> dict[str, str | float]:
        return {
            "sample_id": self._sample_id,
            "gene_symbol": self._gene_symbol,
            "expression_level": self._expression_level,
        }

    @staticmethod
    def run() -> None:
        print("--- IndustryClasses ---")
        record = IndustryClasses(
            sample_id="S-0142", gene_symbol="brca1", expression_level=7.85
        )
        print(record.as_record())

        try:
            IndustryClasses(sample_id="S-0143", gene_symbol="TP53", expression_level=-1.0)
        except ValueError as error:
            print(f"Validation rejected invalid record: {error}")


if __name__ == "__main__":
    UniversityClasses.run()
    InterviewClasses.run()
    IndustryClasses.run()
