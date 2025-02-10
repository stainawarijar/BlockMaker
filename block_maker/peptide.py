import os
from . import utils
from .resources import amino_acids
from .resources import constants


class Peptide():
    def __init__(self, block_name, sequence, cysteine_treatment, methionine_oxidation, isotope_labeling):
        self.block_name = block_name
        self.sequence = sequence
        self.cysteine_treatment = cysteine_treatment
        self.methionine_oxidation = methionine_oxidation
        self.isotope_labeling = isotope_labeling
        self.composition = self.get_composition()
        self.mass = self.calculate_peptide_mass()


    def get_composition(self):
        '''
        Determine elemental composition based on peptide sequence.
        Include cysteine treatment, methionine oxidation and C-13/N-15 labeling when applicable.
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
        if "C" in self.sequence:
            if self.cysteine_treatment == "Iodo- or chloroacetamide":
                # Replace H in cysteine -SH group by -CH2-CO-NH2 group, for each cysteine
                peptide_composition["carbons"] += 2 * self.sequence.count("C")
                peptide_composition["hydrogens"] += 3 * self.sequence.count("C") # Difference of 3 H
                peptide_composition["nitrogens"] += self.sequence.count("C")
                peptide_composition["oxygens"] += self.sequence.count("C")
            elif self.cysteine_treatment == "Iodo- or chloroacetic acid":
                # Replace H in cysteine -SH group by -CH2-CO-OH group, for each cysteine
                peptide_composition["carbons"] += 2 * self.sequence.count("C")
                peptide_composition["hydrogens"] += 2 * self.sequence.count("C")  # Difference of 2 H
                peptide_composition["oxygens"] += 2 * self.sequence.count("C")

        # Check methionine oxidation
        if "M" in self.sequence and self.methionine_oxidation:
            # Add oxygen atom for each methionine residue
            peptide_composition["oxygens"] += self.sequence.count("M")

        # Check list with isotope labeled amino acids
        if len(self.isotope_labeling) > 0:
            # Loop over the labeled amino acids
            # C and N in these amino acids are always C-13 and N-15 (no variation)
            # Must be removed from the composition written to the block file 
            for aa in self.isotope_labeling:
                peptide_composition["carbons"] -= amino_acids.compositions[aa]["carbons"] * self.sequence.count(aa)
                peptide_composition["nitrogens"] -= amino_acids.compositions[aa]["nitrogens"] * self.sequence.count(aa)
                
        return peptide_composition
        
        
    def calculate_peptide_mass(self):
        '''
        Calculate the monoisotopic mass of the peptide based on its sequence.
        Include cysteine treatment, methionine oxidation and C-13/N-15 labeling when applicable.
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
        if "C" in self.sequence:
            if self.cysteine_treatment == "Iodo- or chloroacetamide":
                peptide_mass += (constants.ACETAMIDE_GROUP_MASS - constants.HYDROGEN_MASS) * self.sequence.count("C")
            elif self.cysteine_treatment == "Iodo- or chloroacetic acid":
                peptide_mass += (constants.ACETIC_ACID_GROUP_MASS - constants.HYDROGEN_MASS) * self.sequence.count("C")

        # Check methionine oxidation
        if "M" in self.sequence and self.methionine_oxidation:
            # Add oxygen mass for each methionine residue
            peptide_mass += constants.OXYGEN_MASS * self.sequence.count("M")

        # Check list with isotope labeled amino acids
        if len(self.isotope_labeling) > 0:
            # Loop over the labeled amino acids and increase mass
            for aa in self.isotope_labeling:
                peptide_mass += constants.C13_MASS_DIFF * amino_acids.compositions[aa]["carbons"] * self.sequence.count(aa)
                peptide_mass += constants.N15_MASS_DIFF * amino_acids.compositions[aa]["nitrogens"] * self.sequence.count(aa)

        # Return mass rounded to nine decimals
        return round(peptide_mass, 9)
    

    def write_block_file(self, output_dir):
        '''
        Create block file based on composition and mass of the peptide.
        The output directory of the block file is printed for the user.
        Information is written to the log file.
        '''
        # Write message to log file
        message = (
            f"Writing sequence '{self.sequence}' info to block file '{self.block_name}.block':"
            f"\n\tMass = {self.mass:.5f}" 
            f"\n\tCarbons = {self.composition['carbons']}"
            f"\n\tHydrogens = {self.composition['hydrogens']}"
            f"\n\tNitrogens = {self.composition['nitrogens']}"
            f"\n\tOxygens = {self.composition['oxygens']}"
            f"\n\tSulfurs = {self.composition['sulfurs']}"
        )
        utils.write_to_log(message)
        
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

        # Write each line to the file in the specified output directory
        filename = os.path.join(output_dir, self.block_name + ".block")
        with open(filename, "w") as file:
            for line in lines:
                file.write(line + "\n")
                
        # Print location of the created block file.
        utils.write_to_log(f"'{self.block_name}.block' file created in directory '{output_dir}'")
        print(f"\n'{self.block_name}.block' file created in directory '{output_dir}'")
