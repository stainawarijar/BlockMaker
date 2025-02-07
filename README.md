![Experimental](https://img.shields.io/badge/status-experimental-yellow)

# BlockMaker
BlockMaker is a  simple Python program to make block files for [LaCyTools](<https://pubs.acs.org/doi/10.1021/acs.jproteome.6b00171>), including options for amino acid modifications (cysteine treatment, methionine oxidation and stable isotope labeling).

## How to run BlockMaker?
- 🪟 Windows users:
    - Install [Python 3](https://www.python.org/downloads/).
    - Download this repository as a zip file, and extract the contents somewhere.
    - Double click the file "BlockMaker.bat". This will create a virtual environment, automatically install the required dependencies and then run the program.
- 🐧 Linux users: 
    - Make sure you have [Python 3](https://www.python.org/downloads/) installed.
    - Open a terminal and `cd` to the directory containing "BlockMaker.py".
    - Run the following commands:
        - `python3 -m venv venv` to setup a virtual environment.
        - `source venv/bin/activate` to activate the virtual environment.
        - `pip install -r requirements.txt` do install dependencies.
        - `python3 BlockMaker.py` to launch the program.  
- 🍎 MacOS users: I wouldn´t know...

