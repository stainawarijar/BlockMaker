import datetime
from .resources import amino_acids


def write_to_log(message):
    '''Write message to log file with date and time'''
    with open("BlockMaker.log", "a") as file:  # Use "a" to append to the file
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if message.startswith("Start processing sequence"):
            # Add empty line before new sequence
            file.write(f"\n\n{timestamp}\t{message}")
        else:
            file.write(f"\n{timestamp}\t{message}")
        

def get_input_sequence():
    '''
    Let the user input the amino acid sequence of the peptide using single-letter code.
    Return the capitalized sequence as a string.
    '''
    while True:
        input_sequence = input("\nEnter your peptide sequence: ").strip().upper()  # Capitalize letters
        # Loop over each character in the input sequence and look for invalid entries
        invalid_positions = []    
        invalid_characters = [] 
        for i, char in enumerate(input_sequence):
            if not char in amino_acids.compositions.keys():
                invalid_positions.append(i + 1)  # Add index plus 1, so counting starts at 1
                invalid_characters.append(char)
        # Check if there are invalid entries
        if len(invalid_positions) == 1:
            print(
                f"\nCharacter '{invalid_characters[0]}' at position {invalid_positions[0]} "
                "does not correspond to any amino acid."
            )
        elif len(invalid_positions) > 1:
            positions_join = ", ".join(map(str, invalid_positions[:-1])) + " and " + str(invalid_positions[-1])
            characters_join = (
                ", ".join(f"'{item}'" for item in invalid_characters[:-1]) + 
                " and '" + str(invalid_characters[-1]) + "'"
            )
            print(
                f"\nCharacters {characters_join} at positions {positions_join} "
                "do not correspond to any amino acids."
            )
        else:
            write_to_log(f"Start processing sequence '{input_sequence}'...")
            return input_sequence
    

def get_block_name():
    '''
    Ask user for a name to give to the block file.
    The name can consist only of letters.
    Return the input name as a string after checking its validity.
    '''
    while True:
        input_name = input("\nEnter name for your block file: ").strip()
        if not input_name.isalpha():
            print("\nThe name of your block file can only contain letters.")
        else:
            return input_name

