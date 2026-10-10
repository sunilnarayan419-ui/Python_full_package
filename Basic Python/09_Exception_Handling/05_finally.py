
"""
TOPIC: finally

MAIN POINTS
- finally normally executes whether an exception occurs or not.
- It is useful for cleanup operations.
- It can run after try, except, or else.
- Examples include closing files or releasing resources.
- A finally block does not guarantee execution if the process is forcibly terminated.
"""

try:
    print("Starting biological data analysis.")

    cell_count = 500
    print("Cell count:", cell_count)

except Exception as error:
    print("Analysis failed:", error)

else:
    print("Analysis completed successfully.")

finally:
    print("Analysis procedure has ended.")
