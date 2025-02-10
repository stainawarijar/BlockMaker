from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem
from PyQt6.QtCore import Qt
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
        self.ui.pushButton_deleteall.clicked.connect(self.delete_all)
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
        if file_path:
            # Clear existing table entries if a text file was loaded previously
            if self.ui.listWidget_filelocation.count() > 0:
                self.ui.tableWidget_sequences.clearContents()
                self.ui.tableWidget_sequences.setRowCount(0)
                self.ui.listWidget_filelocation.clear()
            # Add file location
            self.ui.listWidget_filelocation.addItem(file_path)
            # Read sequences from file
            with open(file_path, "r") as file:
                for line in file:
                    # Remove leading or trailing spaces, and capitalize letters
                    sequence = line.strip().upper()
                    # Skip empty lines
                    if sequence == "":
                        continue
                    # Check if the sequence is not a duplicate
                    elif any(
                        self.ui.tableWidget_sequences.item(row, 1) and 
                        self.ui.tableWidget_sequences.item(row, 1).text() == sequence 
                        for row in range(self.ui.tableWidget_sequences.rowCount())
                    ):
                        continue
                    else:
                        # Check validity of the sequence
                        invalid = utils.check_sequence_validity(sequence)
                        if len(invalid["positions"]) > 0:
                            # Show a warning
                            self.show_warning(
                                title = "Oops!",
                                text = utils.generate_invalid_sequence_warning(invalid, sequence),
                                informative_text = ("Adjust this sequence or no block file will be created for it!")
                            )
                        # Add sequence to table (editable)
                        # Invalid sequences are still added because they can be modified in the table
                        row_position = self.ui.tableWidget_sequences.rowCount()
                        self.ui.tableWidget_sequences.insertRow(row_position)
                        self.ui.tableWidget_sequences.setItem(row_position, 1, QTableWidgetItem(sequence))
                        # Add a block name (editable)
                        # First four letters of peptide by default
                        # If already present, add "_b", "_c" etc as suffix
                        block_name = sequence[0:4]
                        suffix = "b"
                        while any(
                            self.ui.tableWidget_sequences.item(row, 0) and 
                            self.ui.tableWidget_sequences.item(row, 0).text() == block_name 
                            for row in range(self.ui.tableWidget_sequences.rowCount())
                        ):
                            block_name = sequence[0:4] + '_' + suffix
                            suffix = chr(ord(suffix) + 1)
                        self.ui.tableWidget_sequences.setItem(row_position, 0, QTableWidgetItem(block_name))
                        # If the sequence is invalid, highlight the row in red
                        if len(invalid["positions"]) > 0:
                            for column in range(self.ui.tableWidget_sequences.columnCount()):
                                self.ui.tableWidget_sequences.item(row_position, column).setBackground(Qt.GlobalColor.red)

    def add_sequence(self):
        print("Add a sequence.")
        
    def delete_sequence(self):
        print("Delete selected sequence.")

    def delete_all(self):
        print("Delete all sequences.")

    def open_output_dir(self):
        print("Select an output directory.")


    def generate_blocks(self):
        print("Generate block files.")

