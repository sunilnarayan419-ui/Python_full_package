"""
TOPIC: shutil
MAIN POINTS:
- Copy files.
- Move files.
- Copy directory trees.
- Inspect disk usage.
"""

import shutil
from pathlib import Path

source_directory = Path("shutil_demo")
source_directory.mkdir(exist_ok=True)

source_file = source_directory / "experiment.txt"
copy_file = source_directory / "experiment_copy.txt"
renamed_file = source_directory / "experiment_renamed.txt"

# Create a demonstration file
source_file.write_text(
    "Experiment ID: EXP001\nResult: Positive\n",
    encoding="utf-8"
)

# Copy a file
shutil.copy2(source_file, copy_file)
print("Copied file:", copy_file)

# Move or rename a file
shutil.move(str(copy_file), str(renamed_file))
print("Moved file:", renamed_file)

# Inspect disk usage
usage = shutil.disk_usage(source_directory)

print("Total bytes:", usage.total)
print("Used bytes:", usage.used)
print("Free bytes:", usage.free)

# Directory copying example:
# shutil.copytree("source_folder", "destination_folder")
#
# Use copytree only when the source exists and the destination
# does not already exist, unless you intentionally configure
# its behavior for an existing destination.
#
# Be careful with file operations: moving or deleting files
# can change your filesystem.