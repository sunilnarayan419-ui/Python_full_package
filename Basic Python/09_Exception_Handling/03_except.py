
"""
TOPIC: except

MAIN POINTS
- except handles a matching exception raised inside try.
- Handle specific exception types whenever possible.
- Multiple except blocks can handle different exception types.
- The exception object can be stored using "as".
- Avoid catching every exception without a good reason.
"""

sample_data = {
    "sample_A": 250,
    "sample_B": 0
}

try:
    sample_name = "sample_B"
    concentration = 1000 / sample_data[sample_name]
    print("Concentration:", concentration)

except ZeroDivisionError:
    print("The sample value cannot be zero.")

except KeyError as error:
    print("Sample not found:", error)
