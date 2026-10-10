
"""
13. nonlocal

Main points
- nonlocal refers to a variable in the nearest enclosing function scope.
- It is used inside a nested function.
- nonlocal allows reassignment of an enclosing function's variable.
- It does not refer to a module-level global variable.
- The name must already exist in an enclosing function scope.
- Closures using nonlocal can maintain state between function calls.
"""

# Example 1: Track processed samples using an enclosing scope.
def create_sample_counter():
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment


count_processed = create_sample_counter()

print("Processed:", count_processed())
print("Processed:", count_processed())
print("Processed:", count_processed())

# Example 2: Maintain a configurable threshold.
def create_threshold_controller(initial_threshold):
    threshold = initial_threshold

    def update_threshold(new_threshold=None):
        nonlocal threshold

        if new_threshold is not None:
            threshold = new_threshold

        return threshold

    return update_threshold


control_threshold = create_threshold_controller(10.0)

print("Initial threshold:", control_threshold())
print("Updated threshold:", control_threshold(15.0))
print("Current threshold:", control_threshold())

# Example 3: Separate controllers maintain separate state.
threshold_a = create_threshold_controller(5.0)
threshold_b = create_threshold_controller(20.0)

print("Threshold A:", threshold_a())
print("Threshold B:", threshold_b())

# nonlocal changes the enclosing variable, not a global variable.
