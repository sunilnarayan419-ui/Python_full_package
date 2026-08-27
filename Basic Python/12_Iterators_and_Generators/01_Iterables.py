"""Iterables: lists, tuples, strings, dicts, and sets over biological data."""


class UniversityIterables:
    def __init__(self, plant_records: list[dict]) -> None:
        self.plant_records = plant_records

    def species_list(self) -> list[str]:
        return [record["species"] for record in self.plant_records]

    def species_tuple(self) -> tuple[str, ...]:
        return tuple(self.species_list())

    def unique_species_set(self) -> set[str]:
        return set(self.species_list())

    def concatenated_ids(self) -> str:
        sample_ids = (record["sample_id"] for record in self.plant_records)
        return "-".join(sample_ids)

    def iterate_dict_items(self) -> list[str]:
        summaries = []
        for record in self.plant_records:
            for key, value in record.items():
                summaries.append(f"{key}={value}")
        return summaries

    @staticmethod
    def run() -> None:
        data = [
            {"sample_id": "P001", "species": "Wheat", "height_cm": 28.5},
            {"sample_id": "P002", "species": "Rice", "height_cm": 31.2},
            {"sample_id": "P003", "species": "Wheat", "height_cm": 26.9},
        ]

        demo = UniversityIterables(data)
        print(f"Species as list: {demo.species_list()}")
        print(f"Species as tuple: {demo.species_tuple()}")
        print(f"Unique species (set): {demo.unique_species_set()}")
        print(f"Concatenated sample IDs: {demo.concatenated_ids()}")
        print("Iterating dict items of first record:")
        for entry in demo.iterate_dict_items()[:3]:
            print(f"  {entry}")


class InterviewIterables:
    def __init__(self, records: list[dict]) -> None:
        self.records = records

    def is_iterable(self, value: object) -> bool:
        try:
            iter(value)
            return True
        except TypeError:
            return False

    def safe_species_set(self) -> set[str]:
        if not self.records:
            return set()
        species = set()
        for record in self.records:
            value = record.get("species")
            if isinstance(value, str) and value.strip():
                species.add(value.strip())
        return species

    def flatten_gene_names(self, records: list[dict]) -> list[str]:
        """Handles records where 'genes' may be missing, a string, or a list."""
        flattened: list[str] = []
        for record in records:
            genes = record.get("genes")
            if genes is None:
                continue
            if isinstance(genes, str):
                flattened.append(genes)
            elif self.is_iterable(genes):
                flattened.extend(genes)
        return flattened

    @staticmethod
    def run() -> None:
        empty_case: list[dict] = []
        processor = InterviewIterables(empty_case)
        print(f"Empty records -> species set: {processor.safe_species_set()}")

        mixed_case = [
            {"species": "Maize", "genes": ["zmm4", "wus1"]},
            {"species": "  Sorghum  ", "genes": "sb_drought1"},
            {"species": None, "genes": None},
            {"height_cm": 40.1},
        ]
        processor = InterviewIterables(mixed_case)
        print(f"Mixed records -> species set: {processor.safe_species_set()}")
        print(f"Flattened gene names: {processor.flatten_gene_names(mixed_case)}")

        print(f"Is a string iterable? {processor.is_iterable('DNA')}")
        print(f"Is an int iterable? {processor.is_iterable(42)}")


class IndustryIterables:
    def __init__(self, experiment_data: list[dict]) -> None:
        self.data = experiment_data

    def build_species_index(self) -> dict[str, list[str]]:
        """Groups sample IDs by species using iterable protocol only."""
        index: dict[str, list[str]] = {}
        for record in self.data:
            species = record.get("species")
            sample_id = record.get("sample_id")
            if not species or not sample_id:
                continue
            index.setdefault(species, []).append(sample_id)
        return index

    def process(self) -> dict[str, object]:
        index = self.build_species_index()
        return {
            "total_samples": len(self.data),
            "unique_species": len(index),
            "species_index": index,
        }

    @staticmethod
    def run() -> None:
        sample_data = [
            {"sample_id": "P001", "species": "Wheat"},
            {"sample_id": "P002", "species": "Rice"},
            {"sample_id": "P003", "species": "Wheat"},
            {"sample_id": "P004", "species": "Barley"},
        ]

        processor = IndustryIterables(sample_data)
        report = processor.process()
        print(f"Experiment report: {report}")


if __name__ == "__main__":
    UniversityIterables.run()
    InterviewIterables.run()
    IndustryIterables.run()
