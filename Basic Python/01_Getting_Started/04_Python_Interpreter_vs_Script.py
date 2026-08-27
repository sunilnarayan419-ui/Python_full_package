"""
04_Python_Interpreter_vs_Script.py
==================================
This file demonstrates the difference between Python interpreter mode
and running a Python script file.
"""

print("=== Python Interpreter vs Script ===")
print()

# What is the Python Interpreter?
print("The Python Interpreter:")
print("  - Runs Python code line by line")
print("  - Also called the Interactive Shell or REPL")
print("  - Each line is executed immediately")
print("  - Useful for testing small code snippets")
print("  - Example: type this: print('Hello') and press Enter")
print()

# What is a Python Script?
print("A Python Script (.py file):")
print("  - A file containing multiple lines of Python code")
print("  - Read once and executed as a whole")
print("  - Can import modules and use variables across all lines")
print("  - Example: save code to script.py, then run: python script.py")
print()

# Comparison Table
print("--- Comparison ---")
print(f"{'Aspect':<30} {'Interpreter':<25} {'Script':<25}")
print("-" * 80)
print(f"{'Input':<30} {'Line by line (stdin)':<25} {'File (one-time)':<25}")
print(f"{'Execution':<30} {'Immediate per line':<25} {'All at once':<25}")
print(f"{'Reusability':<30} {'No (manual typing)':<25} {'Yes (rerun)':<25}")
print(f"{'Use case':<30} {'Quick testing':<25} {'Full programs':<25}")
print()

# A small demonstration
print("--- Quick Demo ---")
print("In interpreter mode:")
print("  >>> x = 10")
print("  >>> y = 5")
print("  >>> x + y")
print("  15")
print()

print("In script mode (script.py):")
print("  # x = 10")
print("  # y = 5")
print("  # print(x + y)")
print("  # When run: python script.py")
print("  # Output: 15")
print()

# Example: create a script file programmatically
import tempfile, os
print("--- Creating a Script File Programmatically ---")
with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
    f.write("print('Hello from Python script!')")
    temp_path = f.name

print(f"Created: {temp_path}")
print("Running it...")
os.system(f"python {temp_path}")
os.unlink(temp_path)
print()
print("Done!")