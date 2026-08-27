"""sorted(): ascending/descending ordering of biological measurements and records."""


class UniversitySorted:
    def __init__(self, plant_heights_cm: list[float]) -> None:
        self.plant_heights_cm = plant_heights_cm

    def ascending(self) -> list[float]:
        return sorted(self.plant_heights_cm)

    def descending(self) -> list[float]:
        return sorted(self.plant_heights_cm, reverse=True)

    @staticmethod
    def run() -> None:
        heights_cm = [31.2, 18.0, 42.8, 25.5]

        processor = UniversitySorted(heights_cm)
        print(f"Original heights: {heights_cm}")
        print(f"Ascending: {processor.ascending()}")
        print(f"Descending: {processor.descending()}")
        print(f"Original list unchanged: {heights_cm}")


class InterviewSorted:
    def __init__(self, samples: list[dict]) -> None:
        self.samples = samples

    def sort_by_height(self) -> list[dict]:
        """Sorts structured records; missing heights are treated as lowest."""
        return sorted(self.samples, key=lambda sample: sample.get("height_cm") or 0.0)

    def sort_by_species_then_height(self) -> list[dict]:
        """Sorts by multiple attributes: species first, then height descending."""
        return sorted(
            self.samples,
            key=lambda sample: (sample.get("species", ""), -(sample.get("height_cm") or 0.0)),
        )

    @staticmethod
    def run() -> None:
        empty_samples: list[dict] = []
        processor = InterviewSorted(empty_samples)
        print(f"Empty samples -> sorted: {processor.sort_by_height()}")

        samples = [
            {"id": "P001", "species": "Rice", "height_cm": 31.2},
            {"id": "P002", "species": "Wheat", "height_cm": None},
            {"id": "P003", "species": "Rice", "height_cm": 24.0},
            {"id": "P004", "species": "Wheat", "height_cm": 28.5},
        ]
        processor = InterviewSorted(samples)
        print(f"Sorted by height (missing -> lowest): {processor.sort_by_height()}")
        print(f"Sorted by species then height desc: {processor.sort_by_species_then_height()}")


class IndustrySorted:
    def __init__(self, experiment_data: list[dict]) -> None:
        self.data = experiment_data

    def rank_samples(self) -> list[dict]:
        return sorted(
            self.data,
            key=lambda sample: sample.get("expression_level", 0.0),
            reverse=True,
        )

    def process(self) -> dict[str, object]:
        ranked = self.rank_samples()
        return {
            "total_samples": len(self.data),
            "ranked_samples": ranked,
            "top_sample_id": ranked[0]["sample_id"] if ranked else None,
        }

    @staticmethod
    def run() -> None:
        experiment_data = [
            {"sample_id": "RNA001", "gene": "GA20ox", "expression_level": 12.4},
            {"sample_id": "RNA002", "gene": "GA20ox", "expression_level": 8.7},
            {"sample_id": "RNA003", "gene": "GA20ox", "expression_level": 18.2},
        ]

        processor = IndustrySorted(experiment_data)
        report = processor.process()
        print(f"Experiment report: {report}")


if __name__ == "__main__":
    UniversitySorted.run()
    InterviewSorted.run()
    IndustrySorted.run()
