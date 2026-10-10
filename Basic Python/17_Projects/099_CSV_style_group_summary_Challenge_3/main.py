"""Runnable educational project. See README.md for the problem statement."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from project_engine import run

PROJECT_TITLE = 'CSV-style group summary — Challenge 3'
ALGORITHM = 'groups'
SAMPLE_INPUT = [['A', 1], ['A', 2], ['A', 3]]

if __name__ == "__main__":
    print(PROJECT_TITLE)
    run(ALGORITHM, SAMPLE_INPUT)
