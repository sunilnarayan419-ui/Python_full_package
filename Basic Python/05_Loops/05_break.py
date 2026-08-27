"""break for early termination in scientific search."""


class NucleotideSearch:
    def __init__(self, sequence: str, target: str) -> None:
        self.sequence = sequence.upper()
        self.target = target.upper()

    def first_index(self) -> int:
        for i, base in enumerate(self.sequence):
            if base == self.target:
                return i
        return -1


class GeneSearcher:
    def __init__(self, gene_names: list[str], target: str) -> None:
        self.gene_names = gene_names
        self.target = target

    def find(self) -> int:
        for i, name in enumerate(self.gene_names):
            if name == self.target:
                return i
        return -1


class QCFailureFinder:
    def __init__(self, qualities: list[float], min_quality: float) -> None:
        self.qualities = qualities
        self.min_quality = min_quality

    def first_failure(self) -> int:
        for i, q in enumerate(self.qualities):
            if q < self.min_quality:
                return i
        return -1


if __name__ == "__main__":
    print(NucleotideSearch("ATGCAT", "C").first_index())

    print(GeneSearcher(["BRCA1", "TP53", "EGFR"], "TP53").find())

    print(QCFailureFinder([35.0, 32.0, 25.0], 30.0).first_failure())
