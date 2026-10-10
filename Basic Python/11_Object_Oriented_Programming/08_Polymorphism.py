"""
TOPIC: Polymorphism

MAIN POINTS
- Polymorphism means that different objects can respond to the same operation in different ways.
- Method overriding allows subclasses to customize inherited behavior.
- Python supports duck typing: objects can be used according to the methods they provide.
- The same method call can produce different results depending on the object's class.
- Polymorphism reduces the need for repetitive type-checking conditions.
- It is useful when a biological pipeline processes different types of samples through a shared interface.
"""

class BiologicalSample:
    """Base class defining a shared sample interface."""

    def __init__(self, sample_id, organism):
        self.sample_id = sample_id
        self.organism = organism

    def analyze(self):
        return "Performing general biological sample analysis"


class DNA_Sample(BiologicalSample):
    """Specialized DNA analysis."""

    def analyze(self):
        return f"{self.sample_id}: Calculating DNA sequence statistics"


class RNA_Sample(BiologicalSample):
    """Specialized RNA analysis."""

    def analyze(self):
        return f"{self.sample_id}: Preparing gene expression measurements"


class Protein_Sample(BiologicalSample):
    """Specialized protein analysis."""

    def analyze(self):
        return f"{self.sample_id}: Calculating protein sequence statistics"


class Metabolite_Sample(BiologicalSample):
    """Specialized metabolomics analysis."""

    def analyze(self):
        return f"{self.sample_id}: Preparing metabolite abundance measurements"


# Store different object types in one collection.
samples = [
    DNA_Sample("DNA_001", "Homo sapiens"),
    RNA_Sample("RNA_001", "Homo sapiens"),
    Protein_Sample("PROT_001", "Mus musculus"),
    Metabolite_Sample("MET_001", "Arabidopsis thaliana")
]

# The same operation works for every sample.
for sample in samples:
    print(sample.analyze())


# Duck typing: this object does not inherit from BiologicalSample.
class CustomAnalysis:
    def analyze(self):
        return "Running a custom bioinformatics analysis"


custom_analysis = CustomAnalysis()

# It still works because it provides the required method.
analyses = samples + [custom_analysis]

print()
for analysis in analyses:
    print(analysis.analyze())