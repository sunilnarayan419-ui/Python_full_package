"""
06_Comments.py
==============
This file demonstrates Python comments and best practices for documentation.
"""

def example_function():
    """Example function with a proper docstring.

    This function simply prints a message.
    It showcases how to write a multi‑line docstring correctly.
    """
    print("Function executed")

# Single‑line comments (use #)
example_var = 42  # This is an inline comment

# Functions with comments
# We comment the next few lines to describe them.
def calculate_area(radius):
    """Calculate the area of a circle.

    Args:
        radius (float): The radius of the circle.

    Returns:
        float: The area of the circle.
    """
    return 3.14159 * radius * radius

# Demonstrate comments in action
example_function()
area = calculate_area(5)
print(f"The area of the circle is: {area}")

# Comments should explain *why*, not *what*
# Good: # Use float division to avoid integer truncation
# Bad:  # Multiply the two numbers

print("All comment examples completed.")