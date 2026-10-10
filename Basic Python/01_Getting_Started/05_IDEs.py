"""

05. IDEs
Main points
An Integrated Development Environment (IDE) or code editor provides tools for writing and running code.
- VS Code: Lightweight, extensible editor with Python support.
- PyCharm: Python-focused development environment.
- Jupyter Notebook: Interactive environment for code, explanations, and data analysis.
- IDLE: A basic Python editor and interactive shell included with standard Python installations.
Useful features include syntax highlighting, autocomplete, debugging, terminal integration, and project navigation.
Resources: VS Code · PyCharm · Jupyter

"""


# Use this program to practise common IDE features.

def calculate_average(values):
    """Return the arithmetic mean of a list of numbers."""
    if not values:
        return None

    return sum(values) / len(values)


measurements = [12.5, 13.0, 14.5, 12.0]

average = calculate_average(measurements)

print("Measurements:", measurements)
print("Average:", average)
