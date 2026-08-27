# Define a function to list naming conventions
def list_naming_conventions():
    """List common naming conventions in Python."""
    
    # Print the title of the section
    print("# Naming Conventions")
    print("--------------------")

    # List common naming conventions
    naming_conventions = [
        "Variable Names:",  # lowercase with underscores
        "Class Names:",     # PascalCase or camelCase
        "Function Names:",   # underscore-separated words
        "Method Names:",     # same as function names
        "Module Names:",     # lowercase with underscores
        "Constant Names:",   # uppercase with underscores
    ]

    # Print the list of naming conventions
    for convention, description in naming_conventions:
        print(f"- {convention}: {description}")

# Define a function to demonstrate good practices
def demonstrate_good_practices():
    """Demonstrate good practices for naming variables and functions."""
    
    # Variable names should be descriptive but concise
    variable_name = "user_age"
    print(f"Variable name '{variable_name}' is acceptable.")
    
    # Function names should follow the underscore-separated words pattern
    def greet_user(name):
        pass
    
    print("Function 'greet_user' demonstrates good naming practices.")

# Main program loop
def main():
    # List naming conventions
    list_naming_conventions()
    
    # Demonstrate good practices
    demonstrate_good_practices()

if __name__ == "__main__":
    main()

"""

**Example Output:**

```
# Naming Conventions
--------------------
- Variable Names: lowercase with underscores
- Class Names: PascalCase or camelCase
- Function Names: underscore-separated words
- Method Names: same as function names
- Module Names: lowercase with underscores
- Constant Names: uppercase with underscores

Function 'greet_user' demonstrates good naming practices.
"""