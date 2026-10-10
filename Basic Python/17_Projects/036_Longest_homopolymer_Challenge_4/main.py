"""Runnable educational project. See README.md for the problem statement."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from project_engine import run

PROJECT_TITLE = 'Longest homopolymer — Challenge 4'
ALGORITHM = 'homopolymer'
SAMPLE_INPUT = 'AAATTTTGGCCGGC'

if __name__ == "__main__":
    print(PROJECT_TITLE)
    run(ALGORITHM, SAMPLE_INPUT)
