"""
TOPIC: pathlib
MAIN POINTS:
- Represent filesystem paths using Path.
- Check whether files and directories exist.
- Create directories.
- Read and write files.
"""

from pathlib import Path

# Create a path object
data_directory = Path("bio_data")
sample_file = data_directory / "samples.txt"

print("Directory path:", data_directory)
print("File path:", sample_file)

# Create a directory if it does not exist
data_directory.mkdir(parents=True, exist_ok=True)

# Write sample data
sample_file.write_text(
    "Sample_A\nSample_B\nSample_C\n",
    encoding="utf-8"
)

# Check whether the file exists
print("File exists:", sample_file.exists())
print("Is a file:", sample_file.is_file())
print("File suffix:", sample_file.suffix)

# Read the contents
contents = sample_file.read_text(encoding="utf-8")
print(contents)

# Iterate through files in a directory
for path in data_directory.iterdir():
    print(path.name)

# Path objects work across Windows, Linux, and macOS.