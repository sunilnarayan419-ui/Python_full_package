"""
02_Installing_Python.py
========================
This file explains how to install Python and verifies the installation.
"""

import sys
import shutil

print("=== Python Installation Check ===")
print()

# Check if Python is already installed
python_path = shutil.which("python") or shutil.which("python3")

if python_path:
    print(f"Python is installed at: {python_path}")
    print(f"Python version: {sys.version}")
else:
    print("Python is NOT installed. Please download from https://python.org")

print()
print("--- Installation Steps (Windows) ---")
print("1. Visit https://www.python.org/downloads/")
print("2. Download the latest stable release")
print("3. Run the installer (python-3.x.x.exe)")
print("4. IMPORTANT: Check 'Add Python to PATH' in the installer")
print("5. Verify with: python --version")

print()
print("--- Installation Steps (macOS) ---")
print("1. Download from https://python.org/downloads/")
print("2. Double-click the .dmg file to install")
print("3. Verify with: python --version")

print()
print("--- Installation Steps (Linux) ---")
print("1. Open terminal and run: sudo apt-get install python3")
print("2. Or use: sudo yum install python3 (on RHEL/CentOS)")
print("3. Verify with: python3 --version")