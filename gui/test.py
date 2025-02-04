import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStyleFactory
from gui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self) 


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set the application style to Fusion
    app.setStyle(QStyleFactory.create("Fusion"))

    # Create and show the main window
    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())

