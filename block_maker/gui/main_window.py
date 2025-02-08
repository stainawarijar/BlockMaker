from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
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


    def show_warning(self, title, text, informative_text):
        '''Show a warning message box.'''
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setText(f"<b>{text}</b>")
        msg_box.setInformativeText(informative_text)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.resize(800, 200)
        msg_box.exec()


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
        if file_path:
            # Clear previous sequence list
            self.ui.listWidget_sequences.clear()
            # Read sequences from file
            with open(file_path, "r") as file:
                for line in file:
                    # Remove leading or trailing spaces, and capitalize letters
                    sequence = line.strip().upper()
                    # Skip empty lines
                    if sequence == "":
                        continue
                    # Check validity of the sequence
                    invalid = utils.check_sequence_validity(sequence)
                    if len(invalid["positions"]) > 0:
                        # Show a warning
                        self.show_warning(
                            title = "Oops!",
                            text = utils.generate_invalid_sequence_warning(invalid, sequence),
                            informative_text = (
                                "Please adjust your text file, "
                                "or no block file will be created for this sequence!"
                            )
                        )
                    else:
                        # Add to sequence list
                        self.ui.listWidget_sequences.addItem(sequence)


    def add_sequence(self):
        print("Add a sequence.")


    def delete_sequence(self):
        print("Delete selected sequence")


    def open_output_dir(self):
        print("Select an output directory.")


    def generate_blocks(self):
        print("Generate block files.")

