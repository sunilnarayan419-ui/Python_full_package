
"""
14. isinstance() Function

Main points
- isinstance(object, classinfo) checks whether an object belongs
  to a specified type or one of its subclasses.
- It returns True or False.
- The second argument can be a type or a tuple of types.
- isinstance() is generally preferred over type() for type validation
  when subclasses should also be accepted.
- bool is a subclass of int, so isinstance(True, int) returns True.
- Type checks should be used when they help enforce meaningful
  requirements, not automatically for every variable.
"""

# Basic checks
count = 10
temperature = 25.5
organism = "Arabidopsis"

print(isinstance(count, int))
print(isinstance(temperature, float))
print(isinstance(organism, str))

# Check against multiple types
value = 25.5

print(isinstance(value, (int, float)))

# Boolean is a subclass of int
print(isinstance(True, int))
print(type(True) is int)

# Validate a sample count
sample_count = 15

if isinstance(sample_count, int):
    print("Sample count is an integer.")
else:
    print("Sample count is not an integer.")

# Note: bool is also an int subclass.
# Exclude bool explicitly when only genuine integers are allowed.
sample_count = True

if isinstance(sample_count, int) and not isinstance(sample_count, bool):
    print("Valid integer sample count.")
else:
    print("Expected an integer, not a boolean.")

# Check a collection
gene_expression = [2.1, 3.4, 1.8]

print(isinstance(gene_expression, list))
print(isinstance(gene_expression, (tuple, list)))
