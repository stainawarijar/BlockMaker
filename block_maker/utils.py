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


def check_sequence_validity(sequence_input):
    '''
    Check the validity of an input peptide sequence.
    Returns a dictionary with two lists: invalid characters and their positions
    '''
    invalid = {"positions": [], "characters": []}
    # Loop over each character in the input sequence and look for invalid entries
    for i, char in enumerate(sequence_input):
        if char not in amino_acids.compositions.keys():
            invalid["positions"].append(i + 1)  # Add index plus 1, so counting starts at 1
            invalid["characters"].append(char)
    # Return the dictionary
    return invalid