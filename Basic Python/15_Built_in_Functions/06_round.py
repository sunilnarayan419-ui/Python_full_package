"""
TOPIC: round()

MAIN POINTS
- round(number, ndigits) rounds a numeric value.
- ndigits specifies the number of decimal places.
- If ndigits is omitted, the result is rounded to an integer.
- Python uses round-half-to-even for exact halfway cases.
- Floating-point representation can affect apparent decimal results.
- Rounding is useful for displaying scientific measurements, but preserve raw values for calculations.
"""

# Example 1: Round a GC percentage.
dna_sequence = "ATGCGCGT"

gc_count = dna_sequence.count("G") + dna_sequence.count("C")
gc_percentage = gc_count / len(dna_sequence) * 100

print("Original GC percentage:", gc_percentage)
print("Rounded GC percentage:", round(gc_percentage, 2))

# Example 2: Round experimental measurements.
expression_values = [24.6789, 18.2345, 42.8765, 35.1234]

rounded_values = [
    round(value, 2)
    for value in expression_values
]

print("Rounded expression values:", rounded_values)

# Example 3: Compare rounding precision.
measurement = 3.1415926535

print(round(measurement))
print(round(measurement, 2))
print(round(measurement, 4))

# Example 4: Demonstrate halfway behavior.
print(round(2.5))
print(round(3.5))
print(round(2.675, 2))

# Example 5: Keep raw and display values separately.
raw_concentration = 42.56789
display_concentration = round(raw_concentration, 2)

print("Raw concentration:", raw_concentration)
print("Display concentration:", display_concentration)