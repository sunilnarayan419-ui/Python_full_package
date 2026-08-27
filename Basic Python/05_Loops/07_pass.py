"""pass as a syntactic placeholder in scientific code."""


class FutureSample:
    def __init__(self, sample_id: str) -> None:
        self.sample_id = sample_id

    def process(self) -> None:
        pass


class PhenotypeClassifier:
    def __init__(self, category: str) -> None:
        self.category = category

    def describe(self) -> str:
        if self.category == "leaf":
            return "leaf tissue"
        elif self.category == "root":
            return "root tissue"
        else:
            pass
        return "unclassified"


class GeneAnnotationHook:
    def __init__(self, gene: str) -> None:
        self.gene = gene
        self.annotation: str | None = None

    def annotate(self) -> None:
        pass


if __name__ == "__main__":
    FutureSample("P1").process()
    print(PhenotypeClassifier("leaf").describe())
    print(PhenotypeClassifier("unknown").describe())
    GeneAnnotationHook("BRCA1").annotate()
