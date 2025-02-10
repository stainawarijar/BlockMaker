![Experimental](https://img.shields.io/badge/status-experimental-yellow)

# BlockMaker
BlockMaker is a simple Python program to make block files for [LaCyTools](https://pubs.acs.org/doi/10.1021/acs.jproteome.6b00171), including options for amino acid modifications (cysteine treatment, methionine oxidation, and stable isotope labeling).

## How to run BlockMaker
- 🪟 **Windows users:**
    - Install [Python 3.13](https://www.python.org/downloads/) (earlier versions may or may not work).
    - Download this repository as a zip file, and extract the contents somewhere.
    - Double-click the file "block_maker.bat". This will create a virtual environment, automatically install the required dependencies, and then run the program.
- 🐧 **Linux users:** you can figure this out.
- 🍎 **MacOS users:** I wouldn't know...

## Usage
Below are short descriptions of the different options in BlockMaker.

- 📁 **Output directory for block files**
    - Select the directory where generated block files will be saved. By default, it is the directory containing "block_maker.py".
- 📜 **Import text file with sequences**
    - Import a text (.txt) file with one-letter peptide sequences.
    - *Note:* Importing a new text file after a previous one has already been imported will automatically clear the table listing the sequences.
- ✏️ **Add peptide sequence manually**
    - Manually add a one-letter peptide sequence to the table. Enter the peptide sequence and then click the **"+"** button.
- 🧪 **Amino acid modifications**
    - Choose modifications for amino acid residues:
        - Cysteine treatment.
        - Methionine oxidation (one extra oxygen atom per M residue).
        - Stable isotope labeling with carbon-13 and nitrogen-15. When an amino acid is checked, all corresponding residues are assumed to be fully labeled (i.e., all carbons are C-13 and all nitrogens are N-15).

The table lists all block names and their corresponding sequences. 
When a peptide sequence is added to the table, a block name is generated automatically based on the first four letters of the sequence. 
If this results in a duplicate block name, a suffix ("_b", "_c", etc.) is added. 
All entries in the table can be edited via double-clicking, allowing you to specify your own block names or to correct a sequence. 
By clicking the corresponding buttons, you can delete either a selection of entries or all of them.

The **"Generate block files"** will create block files based on the sequences and modifications specified in the table. 
Ensure all desired modifications and sequences are correctly entered before clicking this button.

After creating the block files, you can check the generated log file ("BlockMaker.log") to confirm that you made the correct choices.