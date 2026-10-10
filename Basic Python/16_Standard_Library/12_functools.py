"""
TOPIC: functools
MAIN POINTS:
- Apply reduce() to combine values.
- Cache expensive function results.
- Create specialized functions with partial().
- Build decorators with wraps().
"""

from functools import reduce, lru_cache, partial, wraps

# Reduce: combine all values into one
measurements = [2, 3, 4]

product = reduce(lambda x, y: x * y, measurements)
print("Product:", product)

# Cache repeated function calls
@lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2:
        return n

    return fibonacci(n - 1) + fibonacci(n - 2)

print("Fibonacci(10):", fibonacci(10))
print("Cache information:", fibonacci.cache_info())

# Partial: create a specialized function
def calculate_dilution(concentration, dilution_factor):
    return concentration / dilution_factor

dilute_by_ten = partial(
    calculate_dilution,
    dilution_factor=10
)

print("Diluted concentration:", dilute_by_ten(100))

# A simple decorator
def announce_call(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        print("Running:", function.__name__)
        return function(*args, **kwargs)

    return wrapper

@announce_call
def analyze_sample(sample_id):
    return f"Analysis completed for {sample_id}"

print(analyze_sample("EXP001"))