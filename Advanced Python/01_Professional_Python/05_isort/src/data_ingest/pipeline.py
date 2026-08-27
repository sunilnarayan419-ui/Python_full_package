"""End-to-end ingestion pipeline tying loaders together."""
from __future__ import annotations

from pathlib import Path

import numpy as np

from data_ingest.ingestion.loaders import ExpressionMatrix, load_expression_matrix


class IngestPipeline:
    def __init__(self, matrix_path: Path) -> None:
        self._matrix_path = matrix_path

    def run(self) -> ExpressionMatrix:
        matrix = load_expression_matrix(self._matrix_path)
        if np.isnan(matrix.values).any():
            raise ValueError("expression matrix contains NaN values")
        return matrix
