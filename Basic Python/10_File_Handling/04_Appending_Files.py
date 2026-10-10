"""
TOPIC: Appending Files

MAIN POINTS
- Use open(file_path, "a") to append data to a file.
- The "a" mode adds new content to the end of an existing file.
- Existing content is preserved.
- If the file does not exist, append mode creates it.
- Use \n when adding a new line or record.
- Appending is useful for maintaining laboratory logs and recording successive experimental observations.
"""

# Create an initial laboratory log.
with open("lab_observations.txt", "w") as file:
    file.write("Day 1: Bacterial culture initiated.\n")

# Append new observations without deleting the previous entry.
with open("lab_observations.txt", "a") as file:
    file.write("Day 2: Culture turbidity increased.\n")
    file.write("Day 3: Optical density measured at 0.85.\n")
    file.write("Day 4: Samples collected for analysis.\n")

# Read the complete laboratory log.
with open("lab_observations.txt", "r") as file:
    print(file.read())