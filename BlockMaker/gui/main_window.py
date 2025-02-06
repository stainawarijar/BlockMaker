from PyQt6.QtWidgets import QMainWindow, QFileDialog
from .gui import Ui_MainWindow
from .. import utils
from ..peptide import Peptide


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self) 

        # Connect button click signals to functions
        self.ui.toolButton_openfile.clicked.connect(self.open_text_file)
        self.ui.pushButton_addsequence.clicked.connect(self.add_sequence)
        self.ui.pushButton_deletesequence.clicked.connect(self.delete_sequence)
        self.ui.toolButton_openoutputdir.clicked.connect(self.open_output_dir)
        self.ui.pushButton_generateblocks.clicked.connect(self.generate_blocks)

    # Functions for buttons
    def open_text_file(self):
        '''
        Open a file dialog for selecting a text file with peptide sequences.
        Display the location of the file in the UI.
        Read the peptide sequences line by line, check their validity and add them to the list.
        '''
        file_path, _ = QFileDialog.getOpenFileName(None, "Select a Text File", "", "Text Files (*.txt);;All Files (*)")
        self.ui.listWidget_filelocation.clear()
        self.ui.listWidget_filelocation.addItem(file_path)
        with open(file_path, "r") as file:
            for line in file:
                # TODO Check sequence validity
                # Add to sequence list
                self.ui.listWidget_sequences.addItem(line)


    def add_sequence(self):
        print("Add a sequence.")

    def delete_sequence(self):
        print("Delete selected sequence")

    def open_output_dir(self):
        print("Select an output directory.")

    def generate_blocks(self):
        print("Generate block files.")

