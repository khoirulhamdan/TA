def character_counter():
    # Taking input from the user
    input_string = input("Enter some text: ")
    
    # Count the number of characters (including spaces)
    count = len(input_string)
    
    # Display the result
    print(f"The number of characters in the entered text is: {count}")

# Call the function to run
character_counter()
