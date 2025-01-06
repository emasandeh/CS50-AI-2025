from cs50 import get_int

def main():
    # Prompt user for pyramid height
    height = get_height()
    
    # Generate the pyramid
    for row in range(1, height + 1):
        # Print left-aligned spaces for left pyramid
        print(" " * (height - row), end="")
        
        # Print hashes for left pyramid
        print("#" * row, end="")
        
        # Print gap
        print("  ", end="")
        
        # Print hashes for right pyramid
        print("#" * row)

def get_height():
    while True:
        # Prompt for a positive integer between 1 and 8
        height = get_int("Height: ")
        if 1 <= height <= 8:
            return height

if __name__ == "__main__":
    main()
