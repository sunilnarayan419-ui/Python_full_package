"""Loads raw RNA-seq expression matrices from disk.

Import ordering (enforced by isort, `profile = "black"`):
stdlib -> third-party -> first-party -> local, each group alphabetized.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from data_ingest.internal.validation import validate_sample_ids


@dataclass(frozen=True, slots=True)
class ExpressionMatrix:
    gene_ids: tuple[str, ...]
    sample_ids: tuple[str, ...]
    values: np.ndarray


def load_expression_matrix(path: Path) -> ExpressionMatrix:
    frame = pd.read_csv(path, index_col=0)
    validate_sample_ids(tuple(frame.columns))
    return ExpressionMatrix(
        gene_ids=tuple(frame.index),
        sample_ids=tuple(frame.columns),
        values=frame.to_numpy(dtype=np.float64),
    )


def load_sample_manifest(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))
