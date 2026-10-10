"""Runnable educational project. See README.md for the problem statement."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from project_engine import run

PROJECT_TITLE = 'Michaelis-Menten kinetics — Challenge 2'
ALGORITHM = 'mm'
SAMPLE_INPUT = [80, 10, [0, 2, 10, 30]]

if __name__ == "__main__":
    print(PROJECT_TITLE)
    run(ALGORITHM, SAMPLE_INPUT)
