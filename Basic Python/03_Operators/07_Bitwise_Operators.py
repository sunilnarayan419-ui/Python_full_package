
"""
07. Bitwise Operators

Main points
- Bitwise operators work on the binary representation of integers.
- & : Bitwise AND.
- | : Bitwise OR.
- ^ : Bitwise XOR.
- ~ : Bitwise NOT.
- << : Left shift.
- >> : Right shift.
- Bitwise operators are different from logical operators and, or, and not.
- They are useful for bit flags, compact status fields, and low-level computing.
- A simple integer can encode several independent Boolean flags.
"""

# Example 1: Binary representation of integer values
a = 12
b = 10

print("a in binary:", bin(a))
print("b in binary:", bin(b))

# Example 2: Bitwise operations
print("AND:", a & b)
print("OR:", a | b)
print("XOR:", a ^ b)
print("NOT:", ~a)

# Example 3: Bit shifts
print("Left shift:", a << 1)
print("Right shift:", a >> 1)

# Example 4: Represent sequencing pipeline states using flags.
# Each flag occupies a different bit.
RAW_DATA_IMPORTED = 1       # Binary: 001
QUALITY_CHECK_PASSED = 2    # Binary: 010
ALIGNMENT_COMPLETED = 4     # Binary: 100

pipeline_status = 0

# Turn flags on using bitwise OR.
pipeline_status |= RAW_DATA_IMPORTED
pipeline_status |= QUALITY_CHECK_PASSED

print("Pipeline status:", bin(pipeline_status))

# Check whether a particular flag is enabled.
has_raw_data = bool(pipeline_status & RAW_DATA_IMPORTED)
has_quality_check = bool(pipeline_status & QUALITY_CHECK_PASSED)
has_alignment = bool(pipeline_status & ALIGNMENT_COMPLETED)

print("Raw data imported:", has_raw_data)
print("QC passed:", has_quality_check)
print("Alignment completed:", has_alignment)

# Enable alignment completion.
pipeline_status |= ALIGNMENT_COMPLETED

# Turn off the quality-check flag using AND with a complemented mask.
pipeline_status &= ~QUALITY_CHECK_PASSED

print("Updated status:", bin(pipeline_status))
print(
    "QC flag still enabled:",
    bool(pipeline_status & QUALITY_CHECK_PASSED)
)
