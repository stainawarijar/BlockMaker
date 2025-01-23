import os

from . import utils
from .resources import amino_acids
from .resources import constants


class Peptide():
    def __init__(self, sequence, name):
        self.sequence = sequence
        self.name = name
        self.cysteine_treatment = utils.get_cysteine_treatment() if "C" in sequence else None
        self.methionine_oxidation = utils.get_methionine_oxidation() if "M" in sequence else None
        self.composition = self.get_composition()
        self.mass = self.calculate_peptide_mass()
        

    def get_composition(self):
        '''
        Determine elemental composition based on peptide sequence.
        Include cysteine treatment and methionine oxidation when applicable.
        Return a dictionary with number of carbon, hydrogen, nitrogen, oxygen and sulfur atoms.
        '''
        # Initialize dictionary with elements.
        peptide_composition = {
            "carbons": 0,
            "hydrogens": 0,
            "nitrogens": 0,
            "oxygens": 0,
            "sulfurs": 0
        }

        # Loop over amino acids in the sequence
        for amino_acid in self.sequence:
            # Get composition of this amino acid residue
            amino_acid_composition = amino_acids.compositions[amino_acid]
            # Add up elements
            peptide_composition["carbons"] += amino_acid_composition["carbons"]
            peptide_composition["hydrogens"] += amino_acid_composition["hydrogens"]
            peptide_composition["nitrogens"] += amino_acid_composition["nitrogens"]
            peptide_composition["oxygens"] += amino_acid_composition["oxygens"]
            peptide_composition["sulfurs"] += amino_acid_composition["sulfurs"]

        # Add water molecule (H2O)
        peptide_composition["hydrogens"] += 2
        peptide_composition["oxygens"] += 1
        
        # Check cysteine modifications
        if self.cysteine_treatment is not None:
            if self.cysteine_treatment == "amide":
                # Replace H in cysteine -SH group by -CH2-CO-NH2 group, for each cysteine
                peptide_composition["carbons"] += 2 * self.sequence.count("C")
                peptide_composition["hydrogens"] += 3 * self.sequence.count("C") # Difference of 3 H
                peptide_composition["nitrogens"] += 1 * self.sequence.count("C")
                peptide_composition["oxygens"] += 1 * self.sequence.count("C")
            elif self.cysteine_treatment == "acid":
                # Replace H in cysteine -SH group by -CH2-CO-OH group, for each cysteine
                peptide_composition["carbons"] += 2 * self.sequence.count("C")
                peptide_composition["hydrogens"] += 2 * self.sequence.count("C")  # Difference of 2 H
                peptide_composition["oxygens"] += 2 * self.sequence.count("C")

        # Check methionine oxidation
        if self.methionine_oxidation is not None:
            if self.methionine_oxidation:
                # Add oxygen atom for each methionine
                peptide_composition["oxygens"] += self.sequence.count("M")
                
        return peptide_composition
        
        
    def calculate_peptide_mass(self):
        '''
        Calculate the monoisotopic mass of the peptide based on its sequence.
        Include cysteine treatment and methionine oxidation when applicable.
        Return the mass in amu rounded to five decimals.
        '''
        # Initiate mass at 0
        peptide_mass = 0 

        # Loop over the amino acids and add mass of each residue
        for amino_acid in self.sequence:
            peptide_mass += amino_acids.masses[amino_acid]

        # Add mass of H2O
        peptide_mass += constants.WATER_MASS

        # Check cysteine modifications
        if self.cysteine_treatment is not None:
            if self.cysteine_treatment == "amide":
                peptide_mass += (constants.ACETAMIDE_GROUP_MASS - constants.HYDROGEN_MASS) * self.sequence.count("C")
            elif self.cysteine_treatment == "acid":
                peptide_mass += (constants.ACETIC_ACID_GROUP_MASS - constants.HYDROGEN_MASS) * self.sequence.count("C")

        # Check methionine oxidation
        if self.methionine_oxidation is not None:
            if self.methionine_oxidation:
                # Add oxygen mass for each methionine residue
                peptide_mass += constants.OXYGEN_MASS * self.sequence.count("M")

        # Return mass rounded to nine decimals
        return round(peptide_mass, 9)
    

    def write_block_file(self):
        '''
        Create block file based on composition and mass of the peptide.
        The location of the block file is printed for the user.
        '''
        # Print info in terminal
        print(
            f"\nWriting sequence '{self.sequence}' info to block file '{self.name}.block':"
            f"\n\tMass = {self.mass:.5f}" 
            f"\n\tCarbons = {self.composition['carbons']}"
            f"\n\tHydrogens = {self.composition['hydrogens']}"
            f"\n\tNitrogens = {self.composition['nitrogens']}"
            f"\n\tOxygens = {self.composition['oxygens']}"
            f"\n\tSulfurs = {self.composition['sulfurs']}"
        )
        
        # Create list with lines that should be written
        # "\t" is used to separate named and numbers by a tab
        lines = [
            "mass" + "\t" + f"{self.mass:.9f}",  
            "available_for_charge_carrier" + "\t" + "0",
            "carbons" + "\t" + str(self.composition["carbons"]),
            "hydrogens" + "\t" + str(self.composition["hydrogens"]),
            "nitrogens" + "\t" + str(self.composition["nitrogens"]),
            "oxygens" + "\t" + str(self.composition["oxygens"]),
            "sulfurs" + "\t" + str(self.composition["sulfurs"])
        ]

        # Write each line to the file
        filename = self.name + ".block"
        with open(filename, "w") as file:
            for line in lines:
                file.write(line + "\n")
                
        # Print location of the created block file.
        print(f"\n'{self.name}.block' file created in directory '{os.getcwd()}'")
