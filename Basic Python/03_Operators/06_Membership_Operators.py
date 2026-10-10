
"""
06. Membership Operators

Main points
- in checks whether an element belongs to a container.
- not in checks whether an element does not belong to a container.
- Membership works with strings, lists, tuples, sets, and dictionaries.
- For dictionaries, membership checks keys, not values.
- String membership checks whether a substring occurs within a string.
- Set membership is typically faster than list membership for large collections.
- Membership checks do not establish biological function or significance.
"""

# Example 1: Check whether a gene is in a gene panel
gene_panel = ["BRCA1", "TP53", "EGFR", "MYC"]

print("TP53 included:", "TP53" in gene_panel)
print("ALK included:", "ALK" in gene_panel)

# Example 2: Check for a DNA motif
dna_sequence = "ATGCGTACGATG"

print("Contains ATG:", "ATG" in dna_sequence)
print("Contains TTT:", "TTT" in dna_sequence)

# Example 3: Screen for contamination markers
detected_markers = {"marker_A", "marker_B", "marker_C"}

print("Marker A detected:", "marker_A" in detected_markers)
print("Marker D absent:", "marker_D" not in detected_markers)

# Example 4: Dictionary membership checks keys
sample = {
    "sample_id": "S001",
    "organism": "Arabidopsis thaliana",
    "temperature": 25.0
}

print("Has organism key:", "organism" in sample)
print("Has pH key:", "pH" in sample)

# To check dictionary values, use .values()
print("Organism recorded:", "Arabidopsis thaliana" in sample.values())

# Example 5: Check whether a sample is in a control group
control_samples = ("S001", "S002", "S003")

sample_id = "S002"

if sample_id in control_samples:
    print("Sample belongs to the control group.")
else:
    print("Sample is not in the control group.")
