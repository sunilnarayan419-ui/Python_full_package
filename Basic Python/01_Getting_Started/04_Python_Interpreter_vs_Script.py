"""
04. Python Interpreter vs. Script

The Python interpreter runs Python statements directly and shows results
immediately. This interactive mode is also called the REPL: Read, Evaluate,
Print, Loop.

A Python script is a saved .py file. Python executes its statements in order
when you run the file. Scripts are useful for programs you want to save, edit,
share, and run again.

In the interpreter, for example:

>>> 2 + 3
5
>>> message = "Hello"
>>> print(message)
Hello

To run a script from a terminal, change to its folder and use:

	python my_script.py

On some systems, the command is `python3 my_script.py` instead.
"""


def main():
	"""Run the examples in this script."""
	# A script runs statements from top to bottom.
	first_number = 8
	second_number = 4
	print("Running as a script:")
	print("The sum is", first_number + second_number)


# Python sets __name__ to "__main__" when this file is run directly.
# If another file imports it, this condition is false and main() is not called.
if __name__ == "__main__":
	main()
