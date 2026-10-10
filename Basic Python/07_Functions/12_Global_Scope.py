
"""
12. Global Scope

Main points
- A global variable is defined at module level.
- Functions can read global variables without declaring them global.
- The global keyword allows a function to reassign a module-level name.
- Excessive global state makes programs harder to test and maintain.
- Passing values as parameters and returning results is usually preferable.
- A global declaration must appear before the relevant use or assignment
  of that name in the function.
"""

# Module-level configuration
DEFAULT_TEMPERATURE = 25.0
processed_samples = 0


def display_configuration():
    # Reading global names does not require the global keyword.
    print("Default temperature:", DEFAULT_TEMPERATURE)


def register_sample():
    global processed_samples
    processed_samples += 1


display_configuration()

register_sample()
register_sample()
register_sample()

print("Processed samples:", processed_samples)

# Prefer returning updated values when practical.
def increment_counter(counter):
    return counter + 1


counter = 0
counter = increment_counter(counter)
counter = increment_counter(counter)

print("Counter without global mutation:", counter)

# Constants are conventionally written in uppercase.
# Python does not enforce immutability for module-level constants.
