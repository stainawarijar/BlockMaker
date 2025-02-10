import os
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

        # Set the initial output directory to the current directory
        self.ui.listWidget_outputdir.addItem(os.getcwd())

        # Connect button click signals to functions
        self.ui.toolButton_openfile.clicked.connect(self.open_text_file)
        self.ui.pushButton_addsequence.clicked.connect(self.add_sequence)
        self.ui.pushButton_deletesequence.clicked.connect(self.delete_sequence)
        self.ui.pushButton_deleteall.clicked.connect(self.delete_all)
        self.ui.toolButton_openoutputdir.clicked.connect(self.open_output_dir)
        self.ui.pushButton_generateblocks.clicked.connect(self.generate_blocks)

        # Connect edited entry in sequence table to function check_sequence_table_edit
        self.ui.tableWidget_sequences.itemChanged.connect(self.check_sequence_table_edit)


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


    def open_output_dir(self):
        '''
        Open a file dialog for selecting an output directory.
        Display the location of the directory in the UI.
        '''
        dir_path = QFileDialog.getExistingDirectory(None, "Select Output Directory", "")
        if dir_path:
            # Clear existing entry
            self.ui.listWidget_outputdir.clear()
            # Add directory location
            self.ui.listWidget_outputdir.addItem(dir_path)


    def open_text_file(self):
        '''
        Open a file dialog for selecting a text file with peptide sequences.
        Display the location of the file in the UI.
        Read the peptide sequences line by line, check their validity and add them to the list.
        '''
        file_path, _ = QFileDialog.getOpenFileName(None, "Select a Text File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            # If a text file was loaded previously, clear existing entries
            if self.ui.listWidget_filelocation.count() > 0:
                self.delete_all()
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
                        self.create_table_entry(sequence)


    def add_sequence(self):
        '''Check validity of manual input sequence and add it to table.'''
        sequence = self.ui.lineEdit_sequence.text().strip().upper()
        invalid = utils.check_sequence_validity(sequence)
        if (len(invalid["positions"])) > 0:
            # Show warning
            self.show_warning(
                title = "Invalid sequence",
                text = utils.generate_invalid_sequence_warning(invalid, sequence),
                informative_text = "Adjust the sequence and try again."
                )
        elif sequence == "":
            pass  # Do nothing in case of empty sequence
        elif any(
            self.ui.tableWidget_sequences.item(row, 1) and 
            self.ui.tableWidget_sequences.item(row, 1).text() == sequence 
            for row in range(self.ui.tableWidget_sequences.rowCount())
        ):
            pass  # Do nothing in case of duplicate sequence
        else:
            self.create_table_entry(sequence)
    

    def create_table_entry(self, sequence):
        '''
        Create an editable entry in the table for a valid sequence.
        Automatically generates a block name.
        '''
        # Add sequence to table (editable)
        row_position = self.ui.tableWidget_sequences.rowCount()
        self.ui.tableWidget_sequences.insertRow(row_position)
        self.ui.tableWidget_sequences.setItem(row_position, 1, QTableWidgetItem(sequence))
        # Add a block name (editable), first four letters of peptide by default
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


    def delete_sequence(self):
        '''Delete selected rows from the sequence table.'''
        # Get indices of selected rows
        # A set is used because it automatically removes duplicate indices (when both block and sequence in a row are selected)
        selected_rows = set(index.row() for index in self.ui.tableWidget_sequences.selectedIndexes())
        # Remove entries from table
        # Reverse order iteration is used to prevent issues with indices shifting when rows are removed from the table
        for row in sorted(selected_rows, reverse = True):
            self.ui.tableWidget_sequences.removeRow(row)


    def delete_all(self):
        '''Remove all block names and corresponding sequences from the sequence table.'''
        self.ui.tableWidget_sequences.setRowCount(0)
        self.ui.listWidget_filelocation.clear()


    def check_sequence_table_edit(self, item):
        '''Check the validity of an edited sequence entry in the table.'''
        # Get row and column number of the changed item
        row = item.row()
        column = item.column() 
        # Temporarily disconnect the signal to prevent recursion
        # Because changing background color of an entry triggers signal
        self.ui.tableWidget_sequences.itemChanged.disconnect(self.check_sequence_table_edit)
        # Check changes
        if column == 0:  # The block name was edited
            # Remove leading/trailing spaces
            block_name = item.text().strip()
            self.ui.tableWidget_sequences.item(row, column).setText(block_name)
            # Check its validity: only letters or underscores 
            valid_block = all(char.isalpha() or char == "_" for char in block_name)
            if not valid_block or block_name == "":
                # Highlight the corresponding entry
                self.ui.tableWidget_sequences.item(row, column).setBackground(Qt.GlobalColor.red)
                # Show warning if the entry is invalid (not if it is empty)
                self.show_warning(
                    title = "Invalid block name",
                    text = "Block names may only contain letters and underscores.",
                    informative_text = f"Adjust block name '{block_name}' or no file will be created for it!"
                )
            else:
                # Remove highlight
                self.ui.tableWidget_sequences.item(row, column).setBackground(Qt.GlobalColor.transparent)
        else:  # The sequence was edited
            # Remove trailing/leading spaces and capitalize
            sequence = item.text().strip().upper()
            self.ui.tableWidget_sequences.item(row, column).setText(sequence)
            # Check validity of the sequence
            invalid = utils.check_sequence_validity(sequence)
            if (len(invalid["positions"])) > 0 or sequence == "":
                # Highlight the corresponding entry
                self.ui.tableWidget_sequences.item(row, column).setBackground(Qt.GlobalColor.red)
                if len(invalid["positions"]) > 0:
                # Show warning in case of invalid entry (not if it is empty)
                    self.show_warning(
                        title = "Invalid sequence",
                        text = utils.generate_invalid_sequence_warning(invalid, sequence),
                        informative_text = "Adjust this sequence or no block file will be created for it!"
                    )
            else:
                # Remove highlight
                self.ui.tableWidget_sequences.item(row, column).setBackground(Qt.GlobalColor.transparent)
        # Reconnect the signal
        self.ui.tableWidget_sequences.itemChanged.connect(self.check_sequence_table_edit)
    

    def generate_blocks(self):
        '''Generate block files for valid entries in the sequence table'''
        # TODO: methionine oxidation and heavy isotope labeling
        # Get a dictionary with valid sequence entries
        sequences = self.valid_sequence_entries()
        for block_name, sequence in sequences.items():
            # Create instance of Peptide class
            peptide = Peptide(
                block_name, sequence,
                cysteine_treatment = self.ui.comboBox_C_treatment.currentText(),
                methionine_oxidation = self.ui.radioButton_M_oxidation.isChecked()  # Boolean
            )
            # Write message to log file
            utils.write_to_log(f"Start processing block '{block_name}' with sequence '{sequence}'...")
            if "C" in peptide.sequence:
                if peptide.cysteine_treatment == "Iodo- or chloroacetamide":
                    utils.write_to_log("Cysteines treated with iodo- or chloroacetamide.")
                elif peptide.cysteine_treatment == "Iodo- or chloroacetic acid":
                    utils.write_to_log("Cysteines treated with iodo- or chloroacetic acid.")
                else:
                    utils.write_to_log("Cysteines untreated (reduced form).")
            if "M" in peptide.sequence and peptide.methionine_oxidation:
                utils.write_to_log("Methionines oxidized.")
            # Create block file
            peptide.write_block_file(output_dir = self.ui.listWidget_outputdir.item(0).text())


    def valid_sequence_entries(self):
        '''
        Determine valid entries in the sequence tableWidget.
        Return a dictionary with block names as keys and their corresponding sequences as values.
        '''
        valid = {}  # Initiate empty dictionary
        for row in range(self.ui.tableWidget_sequences.rowCount()):
            block_name_item = self.ui.tableWidget_sequences.item(row, 0)
            sequence_item = self.ui.tableWidget_sequences.item(row, 1)
            # Check that neither block_name nor sequence are highlighted in red
            if (
                block_name_item and sequence_item and
                block_name_item.background().color() != Qt.GlobalColor.red and
                sequence_item.background().color() != Qt.GlobalColor.red
            ):
                valid[block_name_item.text()] = sequence_item.text()
        return valid
