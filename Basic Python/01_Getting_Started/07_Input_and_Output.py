"""
07. Input and Output
Main points
- input() reads user input and returns a string.
- print() displays information.
- Convert strings when numeric operations are required.
- int() converts suitable values to integers.
- float() converts suitable values to floating-point numbers.
- f-strings insert expressions into strings using {}.
"""


# Read text input
name = input("Enter your name: ")

# Convert numeric input into an integer
age = int(input("Enter your age: "))

# Convert numeric input into a floating-point number
height_cm = float(input("Enter your height in cm: "))

# Display output
print("Name:", name)
print("Age:", age)
print("Height:", height_cm, "cm")

# Use an f-string for formatted output
print(f"{name} is {age} years old.")

# Scientific example
sample_mass_mg = float(
    input("Enter sample mass in mg: ")
)

sample_mass_g = sample_mass_mg / 1000

print(f"Sample mass: {sample_mass_g:.4f} g")
