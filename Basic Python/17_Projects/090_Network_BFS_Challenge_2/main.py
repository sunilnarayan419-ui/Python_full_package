"""Runnable educational project. See README.md for the problem statement."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from project_engine import run

PROJECT_TITLE = 'Network BFS — Challenge 2'
ALGORITHM = 'bfs'
SAMPLE_INPUT = {'edges': [['A', 'B'], ['B', 'C'], ['C', 'D']], 'start': 'A', 'target': 'D'}

if __name__ == "__main__":
    print(PROJECT_TITLE)
    run(ALGORITHM, SAMPLE_INPUT)
