
"""
TOPIC: raise

MAIN POINTS
- raise manually triggers an exception.
- Use it when input or a result violates a requirement.
- Choose an appropriate built-in exception type.
- You can raise exceptions with a descriptive message.
- raise can also re-raise the current exception inside an except block.
"""

def calculate_cell_density(cell_count, volume_ml):
    if cell_count < 0:
        raise ValueError("Cell count cannot be negative.")

    if volume_ml <= 0:
        raise ValueError("Volume must be greater than zero.")

    return cell_count / volume_ml


try:
    density = calculate_cell_density(
        cell_count=500,
        volume_ml=2
    )
    print("Cell density:", density, "cells/mL")

except ValueError as error:
    print("Invalid input:", error)
