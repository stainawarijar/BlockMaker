from .resources import amino_acids as aa



def get_input_sequence():
    '''
    Let the user input the amino acid sequence of the peptide using single-letter code..
    The validity of the sequence is checked, and letters automatically capitalized.
    Return the capitalized sequence as a string.
    '''
    while True:
        input_sequence = input("\nEnter your peptide sequence: ").strip().upper()  # Capitalize letters
        # Loop over each character in the input sequence and look for invalid entries
        invalid_positions = []    
        invalid_characters = [] 
        for i, char in enumerate(input_sequence):
            if not char in aa.compositions.keys():
                invalid_positions.append(i + 1)  # Add index plus 1, so counting starts at 1
                invalid_characters.append(char)
        # Check if there are invalid entries
        if len(invalid_positions) == 1:
            print(f"\nCharacter '{invalid_characters[0]}' at position {invalid_positions[0]} "
                  "does not correspond to any amino acid.")
        elif len(invalid_positions) > 1:
            positions_join = ", ".join(map(str, invalid_positions[:-1])) + " and " + str(invalid_positions[-1])
            characters_join = (
                ", ".join(f"'{item}'" for item in invalid_characters[:-1]) + 
                " and '" + str(invalid_characters[-1]) + "'"
            )
            print(f"\nCharacters {characters_join} at positions {positions_join} "
                  "do not correspond to any amino acids.")
        else:
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


def get_cysteine_treatment():
    '''
    Ask the user for treatment of cysteine residues.
    Return a string: 'untreated', 'amide' or 'acid'
    '''
    treatments = ["untreated", "amide", "acid"]
    while True:
        choice = input(
            "\nSelect a treatment for your cysteine (C) residues:"
            "\n\t[1] None (reduced form)"
            "\n\t[2] Iodo- or chloroacetamide"
            "\n\t[3] Iodo- or chloroacetic acid"
            "\nEnter your choice: "
        )
        if not choice.strip() in ["1", "2", "3"]:
            print("\nInvalid input. Please enter '1', '2' or '3'")
        else:
            # Print choice
            if choice.strip() == "1":
                print("\nCysteine residues untreated (reduced form).")
            elif choice.strip == "2":
                print("\nCysteine residues treated with iodo- or chloroacetamide.")
            else:
                print("\nCysteine residues treated with iodo- or chloroacetic acid.")
            # Return choice
            return treatments[int(choice) - 1]


def get_methionine_oxidation():
    '''
    Ask user whether methionine residues should be treated as oxidized.
    Return boolean: True (oxidized) or False (non-oxidized)
    '''
    while True:
        choice = input("\nShould methionine (M) residues be considered oxidized? [Y/N]: ").strip().upper()
        if choice == "Y":
            print("\nMethionine residues considered oxidized.")
            return True
        elif choice == "N":
            print("\nMethionine residues not considered oxidized.")
            return False
        else:
            print("\nInvalid input. Please enter 'Y' (yes) or 'N' (no).")

