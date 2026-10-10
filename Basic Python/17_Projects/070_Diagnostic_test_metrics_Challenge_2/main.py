"""Runnable educational project. See README.md for the problem statement."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from project_engine import run

PROJECT_TITLE = 'Diagnostic test metrics — Challenge 2'
ALGORITHM = 'diagnostics'
SAMPLE_INPUT = {'TP': 45, 'FN': 5, 'TN': 80, 'FP': 20}

if __name__ == "__main__":
    print(PROJECT_TITLE)
    run(ALGORITHM, SAMPLE_INPUT)
