from __future__ import annotations


class UniversityStaticMethods:
    """Demonstrates a @staticmethod utility that needs no instance state."""

    class UnitConverter:
        @staticmethod
        def celsius_to_fahrenheit(celsius: float) -> float:
            return celsius * 9 / 5 + 32

    @staticmethod
    def run() -> None:
        print(UniversityStaticMethods.UnitConverter.celsius_to_fahrenheit(25.0))


class InterviewStaticMethods:
    """Demonstrates static methods grouped in a class namespace for related
    scientific utility calculations, distinguishing them from instance and
    class methods that would need self or cls."""

    class LabMath:
        @staticmethod
        def molarity(moles: float, volume_liters: float) -> float:
            if volume_liters <= 0:
                raise ValueError("volume_liters must be positive")
            return moles / volume_liters

        @staticmethod
        def dilution_volume(c1: float, v1: float, c2: float) -> float:
            if c2 <= 0:
                raise ValueError("target concentration c2 must be positive")
            return (c1 * v1) / c2

        @staticmethod
        def is_valid_ph(value: float) -> bool:
            return 0.0 <= value <= 14.0

    @staticmethod
    def run() -> None:
        print(f"molarity={InterviewStaticMethods.LabMath.molarity(0.5, 2.0)}")
        print(f"dilution_volume={InterviewStaticMethods.LabMath.dilution_volume(10.0, 1.0, 2.0)}")
        print(f"is_valid_ph(7.4)={InterviewStaticMethods.LabMath.is_valid_ph(7.4)}")


class IndustryStaticMethods:
    """Demonstrates static methods as a stateless, testable utility layer
    within a domain class, clearly separated from the instance-level API
    that manages actual experiment state."""

    class GenomicsUtils:
        """Pure, side-effect-free helpers for sequence analysis. All methods
        are static because they depend only on their arguments."""

        _VALID_BASES = frozenset("ACGT")

        @staticmethod
        def gc_content(sequence: str) -> float:
            sequence = sequence.upper()
            if not sequence:
                raise ValueError("sequence must not be empty")
            invalid = set(sequence) - IndustryStaticMethods.GenomicsUtils._VALID_BASES
            if invalid:
                raise ValueError(f"sequence contains invalid bases: {sorted(invalid)}")
            gc_count = sequence.count("G") + sequence.count("C")
            return round(gc_count / len(sequence) * 100, 2)

        @staticmethod
        def reverse_complement(sequence: str) -> str:
            complement = {"A": "T", "T": "A", "G": "C", "C": "G"}
            sequence = sequence.upper()
            return "".join(complement[base] for base in reversed(sequence))

        @staticmethod
        def melting_temperature(sequence: str) -> float:
            """Approximates melting temperature using the Wallace rule,
            suitable for short primers (<14 bases)."""
            sequence = sequence.upper()
            a_t = sequence.count("A") + sequence.count("T")
            g_c = sequence.count("G") + sequence.count("C")
            return 2 * a_t + 4 * g_c

        @staticmethod
        def hamming_distance(seq_a: str, seq_b: str) -> int:
            if len(seq_a) != len(seq_b):
                raise ValueError("sequences must be the same length")
            return sum(1 for a, b in zip(seq_a, seq_b) if a != b)

    @staticmethod
    def run() -> None:
        sequence = "ATGCGCATGCTA"
        utils = IndustryStaticMethods.GenomicsUtils
        print(f"gc_content={utils.gc_content(sequence)}%")
        print(f"reverse_complement={utils.reverse_complement(sequence)}")
        print(f"melting_temperature={utils.melting_temperature(sequence)}")
        print(f"hamming_distance={utils.hamming_distance('ATGC', 'ATCC')}")

        try:
            utils.gc_content("ATGX")
        except ValueError as exc:
            print(f"caught expected error: {exc}")


if __name__ == "__main__":
    UniversityStaticMethods.run()
    InterviewStaticMethods.run()
    IndustryStaticMethods.run()
