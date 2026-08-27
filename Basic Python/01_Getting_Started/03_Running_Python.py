"""
03_Running_Python.py
====================
This file demonstrates how to run Python code:
  - From the command line (interactive mode)
  - From a script file
  - Using Python's interactive shell
"""

print("=== How to Run Python ===")
print()

# Option 1: Interactive mode (REPL)
print("1. Interactive Mode (REPL):")
print("   Open a terminal and type: python")
print("   You will see the Python prompt >>>")
print("   Type any expression, press Enter, and it evaluates.")
print("   Example: >>> 2 + 2")
print("           4")
print()

# Option 2: Running a script file
print("2. Running a Script File:")
print("   Create a file called script.py with your Python code:")
print("   python script.py")
print()
print("   The script will execute and the output will appear in the terminal.")
print()

# Option 3: Using the -c flag
print("3. Using python -c (run a command directly):")
print("   python -c 'print(\"Hello World\")'")
print()

# Option 4: Using the -m flag (module mode)
print("4. Using python -m (run a module as a script):")
print("   python -m http.server 8000   (starts a simple HTTP server)")
print()

print("--- Typical Workflow ---")
print("  1. Open a terminal or command prompt")
print("  2. Navigate to your project directory")
print("  3. Type: python filename.py")
print("  4. Your Python code runs!")
print()

# Quick test
print("--- Quick Test ---")
import sys
print(f"Python version: {sys.version}")