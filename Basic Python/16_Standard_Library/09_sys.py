"""
TOPIC: sys
MAIN POINTS:
- Inspect command-line arguments.
- Check the Python version.
- Read interpreter information.
- Exit a program with a status code.
"""

import sys

print("Python version:", sys.version)
print("Python executable:", sys.executable)
print("Platform:", sys.platform)

# Command-line arguments
print("Arguments:", sys.argv)

# Example:
# python 09_sys.py Sample_A
#
# sys.argv[0] is the script name.
# sys.argv[1] would be "Sample_A" in the example above.

if len(sys.argv) > 1:
    sample_id = sys.argv[1]
    print("Processing sample:", sample_id)
else:
    print("No sample ID supplied.")

# Example of an exit status:
# sys.exit(0)   # successful completion
# sys.exit(1)   # indicates an error
#
# Keep these calls commented out so this tutorial continues.