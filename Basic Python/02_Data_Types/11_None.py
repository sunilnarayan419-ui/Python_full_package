
"""
11. None

Main points
- None is Python's singleton object representing the absence of a value.
- Its type is NoneType.
- None is different from 0, False, and an empty string.
- Use 'is None' to check whether a value is None.
- Functions without an explicit return value return None.
- None is commonly used for optional values and uninitialized results.
"""

# Assign None
result = None
sample_id = None

print("Result:", result)
print("Sample ID:", sample_id)
print("Type:", type(result))

# Correct way to check None
if result is None:
    print("No result is available.")

# None is different from other values
print(None == 0)
print(None == False)
print(None == "")

# Function without an explicit return
def display_message():
    print("Processing sample...")

returned_value = display_message()

print("Returned value:", returned_value)
print("Is None:", returned_value is None)

# Function that may return None
def find_sample(sample_ids, target):
    if target in sample_ids:
        return target

    return None


samples = ["S001", "S002", "S003"]
found = find_sample(samples, "S004")

if found is None:
    print("Sample not found.")
else:
    print("Found:", found)
