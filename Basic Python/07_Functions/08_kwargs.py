
"""
08. **kwargs

Main points
- **kwargs collects extra keyword arguments into a dictionary.
- The name kwargs is conventional; the double asterisk is what matters.
- Each keyword becomes a dictionary key, with its supplied value.
- It is useful for optional settings and flexible metadata.
- kwargs can be combined with ordinary parameters and *args.
- Unexpected keyword arguments should be handled deliberately.
"""

# Example 1: Create a flexible biological sample record.
def create_sample_record(sample_id, **metadata):
    record = {"sample_id": sample_id}
    record.update(metadata)
    return record


sample = create_sample_record(
    "S001",
    organism="Arabidopsis thaliana",
    tissue="leaf",
    temperature_celsius=25.0,
    treatment="control"
)

print("Sample record:", sample)

# Example 2: Inspect analysis settings.
def configure_analysis(**settings):
    for key, value in settings.items():
        print(f"{key}: {value}")


configure_analysis(
    normalization="TPM",
    minimum_read_count=10,
    remove_duplicates=True
)

# Example 3: Combine normal parameters, *args, and **kwargs.
def run_analysis(analysis_name, *datasets, **options):
    print("Analysis:", analysis_name)
    print("Datasets:", datasets)
    print("Options:", options)


run_analysis(
    "gene_expression",
    "control.csv",
    "treated.csv",
    normalization="TPM",
    log_transform=True
)

# Example 4: Unpack a dictionary into keyword arguments.
settings = {
    "normalization": "TPM",
    "log_transform": True
}

configure_analysis(**settings)

# These examples illustrate parameter collection, not a validated
# gene-expression analysis pipeline.
