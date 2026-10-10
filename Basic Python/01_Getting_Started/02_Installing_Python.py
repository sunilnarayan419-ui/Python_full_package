"""
02. Installing Python
Main points
- Download Python from the official website: Python Downloads.
- On Windows, select Add Python to PATH during installation when that option is available.
- Verify the installation from a terminal.
- python and py are common commands on Windows; python3 is common on Linux and macOS.
- Use a virtual environment for project-specific dependencies.

"""


# Check whether Python is installed (Windows)
python --version

# Alternative Windows launcher
py --version

# Check pip, Python's package installer
python -m pip --version

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment on Windows
.venv\Scripts\activate

# Upgrade pip inside the active environment
python -m pip install --upgrade pip

# Deactivate the virtual environment when finished
deactivate
