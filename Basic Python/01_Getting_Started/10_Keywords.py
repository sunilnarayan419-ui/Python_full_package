"""
10. Keywords
Main points
- Keywords are reserved words with special meaning in Python syntax.
- You cannot use a keyword as an ordinary variable, function, or class name.
- Examples include if, else, for, while, def, class, return, import, try, and except.
- The keyword list can vary between Python versions.
- True, False, and None are special constants and cannot be reassigned.
- Use the keyword module to inspect keywords for your current Python installation.
"""


import keyword

# Display all keywords in the current Python version
print("Python keywords:")
print(keyword.kwlist)

# Check whether a word is a keyword
print("if:", keyword.iskeyword("if"))
print("for:", keyword.iskeyword("for"))
print("sample:", keyword.iskeyword("sample"))

# Keywords have defined syntactic roles.
temperature = 30

if temperature > 25:
    print("Temperature is above 25.")

for number in range(1, 4):
    print("Number:", number)


def greet(name):
    return f"Hello, {name}!"


print(greet("Python learner"))
