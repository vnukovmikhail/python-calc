import sys

from PyQt6.QtWidgets import QApplication
from app import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    root = MainWindow()
    root.show()
    sys.exit(app.exec())