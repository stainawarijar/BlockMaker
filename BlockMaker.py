from BlockMaker import utils
from BlockMaker.peptide import Peptide



def main():
    # Print a nice welcome message
    BLUE = "\033[34m"
    RESET = "\033[0m"  # Reset to default color
    print(f"{BLUE}\n \U0001F308  Welcome to BlockMaker! \U0001F308{RESET}")
    
    # Ask for user input and generate block file.
    while True:
        sequence = utils.get_input_sequence()
        name = utils.get_block_name()
        peptide = Peptide(sequence, name)
        peptide.write_block_file()  

        # Ask user if they want to create another block file or quit
        while True:
            choice = input("\nDo you want to create another block file? [Y/N]: ").strip().upper()
            if choice == "Y":
                break  # Exit the inner while-loop
            elif choice == "N":
                print("\nExiting the program...")
                return  # Exit the main function
            else:
                print("\nInvalid input. Please enter 'Y' (yes) or 'N' (no).")



if __name__ == "__main__":
    main()
    
