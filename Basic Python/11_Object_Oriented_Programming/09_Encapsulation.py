"""
TOPIC: Encapsulation

MAIN POINTS
- Encapsulation combines data and the methods that operate on that data.
- It helps protect an object's state from invalid changes.
- A single leading underscore indicates a non-public implementation detail by convention.
- Double-leading-underscore names trigger name mangling; they are not absolute security barriers.
- Properties allow attribute-style access with controlled validation.
- Public methods and properties define how other code should interact with an object.
- Encapsulation is especially useful when maintaining scientific data integrity.
"""

class BiologicalSample:
    """Manage sample information with controlled data access."""

    def __init__(
        self,
        sample_id,
        organism,
        dna_concentration,
        purity_ratio
    ):
        self.sample_id = sample_id
        self.organism = organism

        # Internal implementation details.
        self._dna_concentration = None
        self._purity_ratio = None

        # Validate values through the properties.
        self.dna_concentration = dna_concentration
        self.purity_ratio = purity_ratio

        # Name-mangled attribute for illustrative internal use.
        self.__record_status = "Registered"

    @property
    def dna_concentration(self):
        return self._dna_concentration

    @dna_concentration.setter
    def dna_concentration(self, value):
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise TypeError("DNA concentration must be numeric.")

        if value < 0:
            raise ValueError("DNA concentration cannot be negative.")

        self._dna_concentration = float(value)

    @property
    def purity_ratio(self):
        return self._purity_ratio

    @purity_ratio.setter
    def purity_ratio(self, value):
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise TypeError("Purity ratio must be numeric.")

        if value < 0:
            raise ValueError("Purity ratio cannot be negative.")

        self._purity_ratio = float(value)

    def get_record_status(self):
        return self.__record_status

    def update_record_status(self, new_status):
        allowed_statuses = {
            "Registered",
            "Analyzed",
            "Archived"
        }

        if new_status not in allowed_statuses:
            raise ValueError("Invalid record status.")

        self.__record_status = new_status

    def describe(self):
        print("Sample ID:", self.sample_id)
        print("Organism:", self.organism)
        print("DNA concentration:", self.dna_concentration)
        print("Purity ratio:", self.purity_ratio)
        print("Record status:", self.get_record_status())


sample = BiologicalSample(
    "DNA_001",
    "Homo sapiens",
    45.0,
    1.87
)

sample.describe()

print()

# Valid modification: the property validates the new value.
sample.dna_concentration = 52.0
print("Updated concentration:", sample.dna_concentration)

# Valid state transition.
sample.update_record_status("Analyzed")
print("Updated status:", sample.get_record_status())

# Uncomment to observe validation errors.
# sample.dna_concentration = -10
# sample.purity_ratio = "unknown"
# sample.update_record_status("Invalid")

# Python name mangling changes the internal attribute name.
print(sample.__dict__)

# Direct access using the original double-underscore name fails.
# print(sample.__record_status)

# Name mangling is not a security mechanism.
# Internal code can still be accessed through the mangled name.
print(sample._BiologicalSample__record_status)