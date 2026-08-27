"""Demonstrations of the built-in ord() function using scientific text/symbols."""


class UniversityOrd:
    """Teach the fundamental behavior of ord() for character-to-code-point conversion."""

    def __init__(self, character: str) -> None:
        self.character = character

    def to_code_point(self) -> int:
        return ord(self.character)

    @staticmethod
    def run() -> None:
        processor = UniversityOrd(character="A")
        print(f"ord('A') -> {processor.to_code_point()} (DNA base placeholder example)")


class InterviewOrd:
    """Unicode processing with validation for single-character inputs."""

    @staticmethod
    def safe_ord(character: str) -> int | None:
        """Return the code point for a single character, or None if invalid."""
        if len(character) != 1:
            return None
        return ord(character)

    @staticmethod
    def code_points_for_sequence(dna_sequence: str) -> list[int]:
        return [ord(base) for base in dna_sequence]

    @staticmethod
    def run() -> None:
        valid_result = InterviewOrd.safe_ord("G")
        invalid_result = InterviewOrd.safe_ord("GG")  # more than one character
        empty_result = InterviewOrd.safe_ord("")

        print(f"Single character 'G': {valid_result}")
        print(f"Multi-character 'GG': {invalid_result}")
        print(f"Empty string: {empty_result}")

        print(f"Code points for 'ATCG': {InterviewOrd.code_points_for_sequence('ATCG')}")


class IndustryOrd:
    """Scientific-text encoding/validation utility built on ord() and chr()."""

    ALLOWED_DNA_BASES: frozenset[str] = frozenset("ATCG")

    def validate_and_encode(self, dna_sequence: str) -> list[int]:
        """Validate that a sequence contains only allowed bases, then encode it."""
        invalid_bases = {base for base in dna_sequence if base not in self.ALLOWED_DNA_BASES}
        if invalid_bases:
            raise ValueError(f"Invalid DNA base(s) found: {sorted(invalid_bases)}")

        return [ord(base) for base in dna_sequence]

    def decode(self, code_points: list[int]) -> str:
        """Round-trip check: ord() and chr() are inverses of one another."""
        return "".join(chr(code_point) for code_point in code_points)

    @staticmethod
    def run() -> None:
        codec = IndustryOrd()
        sequence = "ATCGGTA"

        encoded = codec.validate_and_encode(sequence)
        decoded = codec.decode(encoded)

        print(f"Original sequence: {sequence}")
        print(f"Encoded code points: {encoded}")
        print(f"Decoded sequence matches original: {decoded == sequence}")

        try:
            codec.validate_and_encode("ATXG")
        except ValueError as error:
            print(f"Validation error: {error}")


if __name__ == "__main__":
    UniversityOrd.run()
    InterviewOrd.run()
    IndustryOrd.run()
