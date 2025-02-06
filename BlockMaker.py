import sys
from PyQt6.QtWidgets import QApplication, QStyleFactory
from BlockMaker.gui.main_window import MainWindow


def main():
    # Create instance of QApplication
    app = QApplication(sys.argv)

    # Set the application style to Fusion
    app.setStyle(QStyleFactory.create("Fusion"))

    # Create and show the main window
    main_window = MainWindow()
    main_window.show()

    # Start the application's event loop and exit the program when the loop ends
    sys.exit(app.exec())



if __name__ == "__main__":
    main()
    
