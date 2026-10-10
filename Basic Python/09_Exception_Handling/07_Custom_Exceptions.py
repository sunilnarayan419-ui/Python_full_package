
"""
TOPIC: Custom Exceptions

MAIN POINTS
- Custom exceptions represent application-specific problems.
- Define them by creating a class that inherits from Exception.
- Raise them using raise and handle them using except.
- They make scientific applications easier to understand.
- Use descriptive names, commonly ending in Error.
"""

class InvalidDNASequenceError(Exception):
    """Raised when a DNA sequence contains invalid characters."""


def validate_dna(sequence):
    valid_bases = {"A", "T", "G", "C"}

    if not isinstance(sequence, str):
        raise TypeError("DNA sequence must be a string.")

    sequence = sequence.upper()

    invalid_bases = set(sequence) - valid_bases

    if invalid_bases:
        raise InvalidDNASequenceError(
            f"Invalid DNA characters: {invalid_bases}"
        )

    return sequence


try:
    dna = validate_dna("ATGXC")
    print("Valid DNA sequence:", dna)

except InvalidDNASequenceError as error:
    print("DNA validation failed:", error)

except TypeError as error:
    print("Input type error:", error)
