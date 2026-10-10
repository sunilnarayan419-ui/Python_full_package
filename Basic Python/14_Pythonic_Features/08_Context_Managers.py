"""
TOPIC: Context Managers

MAIN POINTS
- A context manager manages resources using the with statement.
- File objects are common context managers.
- The resource is cleaned up when the with block exits, including when an exception occurs.
- Context managers implement the __enter__() and __exit__() protocol.
- contextlib provides tools for creating and managing context managers.
- Context managers are useful for files, database connections, and other resources.
- Use them to make scientific data processing safer and easier to maintain.
"""

from pathlib import Path
from contextlib import contextmanager


# Example 1: Use a file context manager.
file_path = Path("gene_expression.txt")

with open(file_path, "w", encoding="utf-8") as file:
    file.write("BRCA1,24.6\n")
    file.write("TP53,18.2\n")
    file.write("EGFR,42.8\n")

# The file is automatically closed after the block.
print("File saved:", file_path.exists())


# Example 2: Read the file safely.
with open(file_path, "r", encoding="utf-8") as file:
    for line in file:
        gene, expression = line.strip().split(",")

        print(
            f"Gene: {gene}, "
            f"Expression: {float(expression)}"
        )


# Example 3: Inspect resource cleanup.
with open(file_path, "r", encoding="utf-8") as file:
    print("\nFirst line:", file.readline().strip())

print("Is file closed:", file.closed)


# Example 4: Create a custom context manager using a class.
class ExperimentSession:
    """Represent the start and end of an experiment session."""

    def __init__(self, experiment_name):
        self.experiment_name = experiment_name

    def __enter__(self):
        print(f"Starting experiment: {self.experiment_name}")
        return self

    def record_observation(self, observation):
        print("Observation:", observation)

    def __exit__(self, exception_type, exception_value, traceback):
        if exception_type is not None:
            print("Experiment ended with an error:", exception_value)
        else:
            print("Experiment completed successfully.")

        # False means exceptions are not suppressed.
        return False


with ExperimentSession("Gene Expression Analysis") as experiment:
    experiment.record_observation("BRCA1 expression measured.")
    experiment.record_observation("TP53 expression measured.")


# Example 5: Create a context manager using contextlib.
@contextmanager
def experiment_log(experiment_name):
    print(f"\nOpening log for: {experiment_name}")

    try:
        yield
    except Exception as error:
        print("Error during experiment:", error)
        raise
    finally:
        print("Closing experiment log.")


with experiment_log("DNA Sequence Analysis"):
    print("Calculating nucleotide composition.")
    print("Calculating GC percentage.")


# Example 6: Context managers still clean up after exceptions.
try:
    with experiment_log("Invalid Analysis"):
        print("Starting analysis.")
        raise ValueError("Invalid experimental measurement.")
except ValueError as error:
    print("Caught error outside context manager:", error)


# Example 7: Use a context manager for a DNA report.
report_path = Path("dna_report.txt")
dna_sequence = "ATGCGCGT"

with open(report_path, "w", encoding="utf-8") as report:
    report.write("DNA SEQUENCE REPORT\n")
    report.write(f"Sequence: {dna_sequence}\n")
    report.write(f"Length: {len(dna_sequence)}\n")

    gc_count = dna_sequence.count("G") + dna_sequence.count("C")
    gc_percentage = gc_count / len(dna_sequence) * 100

    report.write(f"GC percentage: {gc_percentage:.2f}%\n")

with open(report_path, "r", encoding="utf-8") as report:
    print("\nGenerated report:")
    print(report.read())