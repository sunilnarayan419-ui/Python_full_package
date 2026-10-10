
"""
06. String Indexing

Main points
- Indexing accesses an individual character in a string.
- Positive indexing starts at 0 from the left.
- Negative indexing starts at -1 from the right.
- String indexing returns a string containing one character.
- Accessing an out-of-range index raises IndexError.
- Strings are immutable.
"""

sequence = "ATGCGT"

# Positive indexing
print("First character:", sequence[0])
print("Second character:", sequence[1])
print("Fourth character:", sequence[3])

# Negative indexing
print("Last character:", sequence[-1])
print("Second-last character:", sequence[-2])

# Index positions
print("Sequence:", sequence)
print("Length:", len(sequence))

# Access the middle character
middle_index = len(sequence) // 2
print("Character at middle index:", sequence[middle_index])

# Iterate through indexed characters
for index in range(len(sequence)):
    print(index, sequence[index])

# Uncomment to observe IndexError:
# print(sequence[100])
