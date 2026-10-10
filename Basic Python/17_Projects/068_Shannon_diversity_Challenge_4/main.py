"""Runnable educational project. See README.md for the problem statement."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from project_engine import run

PROJECT_TITLE = 'Shannon diversity — Challenge 4'
ALGORITHM = 'shannon'
SAMPLE_INPUT = {'A': 2, 'B': 4, 'C': 6, 'D': 8}

if __name__ == "__main__":
    print(PROJECT_TITLE)
    run(ALGORITHM, SAMPLE_INPUT)
