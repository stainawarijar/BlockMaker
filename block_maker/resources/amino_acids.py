from . import constants


def calculate_amino_acid_mass(composition):
    '''
    Calculate the masses of an amino acid based on its elemental composition.
    Used to generate dictionary of amino acid masses.
    Input 'amino_acid_composition' is a dictionary.
    Return mass (amu) as a float.
    '''
    mass = (
        composition["carbons"] * constants.CARBON_MASS
        + composition["hydrogens"] * constants.HYDROGEN_MASS
        + composition["oxygens"] * constants.OXYGEN_MASS
        + composition["nitrogens"] * constants.NITROGEN_MASS
        + composition["sulfurs"] * constants.SULFUR_MASS
    )      
    
    return mass


# Dictionary with amino acid residue elemental compositions (full composition minus H2O).
compositions = {
    "A": {"carbons": 3, "hydrogens": 5, "nitrogens": 1, "oxygens": 1, "sulfurs": 0},  # Alanine (Ala)
    "R": {"carbons": 6, "hydrogens": 12, "nitrogens": 4, "oxygens": 1, "sulfurs": 0},  # Arginine (Arg)
    "N": {"carbons": 4, "hydrogens": 6, "nitrogens": 2, "oxygens": 2, "sulfurs": 0},  # Asparagine (Asn)
    "D": {"carbons": 4, "hydrogens": 5, "nitrogens": 1, "oxygens": 3, "sulfurs": 0},  # Aspartic acid (Asp)
    "C": {"carbons": 3, "hydrogens": 5, "nitrogens": 1, "oxygens": 1, "sulfurs": 1},  # Cysteine (Cys)
    "E": {"carbons": 5, "hydrogens": 7, "nitrogens": 1, "oxygens": 3, "sulfurs": 0},  # Glutamic acid (Glu)
    "Q": {"carbons": 5, "hydrogens": 8, "nitrogens": 2, "oxygens": 2, "sulfurs": 0},  # Glutamine (Gln)
    "G": {"carbons": 2, "hydrogens": 3, "nitrogens": 1, "oxygens": 1, "sulfurs": 0},  # Glycine (Gly)
    "H": {"carbons": 6, "hydrogens": 7, "nitrogens": 3, "oxygens": 1, "sulfurs": 0},  # Histidine (His)
    "I": {"carbons": 6, "hydrogens": 11, "nitrogens": 1, "oxygens": 1, "sulfurs": 0},  # Isoleucine (Ile)
    "L": {"carbons": 6, "hydrogens": 11, "nitrogens": 1, "oxygens": 1, "sulfurs": 0},  # Leucine (Leu)
    "K": {"carbons": 6, "hydrogens": 12, "nitrogens": 2, "oxygens": 1, "sulfurs": 0},  # Lysine (Lys)
    "M": {"carbons": 5, "hydrogens": 9, "nitrogens": 1, "oxygens": 1, "sulfurs": 1},  # Methionine (Met)
    "F": {"carbons": 9, "hydrogens": 9, "nitrogens": 1, "oxygens": 1, "sulfurs": 0},  # Phenylalanine (Phe)
    "P": {"carbons": 5, "hydrogens": 7, "nitrogens": 1, "oxygens": 1, "sulfurs": 0},  # Proline (P)
    "S": {"carbons": 3, "hydrogens": 5, "nitrogens": 1, "oxygens": 2, "sulfurs": 0},  # Serine (Ser)
    "T": {"carbons": 4, "hydrogens": 7, "nitrogens": 1, "oxygens": 2, "sulfurs": 0},  # Threonine (Thr)
    "W": {"carbons": 11, "hydrogens": 10, "nitrogens": 2, "oxygens": 1, "sulfurs": 0},  # Tryptophan (Trp)
    "Y": {"carbons": 9, "hydrogens": 9, "nitrogens": 1, "oxygens": 2, "sulfurs": 0},  # Tyrosine (Tyr)
    "V": {"carbons": 5, "hydrogens": 9, "nitrogens": 1, "oxygens": 1, "sulfurs": 0}  # Valine (Val)
}


# Dictionary with monoisotopic masses of amino acid residues.
# Calculated based on elemental compositions.
masses = {
    aa: calculate_amino_acid_mass(composition)
    for aa, composition in compositions.items()
}

