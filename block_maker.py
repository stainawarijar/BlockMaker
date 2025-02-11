import sys
from PyQt6.QtWidgets import QApplication, QStyleFactory
from block_maker.gui.main_window import MainWindow


def main():
    # Create instance of QApplication.
    app = QApplication(sys.argv)
    # Set the application style to Fusion.
    app.setStyle(QStyleFactory.create("Fusion"))
    # Create and show the main window.
    main_window = MainWindow()
    main_window.show()
    # Start application's event loop, exit program when the loop ends.
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
    
