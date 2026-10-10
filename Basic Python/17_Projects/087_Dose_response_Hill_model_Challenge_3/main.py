"""Runnable educational project. See README.md for the problem statement."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from project_engine import run

PROJECT_TITLE = 'Dose-response Hill model — Challenge 3'
ALGORITHM = 'hill'
SAMPLE_INPUT = [1, 10, 2, [0, 1, 10, 100]]

if __name__ == "__main__":
    print(PROJECT_TITLE)
    run(ALGORITHM, SAMPLE_INPUT)
