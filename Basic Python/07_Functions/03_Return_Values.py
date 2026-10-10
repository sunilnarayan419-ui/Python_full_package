
"""
03. Return Values

Main points
- return sends a result back to the caller and terminates that function call.
- The caller can store, print, or further process the returned result.
- A function can return numbers, strings, collections, or custom objects.
- A function can return multiple values, commonly packed into a tuple.
- A function without an explicit return statement returns None.
- print() displays a value; return makes the value available to the caller.
"""

# Example 1: Return a DNA sequence length.
def sequence_length(sequence):
    return len(sequence)


length = sequence_length("ATGCGT")
print("Sequence length:", length)

# Example 2: Return a GC percentage.
def gc_percentage(sequence):
    gc_count = sequence.count("G") + sequence.count("C")
    return gc_count / len(sequence) * 100


result = gc_percentage("ATGCGC")
print("GC percentage:", result)

# Example 3: Return multiple summary statistics.
def summarize_measurements(values):
    minimum = min(values)
    maximum = max(values)
    mean = sum(values) / len(values)

    return minimum, maximum, mean


measurements = [12.5, 14.0, 16.5, 11.0]

minimum, maximum, mean = summarize_measurements(measurements)

print("Minimum:", minimum)
print("Maximum:", maximum)
print("Mean:", mean)

# Example 4: Return a dictionary.
def analyze_sample(sample_id, measurements):
    return {
        "sample_id": sample_id,
        "count": len(measurements),
        "mean": sum(measurements) / len(measurements)
    }


summary = analyze_sample("S004", measurements)
print("Summary:", summary)

# Example 5: print() is not the same as return.
def display_message():
    print("Analysis completed.")


output = display_message()
print("Returned value:", output)  # None

# These examples assume non-empty numeric inputs where required.
