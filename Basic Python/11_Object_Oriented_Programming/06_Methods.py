"""
TOPIC: Methods

MAIN POINTS
- Methods are functions defined inside a class.
- Instance methods receive self as their first parameter.
- Instance methods can read and modify instance attributes.
- Class methods use @classmethod and receive cls as their first parameter.
- Static methods use @staticmethod when the operation does not require instance or class state.
- Methods can model biological operations, calculations, validations, and state changes.
- Keep each method focused on a clear responsibility.
"""

class BiologicalSample:
    """Represent a biological sample and its basic analysis."""

    laboratory_name = "Molecular Biology Laboratory"
    total_samples_created = 0

    def __init__(
        self,
        sample_id,
        organism,
        tissue,
        dna_concentration,
        purity_ratio
    ):
        self.sample_id = sample_id
        self.organism = organism
        self.tissue = tissue
        self.dna_concentration = dna_concentration
        self.purity_ratio = purity_ratio

        BiologicalSample.total_samples_created += 1

    # Instance method: accesses the current object's attributes.
    def calculate_dna_mass(self, volume_microliters):
        if volume_microliters < 0:
            raise ValueError("Volume cannot be negative.")

        return self.dna_concentration * volume_microliters

    # Instance method: evaluates the sample's purity ratio.
    def evaluate_purity(self):
        if 1.8 <= self.purity_ratio <= 2.0:
            return "Within the illustrative DNA purity range"

        return "Outside the illustrative DNA purity range"

    # Instance method: modifies object state.
    def update_concentration(self, new_concentration):
        if new_concentration < 0:
            raise ValueError("Concentration cannot be negative.")

        self.dna_concentration = new_concentration

    # Class method: accesses class-level information.
    @classmethod
    def get_total_samples(cls):
        return cls.total_samples_created

    # Alternative constructor.
    @classmethod
    def from_dictionary(cls, data):
        return cls(
            sample_id=data["sample_id"],
            organism=data["organism"],
            tissue=data["tissue"],
            dna_concentration=data["dna_concentration"],
            purity_ratio=data["purity_ratio"]
        )

    # Static method: performs a calculation independent of object state.
    @staticmethod
    def calculate_dilution_volume(
        initial_concentration,
        target_concentration,
        final_volume
    ):
        if initial_concentration <= 0:
            raise ValueError("Initial concentration must be positive.")

        if not 0 < target_concentration <= initial_concentration:
            raise ValueError("Target concentration must be positive and no greater than the initial concentration.")

        if final_volume < 0:
            raise ValueError("Final volume cannot be negative.")

        # C1V1 = C2V2
        return (
            target_concentration * final_volume
        ) / initial_concentration


sample_1 = BiologicalSample(
    "DNA_001",
    "Homo sapiens",
    "Blood",
    40.0,
    1.85
)

print("DNA mass in 10 µL:", sample_1.calculate_dna_mass(10))
print("Purity assessment:", sample_1.evaluate_purity())

sample_1.update_concentration(45.0)
print("Updated concentration:", sample_1.dna_concentration)

print("Samples created:", BiologicalSample.get_total_samples())

# Create an object from structured data.
sample_data = {
    "sample_id": "DNA_002",
    "organism": "Mus musculus",
    "tissue": "Liver",
    "dna_concentration": 60.0,
    "purity_ratio": 1.92
}

sample_2 = BiologicalSample.from_dictionary(sample_data)

print("New sample ID:", sample_2.sample_id)

# Calculate a dilution independently of any particular sample.
stock_concentration = 100.0
target_concentration = 20.0
final_volume = 500.0

stock_volume = BiologicalSample.calculate_dilution_volume(
    stock_concentration,
    target_concentration,
    final_volume
)

diluent_volume = final_volume - stock_volume

print("Stock volume:", stock_volume, "µL")
print("Diluent volume:", diluent_volume, "µL")