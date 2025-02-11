import datetime
from .resources import amino_acids


def write_to_log(message):
    '''Write message to log file with date and time'''
    with open("BlockMaker.log", "a") as file:  
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if message.startswith("Start processing block"):
            # Add empty line before new sequence.
            file.write(f"\n\n{timestamp}\t{message}")
        else:
            file.write(f"\n{timestamp}\t{message}")


def check_sequence_validity(sequence_input):
    '''
    Check the validity of an input peptide sequence.
    Returns a dictionary with two lists: invalid characters and their positions.
    The position count starts at 1.
    '''
    invalid = {"positions": [], "characters": []}
    # Loop over each character in the sequence and look for invalid entries.
    for i, char in enumerate(sequence_input):
        if char not in amino_acids.compositions.keys():
            # Add index plus 1, so counting starts at 1
            invalid["positions"].append(i + 1) 
            invalid["characters"].append(char)
    # Return the dictionary.
    return invalid


def generate_invalid_sequence_warning(invalid, sequence):
    '''
    Generates a warning message based on invalid positions and characters
    in a peptide input sequence.
    '''
    if len(invalid["positions"]) == 1:
        warning_msg = (
            f"\nCharacter '{invalid["characters"][0]}' "
            f"at position {invalid["positions"][0]} "
            f"in sequence '{sequence}' does not correspond to any amino acid."
        )
    else:
        positions_join = (
            ", ".join(map(str, invalid["positions"][:-1])) + " and " 
            + str(invalid["positions"][-1])
        )
        characters_join = (
            ", ".join(f"'{char}'" for char in invalid["characters"][:-1]) + 
            " and '" + str(invalid["characters"][-1]) + "'"
        )
        warning_msg = (
            f"\nCharacters {characters_join} at positions {positions_join} "
            f"in sequence '{sequence}' do not correspond to any amino acids."
        )
        
    return warning_msg