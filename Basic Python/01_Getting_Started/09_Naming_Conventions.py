"""
09. Naming Conventions
Main points
- Use descriptive names such as sample_count instead of sc.
- Variables and functions conventionally use snake_case.
- Classes conventionally use PascalCase.
- Constants conventionally use UPPER_SNAKE_CASE.
- Names cannot begin with a digit.
- Names cannot contain spaces or hyphens.
- Avoid using Python keywords as names.
- A leading underscore often signals an internal implementation detail by convention.
"""


# Variables: snake_case
student_name = "Sunil"
sample_count = 12

# Constants: UPPER_SNAKE_CASE
MAX_RETRY_COUNT = 3
DEFAULT_TEMPERATURE = 25.0

# Functions: snake_case
def calculate_total(samples, price_per_sample):
    return samples * price_per_sample


# Classes: PascalCase
class BiologicalSample:
    def __init__(self, sample_id):
        self.sample_id = sample_id


# A leading underscore conventionally indicates internal use.
_internal_note = "For internal use"

total_cost = calculate_total(12, 50)

sample = BiologicalSample("BIO001")

print("Student:", student_name)
print("Total cost:", total_cost)
print("Sample ID:", sample.sample_id)
print("Retry limit:", MAX_RETRY_COUNT)


# Valid vs invalid identifiers


# Valid identifiers
sample_name = "S001"
sample2 = "S002"
_sample_count = 5
sample_count_2026 = 20

# Invalid identifiers — uncomment to observe SyntaxError:
# 2sample = "S003"       # Begins with a digit
# sample-name = "S004"   # Contains a hyphen
# sample name = "S005"   # Contains a space
