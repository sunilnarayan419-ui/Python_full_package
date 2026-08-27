"""
bioutils

A small self-contained bioinformatics utility package used to demonstrate
Python package structure and namespace organization.
"""

from .sequence_tools import gc_content, reverse_complement
from .stats_tools import summarize_measurements

__all__ = ["gc_content", "reverse_complement", "summarize_measurements"]
