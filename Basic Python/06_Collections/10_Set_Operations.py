"""10_Set_Operations.py — Python set operations through plant science and genomics."""
from __future__ import annotations


class PlantSpeciesSetOperationsUniversity:
    """University level: simple set operations."""

    def __init__(self) -> None:
        self.set_a: set[str] = {"Wheat", "Rice", "Maize"}
        self.set_b: set[str] = {"Rice", "Barley", "Maize"}

    def demonstrate(self) -> None:
        print("University — Set operations:")
        print(f"  Union:        {self.set_a | self.set_b}")
        print(f"  Intersection: {self.set_a & self.set_b}")
        print(f"  Difference A-B: {self.set_a - self.set_b}")
        print(f"  Symmetric:    {self.set_a ^ self.set_b}")

    @staticmethod
    def run() -> None:
        demo = PlantSpeciesSetOperationsUniversity()
        demo.demonstrate()


class GeneSetComparatorInterview:
    """Interview level: compare two genomic datasets."""

    def __init__(self, set_a: set[str], set_b: set[str]) -> None:
        self.set_a = set_a
        self.set_b = set_b

    def shared_genes(self) -> set[str]:
        return self.set_a & self.set_b

    def unique_to_a(self) -> set[str]:
        return self.set_a - self.set_b

    def unique_to_either(self) -> set[str]:
        return self.set_a ^ self.set_b

    @staticmethod
    def run() -> None:
        control = {"AT1G01010", "AT1G01020", "AT1G01030", "AT1G01040"}
        treatment = {"AT1G01010", "AT1G01030", "AT1G01050", "AT1G01060"}
        demo = GeneSetComparatorInterview(control, treatment)
        print("Interview — Gene set comparison:")
        print(f"  Shared:       {sorted(demo.shared_genes())}")
        print(f"  Unique to control:   {sorted(demo.unique_to_a())}")
        print(f"  Unique to either:    {sorted(demo.unique_to_either())}")


class MultiConditionGeneAnalyzerIndustry:
    """Industry level: dataset-comparison component."""

    def __init__(self, conditions: dict[str, set[str]]) -> None:
        self.conditions = conditions

    def genes_in_all_conditions(self) -> set[str]:
        if not self.conditions:
            return set()
        return set.intersection(*self.conditions.values())

    def genes_unique_to(self, condition: str) -> set[str]:
        if condition not in self.conditions:
            raise ValueError(f"condition {condition} not found")
        others = set.union(*(v for k, v in self.conditions.items() if k != condition))
        return self.conditions[condition] - others

    @staticmethod
    def run() -> None:
        conditions = {
            "drought": {"AT1G01010", "AT1G01020", "AT1G01030"},
            "salt":    {"AT1G01010", "AT1G01030", "AT1G01040"},
            "heat":    {"AT1G01010", "AT1G01040", "AT1G01050"},
        }
        analyzer = MultiConditionGeneAnalyzerIndustry(conditions)
        print("Industry — Multi-condition gene analysis:")
        print(f"  Genes in all conditions: {sorted(analyzer.genes_in_all_conditions())}")
        print(f"  Unique to drought:       {sorted(analyzer.genes_unique_to('drought'))}")


if __name__ == "__main__":
    PlantSpeciesSetOperationsUniversity.run()
    print()
    GeneSetComparatorInterview.run()
    print()
    MultiConditionGeneAnalyzerIndustry.run()
