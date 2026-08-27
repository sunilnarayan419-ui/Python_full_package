"""Demonstrations of the built-in dir() function using biological data objects."""


class PlantSample:
    """A simple biological data object used for introspection examples."""

    def __init__(self, sample_id: str, height: float) -> None:
        self.sample_id = sample_id
        self.height = height

    def describe(self) -> str:
        return f"{self.sample_id} ({self.height} cm)"


class UniversityDir:
    """Teach the fundamental behavior of dir() for object inspection."""

    def __init__(self, plant_sample: PlantSample) -> None:
        self.plant_sample = plant_sample

    def public_attributes(self) -> list[str]:
        """dir() ordering is not guaranteed; sort for a stable, readable view."""
        return sorted(
            name for name in dir(self.plant_sample) if not name.startswith("_")
        )

    @staticmethod
    def run() -> None:
        sample = PlantSample(sample_id="P001", height=58.2)
        processor = UniversityDir(sample)
        print(f"Public attributes/methods: {processor.public_attributes()}")


class InterviewDir:
    """Practical introspection: distinguish data attributes from methods."""

    def __init__(self, obj: object) -> None:
        self.obj = obj

    def data_attribute_names(self) -> list[str]:
        """Return public names that are not callable (likely data fields)."""
        names = [name for name in dir(self.obj) if not name.startswith("_")]
        return sorted(name for name in names if not callable(getattr(self.obj, name)))

    def method_names(self) -> list[str]:
        names = [name for name in dir(self.obj) if not name.startswith("_")]
        return sorted(name for name in names if callable(getattr(self.obj, name)))

    @staticmethod
    def run() -> None:
        sample = PlantSample(sample_id="P002", height=61.4)
        analyzer = InterviewDir(sample)

        print(f"Data attributes: {analyzer.data_attribute_names()}")
        print(f"Methods: {analyzer.method_names()}")

        empty_object_analyzer = InterviewDir(object())
        print(f"Data attributes of plain object: {empty_object_analyzer.data_attribute_names()}")


class IndustryDir:
    """Controlled diagnostic utility for inspecting scientific data objects."""

    def __init__(self, exclude_private: bool = True) -> None:
        self.exclude_private = exclude_private

    def inspect(self, obj: object) -> dict[str, list[str]]:
        """Return a small, filtered introspection report for diagnostics.

        Avoids dumping the full built-in attribute list; focuses on the
        object's own public interface.
        """
        names = dir(obj)
        if self.exclude_private:
            names = [name for name in names if not name.startswith("_")]

        data_fields = sorted(name for name in names if not callable(getattr(obj, name)))
        methods = sorted(name for name in names if callable(getattr(obj, name)))

        return {"data_fields": data_fields, "methods": methods}

    @staticmethod
    def run() -> None:
        sample = PlantSample(sample_id="P003", height=49.9)
        inspector = IndustryDir()
        report = inspector.inspect(sample)

        print(f"Diagnostic report -> data fields: {report['data_fields']}")
        print(f"Diagnostic report -> methods: {report['methods']}")


if __name__ == "__main__":
    UniversityDir.run()
    InterviewDir.run()
    IndustryDir.run()
