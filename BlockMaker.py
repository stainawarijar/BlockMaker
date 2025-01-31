from BlockMaker import utils
from BlockMaker.peptide import Peptide


def main():
    # Ask for user input and generate block file.
    while True:
        sequence = utils.get_input_sequence()
        name = utils.get_block_name()
        peptide = Peptide(sequence, name)
        peptide.write_block_file()  

        # Ask user if they want to create another block file or quit
        while True:
            input_continue = input("\nDo you want to create another block file? [Y/N]: ").strip().upper()
            if input_continue == "Y":
                break  # Exit the inner while-loop
            elif input_continue == "N":
                print("\nExiting the program...")
                return  # Exit the main function
            else:
                print("\nInvalid input. Please enter 'Y' (yes) or 'N' (no).")



if __name__ == "__main__":
    main()
    
