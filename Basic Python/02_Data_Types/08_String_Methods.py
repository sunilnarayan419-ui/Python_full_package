
"""
08. String Methods

Main points
- String methods perform operations on strings.
- upper() converts letters to uppercase.
- lower() converts letters to lowercase.
- strip() removes leading and trailing whitespace by default.
- replace() substitutes matching text.
- split() divides a string into a list.
- join() combines strings using a separator.
- find() returns the first matching index or -1.
- count() counts non-overlapping occurrences.
- String methods generally return new values because strings are immutable.
"""

organism = "  Arabidopsis Thaliana  "
sequence = "atgcgtaatg"

# Change case
print(organism.upper())
print(organism.lower())
print(organism.title())

# Remove surrounding whitespace
clean_name = organism.strip()
print("Clean name:", clean_name)

# Replace text
print(clean_name.replace("Thaliana", "plant"))

# Split a string
csv_line = "sample_01,25.5,7.4"
fields = csv_line.split(",")

print("Fields:", fields)

# Join strings
joined_text = " | ".join(fields)
print("Joined:", joined_text)

# Search and count
print("Index of 'g':", sequence.find("g"))
print("Count of 'a':", sequence.count("a"))

# Prefix and suffix checks
print("Starts with 'atg':", sequence.startswith("atg"))
print("Ends with 'atg':", sequence.endswith("atg"))

# Check string content
print("Is alphabetic:", "Python".isalpha())
print("Is numeric:", "12345".isdigit())

# Original string remains unchanged
print("Original organism:", organism)
