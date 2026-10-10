"""
TOPIC: os
MAIN POINTS:
- Inspect the current working directory.
- List directory contents.
- Read environment variables.
- Work with operating-system paths.
"""

import os

# Current working directory
print("Current directory:", os.getcwd())

# List files and folders
print("Directory contents:", os.listdir("."))

# Create an environment variable for this process
os.environ["PROJECT_NAME"] = "BioinformaticsTutorial"

print("Project name:", os.getenv("PROJECT_NAME"))

# Read an environment variable with a default
data_directory = os.getenv("BIO_DATA_DIR", "data")
print("Data directory:", data_directory)

# Operating-system information
print("Operating system:", os.name)
print("Path separator:", os.sep)

# os.path.join builds paths using the correct separator.
file_path = os.path.join("data", "samples.csv")
print("Example path:", file_path)

# Avoid hardcoding secrets in source code.
# Use environment variables for configuration.