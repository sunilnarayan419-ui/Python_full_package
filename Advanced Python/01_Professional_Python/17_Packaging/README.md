# bioseqkit

Sequence validation and summarization utilities for bioinformatics
pipelines, packaged with a modern `src/` layout.

## Install

    pip install bioseqkit
    pip install "bioseqkit[cli]"   # adds the `bioseqkit` console script

## Usage

    from bioseqkit import summarize
    stats = summarize("ACGTACGT")

## Development

    pip install -e ".[dev]"
    pytest
    mypy
    ruff check src tests
