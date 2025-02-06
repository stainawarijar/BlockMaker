from PyQt6.QtWidgets import QMainWindow
from .gui import Ui_MainWindow
from .. import utils
from ..peptide import Peptide


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self) 

        # Connect button click signals
        self.ui.toolButton_openfile.clicked.connect(self.open_text_file)
        self.ui.pushButton_addsequence.clicked.connect(self.add_sequence)
        self.ui.pushButton_deletesequence.clicked.connect(self.delete_sequence)
        self.ui.toolButton_openoutputdir.clicked.connect(self.open_output_dir)
        self.ui.pushButton_generateblocks.clicked.connect(self.generate_blocks)

    # Functions for buttons
    def open_text_file(self):
        print("Open a text file.")

    def add_sequence(self):
        print("Add a sequence.")

    def delete_sequence(self):
        print("Delete a sequence")

    def open_output_dir(self):
        print("Select output directory.")

    def generate_blocks(self):
        print("Generate files.")


# lineEdit_file
# lineEdit_sequence
# listWidget_sequences
# comboBox_C_treatment
# radioButton_M_oxidation
# checkBox_<amino acid>
# lineEdit_outputdir
# pushButton_generateblocks
