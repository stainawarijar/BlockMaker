from . import constants


def calculate_amino_acid_residue_mass(composition):
    '''
    Calculate the monoisotopic mass of an amino acid residue based on 
    its elemental composition. Composition input is a dictionary.
    Return the mass (amu) as a float.
    '''
    mass = (
        composition["carbons"] * constants.CARBON_MASS
        + composition["hydrogens"] * constants.HYDROGEN_MASS
        + composition["oxygens"] * constants.OXYGEN_MASS
        + composition["nitrogens"] * constants.NITROGEN_MASS
        + composition["sulfurs"] * constants.SULFUR_MASS
    )     
     
    return mass


# Dictionary with elemental compositions of amino acid residues (excluding H2O).
compositions = {
    "A": { # Alanine (Ala)
        "carbons": 3, "hydrogens": 5, "nitrogens": 1, "oxygens": 1, "sulfurs": 0
    }, 
    "R": { # Arginine (Arg)
        "carbons": 6, "hydrogens": 12, "nitrogens": 4, "oxygens": 1, "sulfurs": 0
    },  
    "N": { # Asparagine (Asn)
        "carbons": 4, "hydrogens": 6, "nitrogens": 2, "oxygens": 2, "sulfurs": 0
    }, 
    "D": { # Aspartic acid (Asp)
        "carbons": 4, "hydrogens": 5, "nitrogens": 1, "oxygens": 3, "sulfurs": 0
    },  
    "C": { # Cysteine (Cys)
        "carbons": 3, "hydrogens": 5, "nitrogens": 1, "oxygens": 1, "sulfurs": 1
    },
    "E": { # Glutamic acid (Glu)
        "carbons": 5, "hydrogens": 7, "nitrogens": 1, "oxygens": 3, "sulfurs": 0
    },
    "Q": { # Glutamine (Gln)
        "carbons": 5, "hydrogens": 8, "nitrogens": 2, "oxygens": 2, "sulfurs": 0
    },
    "G": { # Glycine (Gly)
        "carbons": 2, "hydrogens": 3, "nitrogens": 1, "oxygens": 1, "sulfurs": 0
    },
    "H": { # Histidine (His)
        "carbons": 6, "hydrogens": 7, "nitrogens": 3, "oxygens": 1, "sulfurs": 0
    },
    "I": { # Isoleucine (Ile)
        "carbons": 6, "hydrogens": 11, "nitrogens": 1, "oxygens": 1, "sulfurs": 0
    },
    "L": { # Leucine (Leu)
        "carbons": 6, "hydrogens": 11, "nitrogens": 1, "oxygens": 1, "sulfurs": 0
    },
    "K": { # Lysine (Lys)
        "carbons": 6, "hydrogens": 12, "nitrogens": 2, "oxygens": 1, "sulfurs": 0
    },
    "M": { # Methionine (Met)
        "carbons": 5, "hydrogens": 9, "nitrogens": 1, "oxygens": 1, "sulfurs": 1
    }, 
    "F": { # Phenylalanine (Phe)
        "carbons": 9, "hydrogens": 9, "nitrogens": 1, "oxygens": 1, "sulfurs": 0
    }, 
    "P": { # Proline (P)
        "carbons": 5, "hydrogens": 7, "nitrogens": 1, "oxygens": 1, "sulfurs": 0
    }, 
    "S": { # Serine (Ser)
        "carbons": 3, "hydrogens": 5, "nitrogens": 1, "oxygens": 2, "sulfurs": 0
    },
    "T": { # Threonine (Thr)
        "carbons": 4, "hydrogens": 7, "nitrogens": 1, "oxygens": 2, "sulfurs": 0
    },
    "W": { # Tryptophan (Trp)
        "carbons": 11, "hydrogens": 10, "nitrogens": 2, "oxygens": 1, "sulfurs": 0
    },
    "Y": { # Tyrosine (Tyr)
        "carbons": 9, "hydrogens": 9, "nitrogens": 1, "oxygens": 2, "sulfurs": 0
    },
    "V": { # Valine (Val)
        "carbons": 5, "hydrogens": 9, "nitrogens": 1, "oxygens": 1, "sulfurs": 0
    }
}


# Dictionary with monoisotopic masses of amino acid residues.
# Calculated based on elemental compositions.
masses = {
    aa: calculate_amino_acid_residue_mass(composition)
    for aa, composition in compositions.items()
}

