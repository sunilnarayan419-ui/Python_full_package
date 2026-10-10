"""Runnable educational project. See README.md for the problem statement."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from project_engine import run

PROJECT_TITLE = 'Shannon diversity — Challenge 3'
ALGORITHM = 'shannon'
SAMPLE_INPUT = {'one': 100}

if __name__ == "__main__":
    print(PROJECT_TITLE)
    run(ALGORITHM, SAMPLE_INPUT)
