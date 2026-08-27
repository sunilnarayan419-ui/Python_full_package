class UniversityRecursion:
    def __init__(self, species: str) -> None:
        self.species = species

    def count_leaves(self, branch: dict) -> int:
        # Base case: a branch with no sub-branches contributes its own leaves.
        if not branch.get("sub_branches"):
            return branch.get("leaf_count", 0)

        # Recursive case: sum this branch's leaves plus every sub-branch's leaves.
        total = branch.get("leaf_count", 0)
        for sub_branch in branch["sub_branches"]:
            total += self.count_leaves(sub_branch)
        return total

    @staticmethod
    def run() -> None:
        plant_structure = {
            "leaf_count": 2,
            "sub_branches": [
                {"leaf_count": 3, "sub_branches": []},
                {
                    "leaf_count": 1,
                    "sub_branches": [
                        {"leaf_count": 4, "sub_branches": []},
                    ],
                },
            ],
        }
        tree = UniversityRecursion("Ficus benjamina")
        total_leaves = tree.count_leaves(plant_structure)
        print("University - total leaves:", total_leaves)


class InterviewRecursion:
    def __init__(self, sequence: str) -> None:
        self.sequence = sequence

    def is_palindromic_sequence(self, sequence: str | None = None) -> bool:
        if sequence is None:
            sequence = self.sequence

        # Base case: sequences of length 0 or 1 are trivially palindromic.
        if len(sequence) <= 1:
            return True

        # Base case: mismatched ends short-circuit the recursion.
        if sequence[0] != sequence[-1]:
            return False

        # Recursive case: strip both ends and check the remaining core.
        return self.is_palindromic_sequence(sequence[1:-1])

    @staticmethod
    def run() -> None:
        palindrome_checker = InterviewRecursion("GATTACATTAG")
        print(
            "Interview - is 'GATTACATTAG' palindromic:",
            palindrome_checker.is_palindromic_sequence(),
        )
        print(
            "Interview - is 'ATCG' palindromic:",
            palindrome_checker.is_palindromic_sequence("ATCG"),
        )
        print(
            "Interview - is '' palindromic:",
            palindrome_checker.is_palindromic_sequence(""),
        )


class IndustryRecursion:
    """Traverses a taxonomic classification tree using both recursive and
    iterative strategies, allowing comparison between the two approaches."""

    def __init__(self, root_taxon: dict) -> None:
        self.root_taxon = root_taxon

    def find_species_recursive(self, target_species: str, node: dict | None = None) -> list[str] | None:
        if node is None:
            node = self.root_taxon

        path = [node["name"]]

        # Base case: current node matches the target species.
        if node["name"] == target_species:
            return path

        # Recursive case: search each child and prepend the current node
        # to any path found beneath it.
        for child in node.get("children", []):
            found_path = self.find_species_recursive(target_species, child)
            if found_path is not None:
                return path + found_path

        return None

    def find_species_iterative(self, target_species: str) -> list[str] | None:
        stack: list[tuple[dict, list[str]]] = [(self.root_taxon, [])]
        while stack:
            node, ancestors = stack.pop()
            current_path = ancestors + [node["name"]]
            if node["name"] == target_species:
                return current_path
            for child in node.get("children", []):
                stack.append((child, current_path))
        return None

    @staticmethod
    def run() -> None:
        taxonomy = {
            "name": "Plantae",
            "children": [
                {
                    "name": "Angiosperms",
                    "children": [
                        {"name": "Zea mays", "children": []},
                        {"name": "Glycine max", "children": []},
                    ],
                },
                {
                    "name": "Gymnosperms",
                    "children": [
                        {"name": "Pinus sylvestris", "children": []},
                    ],
                },
            ],
        }
        classifier = IndustryRecursion(taxonomy)

        recursive_path = classifier.find_species_recursive("Glycine max")
        iterative_path = classifier.find_species_iterative("Glycine max")
        print("Industry - recursive path:", recursive_path)
        print("Industry - iterative path:", iterative_path)

        missing_path = classifier.find_species_recursive("Unknown species")
        print("Industry - missing species path:", missing_path)


if __name__ == "__main__":
    UniversityRecursion.run()
    InterviewRecursion.run()
    IndustryRecursion.run()
