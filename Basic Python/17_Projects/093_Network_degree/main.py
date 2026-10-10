"""Runnable educational project. See README.md for the problem statement."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from project_engine import run

PROJECT_TITLE = 'Network degree'
ALGORITHM = 'degree'
SAMPLE_INPUT = [['A', 'B'], ['A', 'C'], ['B', 'C'], ['C', 'A']]

if __name__ == "__main__":
    print(PROJECT_TITLE)
    run(ALGORITHM, SAMPLE_INPUT)
