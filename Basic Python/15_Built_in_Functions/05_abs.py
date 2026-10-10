"""
TOPIC: abs()

MAIN POINTS
- abs() returns the absolute value of a number.
- Absolute value measures magnitude without a negative sign.
- It works with integers, floats, and compatible numeric objects.
- It is useful for calculating absolute differences between measurements.
- Absolute difference does not indicate the direction of a biological change.
"""

# Example 1: Absolute numerical difference.
control_expression = 25.0
treatment_expression = 18.0

difference = treatment_expression - control_expression

print("Signed difference:", difference)
print("Absolute difference:", abs(difference))

# Example 2: Compare experimental measurements.
control_values = [10.0, 20.0, 30.0]
treatment_values = [12.0, 17.0, 35.0]

for control, treatment in zip(
    control_values,
    treatment_values,
    strict=True
):
    signed_change = treatment - control

    print(
        f"Control={control}, "
        f"Treatment={treatment}, "
        f"Absolute difference={abs(signed_change)}"
    )

# Example 3: Calculate the absolute error of a prediction.
observed_expression = 42.8
predicted_expression = 40.5

absolute_error = abs(
    observed_expression - predicted_expression
)

print("Absolute prediction error:", absolute_error)

# Example 4: Absolute value of different numbers.
print(abs(-15))
print(abs(15))
print(abs(-3.75))

# Example 5: Check whether a measurement is close to a reference.
measured_pH = 7.35
reference_pH = 7.40
tolerance = 0.10

within_tolerance = abs(measured_pH - reference_pH) <= tolerance

print("Within tolerance:", within_tolerance)