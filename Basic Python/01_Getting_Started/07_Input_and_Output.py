# Define a function to get user input
def get_user_input():
    """Get user input from the console."""
    user_input = input("Please enter something: ")
    return user_input

# Define a function to process user input
def process_input(user_input):
    """Process the user's input and provide a response."""
    # Convert the input to uppercase
    upper_case_input = user_input.upper()
    
    # Check if the input is a palindrome (reads the same forwards and backwards)
    if upper_case_input == upper_case_input[::-1]:
        return f"Wow, '{user_input}' is a palindrome!"
    else:
        return f"'{user_input}' is not a palindrome. Try again!"

# Define a function to handle exceptions
def handle_exceptions(e):
    """Handle any exceptions that occur during execution."""
    print(f"An error occurred: {e}")
    return None

# Main program loop
try:
    # Get user input
    user_input = get_user_input()
    
    # Process the user's input
    result = process_input(user_input)
    
    # Print the result to the console
    print(result)
except Exception as e:
    # Handle any exceptions that occur during execution
    result = handle_exceptions(e)
