"""Runnable educational project. See README.md for the problem statement."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from project_engine import run

PROJECT_TITLE = 'CSV-style group summary — Challenge 2'
ALGORITHM = 'groups'
SAMPLE_INPUT = [['Control', 5], ['Control', 7], ['Drug', 9], ['Drug', 11]]

if __name__ == "__main__":
    print(PROJECT_TITLE)
    run(ALGORITHM, SAMPLE_INPUT)
