"""
02_Objects.py

Concept: Objects
An object is a concrete instance of a class: it has its own identity and
its own state, even though it shares behavior with every other instance
of the same class. This file demonstrates that idea at three levels.
"""

from __future__ import annotations


# --------------------------------------------------------------------------- #
# University Level
# --------------------------------------------------------------------------- #
class UniversityObjects:
    """A simple plant object.

    Purpose: show that creating two objects from the same class produces
    two independent instances with independent state.
    """

    def __init__(self, species: str, leaf_count: int) -> None:
        self.species = species
        self.leaf_count = leaf_count

    def grow_leaf(self) -> None:
        self.leaf_count += 1

    @staticmethod
    def run() -> None:
        print("--- UniversityObjects ---")
        plant_a = UniversityObjects(species="Mentha", leaf_count=4)
        plant_b = UniversityObjects(species="Mentha", leaf_count=4)

        plant_a.grow_leaf()

        print(f"plant_a leaves: {plant_a.leaf_count}")
        print(f"plant_b leaves: {plant_b.leaf_count}")
        print(f"Same object? {plant_a is plant_b}")


# --------------------------------------------------------------------------- #
# Interview Level
# --------------------------------------------------------------------------- #
class InterviewObjects:
    """Manages multiple independent biological objects.

    Purpose: demonstrate tracking a set of objects by identity (id()) and
    performing per-object operations without mixing up their state.
    """

    def __init__(self) -> None:
        self._plants: dict[str, UniversityObjects] = {}

    def register(self, plant_id: str, plant: UniversityObjects) -> None:
        if plant_id in self._plants:
            raise ValueError(f"plant_id '{plant_id}' already registered")
        self._plants[plant_id] = plant

    def grow(self, plant_id: str) -> None:
        if plant_id not in self._plants:
            raise KeyError(f"unknown plant_id '{plant_id}'")
        self._plants[plant_id].grow_leaf()

    def report(self) -> dict[str, int]:
        return {pid: plant.leaf_count for pid, plant in self._plants.items()}

    @staticmethod
    def run() -> None:
        print("--- InterviewObjects ---")
        registry = InterviewObjects()
        registry.register("P1", UniversityObjects("Basilicum", 3))
        registry.register("P2", UniversityObjects("Basilicum", 5))

        registry.grow("P1")
        registry.grow("P1")

        print(registry.report())


# --------------------------------------------------------------------------- #
# Industry Level
# --------------------------------------------------------------------------- #
class IndustryObjects:
    """Demonstrates independent domain objects participating in a small
    scientific workflow (sample intake -> measurement -> summary).

    Purpose: show that in real software, objects are created, passed
    around, and combined without ever losing their individual identity
    or state.
    """

    def __init__(self, workflow_name: str) -> None:
        if not workflow_name.strip():
            raise ValueError("workflow_name cannot be empty")
        self._workflow_name = workflow_name
        self._measurements: list[_Measurement] = []

    def intake(self, sample_id: str, concentration_ng_ul: float) -> "_Measurement":
        measurement = _Measurement(sample_id=sample_id, concentration_ng_ul=concentration_ng_ul)
        self._measurements.append(measurement)
        return measurement

    def summary(self) -> dict[str, float]:
        if not self._measurements:
            return {"count": 0, "mean_concentration": 0.0}
        total = sum(m.concentration_ng_ul for m in self._measurements)
        return {
            "count": len(self._measurements),
            "mean_concentration": total / len(self._measurements),
        }

    @staticmethod
    def run() -> None:
        print("--- IndustryObjects ---")
        workflow = IndustryObjects(workflow_name="DNA Extraction QC")

        m1 = workflow.intake("S-01", 42.7)
        m2 = workflow.intake("S-02", 55.1)

        print(f"m1 is m2: {m1 is m2}")
        print(f"m1 sample: {m1.sample_id}, concentration: {m1.concentration_ng_ul}")
        print(workflow.summary())


class _Measurement:
    """Supporting domain object: a single concentration measurement."""

    def __init__(self, sample_id: str, concentration_ng_ul: float) -> None:
        if concentration_ng_ul < 0:
            raise ValueError("concentration_ng_ul cannot be negative")
        self.sample_id = sample_id
        self.concentration_ng_ul = concentration_ng_ul


if __name__ == "__main__":
    UniversityObjects.run()
    InterviewObjects.run()
    IndustryObjects.run()
