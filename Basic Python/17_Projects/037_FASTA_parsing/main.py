"""Runnable educational project. See README.md for the problem statement."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from project_engine import run

PROJECT_TITLE = 'FASTA parsing'
ALGORITHM = 'fasta'
SAMPLE_INPUT = '>gene1\nATGC\nGGTA\n>gene2\nTTAA\n'

if __name__ == "__main__":
    print(PROJECT_TITLE)
    run(ALGORITHM, SAMPLE_INPUT)
