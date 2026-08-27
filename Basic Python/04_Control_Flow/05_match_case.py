"""match/case for biological classification."""


class NucleotideLabel:
    @staticmethod
    def label(base: str) -> str:
        match base.upper():
            case "A":
                return "Adenine"
            case "T":
                return "Thymine"
            case "G":
                return "Guanine"
            case "C":
                return "Cytosine"
            case _:
                return "Unknown"


class TissueTypeCheck:
    @staticmethod
    def is_focus(tissue: str) -> bool:
        match tissue.lower():
            case "leaf" | "root" | "stem":
                return True
            case _:
                return False


class SequencingStatus:
    @staticmethod
    def action(status: str, coverage: float) -> str:
        match (status.lower(), coverage):
            case ("pending", _):
                return "queue"
            case ("running", c) if c < 10.0:
                return "low_coverage"
            case ("running", _):
                return "in_progress"
            case ("complete", _):
                return "archive"
            case _:
                return "unknown"


if __name__ == "__main__":
    print(NucleotideLabel.label("A"))

    print(TissueTypeCheck.is_focus("leaf"))

    print(SequencingStatus.action("running", 5.0))
    print(SequencingStatus.action("complete", 30.0))
