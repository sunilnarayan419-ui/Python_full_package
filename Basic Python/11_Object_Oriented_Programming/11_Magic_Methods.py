"""
TOPIC: Magic Methods

MAIN POINTS
- Magic methods are special methods whose names begin and end with double underscores.
- They are also called dunder methods.
- __init__() initializes an object.
- __str__() defines its human-readable string representation.
- __repr__() defines a developer-oriented representation.
- __len__() allows len(object) to work.
- __eq__() defines equality comparisons using ==.
- __add__() can define behavior for the + operator.
- Implement magic methods when their behavior is meaningful and intuitive for the object.
- Custom magic methods can make scientific objects easier to inspect and compare.
"""

class DNASequence:
    """Represent a validated DNA sequence."""

    VALID_BASES = {"A", "T", "G", "C"}

    def __init__(self, sequence, sequence_id="Unknown"):
        if not isinstance(sequence, str):
            raise TypeError("DNA sequence must be a string.")

        sequence = sequence.upper()

        if not sequence:
            raise ValueError("DNA sequence cannot be empty.")

        invalid_bases = set(sequence) - self.VALID_BASES

        if invalid_bases:
            raise ValueError(
                f"Invalid DNA characters: {invalid_bases}"
            )

        self.sequence = sequence
        self.sequence_id = sequence_id

    def __str__(self):
        return f"{self.sequence_id}: {self.sequence}"

    def __repr__(self):
        return (
            f"DNASequence(sequence={self.sequence!r}, "
            f"sequence_id={self.sequence_id!r})"
        )

    def __len__(self):
        return len(self.sequence)

    def __eq__(self, other):
        if not isinstance(other, DNASequence):
            return NotImplemented

        return self.sequence == other.sequence

    def __add__(self, other):
        if not isinstance(other, DNASequence):
            return NotImplemented

        # Concatenate two DNA sequences into a new object.
        return DNASequence(
            self.sequence + other.sequence,
            sequence_id=f"{self.sequence_id}+{other.sequence_id}"
        )

    def gc_percentage(self):
        gc_count = self.sequence.count("G") + self.sequence.count("C")
        return gc_count / len(self.sequence) * 100


dna_1 = DNASequence("ATGC", "Fragment_A")
dna_2 = DNASequence("CGTA", "Fragment_B")
dna_3 = DNASequence("ATGC", "Fragment_C")

# __str__() is used by print().
print(dna_1)

# __repr__() provides a developer-oriented representation.
print(repr(dna_1))

# __len__() enables len().
print("Sequence length:", len(dna_1))

# __eq__() enables equality comparisons.
print("DNA 1 equals DNA 2:", dna_1 == dna_2)
print("DNA 1 equals DNA 3:", dna_1 == dna_3)

# __add__() enables the + operator.
combined_sequence = dna_1 + dna_2

print("Combined sequence:", combined_sequence)
print("Combined length:", len(combined_sequence))

print("GC percentage:", dna_1.gc_percentage())