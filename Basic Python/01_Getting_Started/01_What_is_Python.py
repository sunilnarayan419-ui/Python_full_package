"""
01_What_is_Python.py
====================
This file demonstrates what Python is and its key characteristics.
"""

# Python is a high-level, interpreted programming language
# Key features:
# - Easy to read and write (clean syntax)
# - Interpreted (no compilation needed)
# - Dynamically typed
# - Object-oriented
# - Large standard library
# - Cross-platform

print("=== What is Python? ===")
print()
print("Python is a versatile programming language used for:")
print("  • Web Development (Django, Flask, FastAPI)")
print("  • Data Science & AI (NumPy, Pandas, TensorFlow, PyTorch)")
print("  • Automation & Scripting")
print("  • Scientific Computing")
print("  • Game Development")
print("  • Desktop Applications")
print()
print("Python version:", __import__('sys').version.split()[0])

# Simple demonstration
print("\n--- Quick Demo ---")
name = "Python"
version = 3.12
print(f"Hello from {name} {version}!")
print(f"Type of 'name': {type(name)}")
print(f"Type of 'version': {type(version)}")