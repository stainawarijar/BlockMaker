import os
from . import utils
from .resources import amino_acids
from .resources import constants


class Peptide():
    def __init__(self, sequence, name):
        self.sequence = sequence
        self.name = name
        self.cysteine_treatment = self.get_cysteine_treatment()
        self.methionine_oxidation = self.get_methionine_oxidation()
        self.isotope_labeling = self.get_isotope_labeling()
        self.composition = self.get_composition()
        self.mass = self.calculate_peptide_mass()
    
    
    def get_cysteine_treatment(self):
        '''
        Ask the user for treatment of cysteine residues.
        Return a string: 'untreated', 'amide' or 'acid' if C is in the sequence.
        Return None when C is not in the sequence.
        '''
        if not "C" in self.sequence:
            return None
        else:
            treatments = ["untreated", "amide", "acid"]
            while True:
                choice_treatment = input(
                    "\nSelect a treatment for your cysteine (C) residues:"
                    "\n\t[1] None (reduced form)"
                    "\n\t[2] Iodo- or chloroacetamide"
                    "\n\t[3] Iodo- or chloroacetic acid"
                    "\nEnter your choice: "
                )
                if not choice_treatment.strip() in ["1", "2", "3"]:
                    print("\nInvalid input. Please enter '1', '2' or '3'")
                else:
                    # Print choice and write to log file
                    if choice_treatment.strip() == "1":
                        utils.write_to_log("Cysteine (C) residues untreated (reduced form).")
                        print("\nCysteine residues untreated (reduced form).")
                    elif choice_treatment.strip() == "2":
                        utils.write_to_log("Cysteine (C) residues treated with iodo- or chloroacetamide.")
                        print("\nCysteine residues treated with iodo- or chloroacetamide.")
                    else:
                        utils.write_to_log("Cysteine (C) residues treated with iodo- or chloroacetic acid.")
                        print("\nCysteine residues treated with iodo- or chloroacetic acid.")
                    # Return choice
                    return treatments[int(choice_treatment) - 1]
                
    
    
    def get_methionine_oxidation(self):
        '''
        Ask user whether methionine residues should be treated as oxidized.
        Return boolean: True (oxidized) or False (non-oxidized) if M is in the sequence.
        Return None if M is not part of the sequence.
        '''
        if not "M" in self.sequence:
            return None
        else:
            while True:
                choice_oxidation = input("\nShould methionine (M) residues be considered oxidized? [Y/N]: ").strip().upper()
                if choice_oxidation == "Y":
                    utils.write_to_log("Methionine (M) residues considered oxidized.")
                    print("\nMethionine residues considered oxidized.")
                    return True
                elif choice_oxidation == "N":
                    utils.write_to_log("Methionine (M) residues not considered oxidized.")
                    print("\nMethionine residues not considered oxidized.")
                    return False
                else:
                    print("Invalid input. Please enter 'Y' (yes) or 'N' (no).")


    def get_isotope_labeling(self):
        '''
        Ask user if the peptide contains amino acid residues labeled with C-13 and N-15.
        If yes, return a list with amino acids that are labeled.
        If no, return None.
        '''
        pass


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
                peptide_composition["nitrogens"] += self.sequence.count("C")
                peptide_composition["oxygens"] += self.sequence.count("C")
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
        # Print info in terminal and write to log
        message = (
            f"Writing sequence '{self.sequence}' info to block file '{self.name}.block':"
            f"\n\tMass = {self.mass:.5f}" 
            f"\n\tCarbons = {self.composition['carbons']}"
            f"\n\tHydrogens = {self.composition['hydrogens']}"
            f"\n\tNitrogens = {self.composition['nitrogens']}"
            f"\n\tOxygens = {self.composition['oxygens']}"
            f"\n\tSulfurs = {self.composition['sulfurs']}"
        )
        utils.write_to_log(message)
        print(f"Writing sequence '{self.sequence}' info to block file '{self.name}.block'")
        
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
        utils.write_to_log(f"'{self.name}.block' file created in directory '{os.getcwd()}'")
        print(f"\n'{self.name}.block' file created in directory '{os.getcwd()}'")
