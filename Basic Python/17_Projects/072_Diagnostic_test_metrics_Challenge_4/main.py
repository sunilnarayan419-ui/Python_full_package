"""Runnable educational project. See README.md for the problem statement."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from project_engine import run

PROJECT_TITLE = 'Diagnostic test metrics — Challenge 4'
ALGORITHM = 'diagnostics'
SAMPLE_INPUT = {'TP': 90, 'FN': 10, 'TN': 90, 'FP': 10}

if __name__ == "__main__":
    print(PROJECT_TITLE)
    run(ALGORITHM, SAMPLE_INPUT)
