# Define a function to list general variables
def list_variables():
    """List general variables in Python."""
    
    # Print the title of the section
    print("# Built-In Variables")
    print("--------------------")

    # List the built-in variables
    built_in_vars = [
        "abs()",
        "all()",
        "any()",
        "ascii()",
        "bin()",
        "bool()",
        "bytearray()",
        "bytes()",
        "chr()",
        "classmethod()",
        "compile()",
        "complex()",
        "delattr()",
        "dict()",
        "dir()",
        "divmod()",
        "enumerate()",
        "eval()",
        "exec()",
        "filter()",
        "float()",
        "format()",
        "frozenset()",
        "getattr()",
        "globals()",
        "hasattr()",
        "hash()",
        "help()",
        "hex()",
        "id()",
        "input()",
        "int()",
        "isinstance()",
        "issubclass()",
        "iter()",
        "len()",
        "list()",
        "locals()",
        "map()",
        "max()",
        "memoryview()",
        "min()",
        "next()",
        "object()",
        "oct()",
        "open()",
        "ord()",
        "pow()",
        "print()",
        "property()",
        "range()",
        "repr()",
        "reversed()",
        "round()",
        "set()",
        "setattr()",
        "slice()",
        "sorted()",
        "staticmethod()",
        "str()",
        "sum()",
        "tuple()",
        "type()",
        "vars()",
        "zip()",
    ]

    # Print the list of built-in variables
    for var in built_in_vars:
        print(f"- {var}")

    # Print a horizontal line to separate the section from the next one
    print("-" * 80)

# Define a function to list commonly used variables
def list_commonly_used_variables():
    """List commonly used variables in Python."""
    
    # Print the title of the section
    print("# Commonly Used Variables")
    print("-------------------------")

    # List the commonly used variables
    common_vars = [
        "True",
        "False",
        "None",
        "range()",
        "int()",
        "float()",
        "str()",
        "list()",
        "dict()",
        "tuple()",
        "set()",
        "bool()",
        "complex()",
    ]

    # Print the list of commonly used variables
    for var in common_vars:
        print(f"- {var}")

# Define a function to list variables from the built-in functions module
def list_built_in_functions():
    """List variables from the built-in functions module."""
    
    # Import the built-in functions module
    import builtins

    # Print the title of the section
    print("# Built-In Functions")
    print("-------------------")

    # List the variables from the built-in functions module
    for var in dir(builtins):
        if not var.startswith("_"):
            print(f"- {var}")

# Main program loop
def main():
    # List general variables
    list_variables()
    
    # Print a horizontal line to separate the section from the next one
    print("-" * 80)

    # List commonly used variables
    list_commonly_used_variables()
    
    # Print a horizontal line to separate the section from the next one
    print("-" * 80)

    # List variables from the built-in functions module
    list_built_in_functions()

if __name__ == "__main__":
    main()

"""
# Built-In Variables
--------------------
- abs()
- all()
- any()
- ascii()
- bin()
- bool()
- bytearray()
- bytes()
- chr()
- classmethod()
- compile()
- complex()
- delattr()
- dict()
- dir()
- divmod()
- enumerate()
- eval()
- exec()
- filter()
- float()
- format()
- frozenset()
- getattr()
- globals()
- hasattr()
- hash()
- help()
- hex()
- id()
- input()
- int()
- isinstance()
- issubclass()
- iter()
- len()
- list()
- locals()
- map()
- max()
- memoryview()
- min()
- next()
- object()
- oct()
- open()
- ord()
- pow()
- print()
- property()
- range()
- repr()
- reversed()
- round()
- set()
- setattr()
- slice()
- sorted()
- staticmethod()
- str()
- sum()
- tuple()
- type()
- vars()
- zip()

---------------------------------------------------

# Commonly Used Variables
-------------------------
- True
- False
- None
- range()
- int()
- float()
- str()
- list()
- dict()
- tuple()
- set()
- bool()
- complex()

---------------------------------------------------

# Built-In Functions
-------------------
- abs()
- all()
- any()
- ascii()
- bin()
- bool()
- bytearray()
- bytes()
- chr()
- classmethod()
- compile()
- complex()
- delattr()
- dict()
- dir()
- divmod()
- enumerate()
- eval()
- exec()
- filter()
- float()
- format()
- frozenset()
- getattr()
- globals()
- hasattr()
- hash()
- help()
- hex()
- id()
- input()
- int()
- isinstance()
- issubclass()
- iter()
- len()
- list()
- locals()
- map()
- max()
- memoryview()
- min()
- next()
- object()
- oct()
- open()
- ord()
- pow()
- print()
- property()
- range()
- repr()
- reversed()
- round()
- set()
- setattr()
- slice()
- sorted()
- staticmethod()
- str()
- sum()
- tuple()
- type()
- vars()
- zip()
"""