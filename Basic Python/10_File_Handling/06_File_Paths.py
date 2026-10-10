"""
TOPIC: File Paths

MAIN POINTS
- A file path specifies the location of a file on the computer.
- Absolute paths specify the full location of a file.
- Relative paths are interpreted from the current working directory.
- Use pathlib.Path to construct and inspect paths in a platform-independent way.
- Path.exists() checks whether a path exists.
- Path.is_file() checks whether the path refers to a file.
- File-path management is essential when organizing genomic datasets and analysis outputs.
"""

from pathlib import Path

# Create a project directory for a genomics analysis.
project_dir = Path("genomics_project")
data_dir = project_dir / "data"
results_dir = project_dir / "results"

# Create the directories if they do not exist.
data_dir.mkdir(parents=True, exist_ok=True)
results_dir.mkdir(parents=True, exist_ok=True)

# Construct a relative path to a DNA sequence file.
dna_file = data_dir / "sample_dna.txt"

# Write a sample DNA sequence.
dna_file.write_text("ATGCGTACGTAG", encoding="utf-8")

print("File path:", dna_file)
print("Absolute path:", dna_file.resolve())
print("File exists:", dna_file.exists())
print("Is a file:", dna_file.is_file())

# Read the DNA sequence using its Path object.
sequence = dna_file.read_text(encoding="utf-8").strip()

# Save a simple analysis result.
result_file = results_dir / "sequence_length.txt"
result_file.write_text(
    f"DNA sequence length: {len(sequence)} nucleotides\n",
    encoding="utf-8"
)

print(result_file.read_text(encoding="utf-8"))