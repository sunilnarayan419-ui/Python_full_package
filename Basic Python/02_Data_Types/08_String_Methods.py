"""Useful string methods for biological data."""


class StringMethodsUniversity:
    @staticmethod
    def clean(sequence: str) -> str:
        return sequence.strip().upper()


class StringMethodsInterview:
    def __init__(self, sequence: str) -> None:
        self.sequence = sequence

    def starts_with_atg(self) -> bool:
        return self.sequence.upper().startswith("ATG")

    def count_gc(self) -> int:
        return self.sequence.upper().count("G") + self.sequence.upper().count("C")


class StringMethodsIndustry:
    @staticmethod
    def is_valid_dna(sequence: str) -> bool:
        s = sequence.upper()
        return all(c in "ACGT" for c in s)

    @staticmethod
    def replace_u_with_t(rna: str) -> str:
        return rna.upper().replace("U", "T")


if __name__ == "__main__":
    print(StringMethodsUniversity.clean("  atgc  "))

    s = StringMethodsInterview("ATGCGCAT")
    print(s.starts_with_atg())
    print(s.count_gc())

    print(StringMethodsIndustry.is_valid_dna("ATGC"))
    print(StringMethodsIndustry.replace_u_with_t("AUGC"))
