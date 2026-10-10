"""Runnable educational project. See README.md for the problem statement."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from project_engine import run

PROJECT_TITLE = 'Exponential growth — Challenge 4'
ALGORITHM = 'exponential'
SAMPLE_INPUT = [200, 0.1, 15]

if __name__ == "__main__":
    print(PROJECT_TITLE)
    run(ALGORITHM, SAMPLE_INPUT)
