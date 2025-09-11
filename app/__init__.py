import time
from PyQt6.QtWidgets import QMainWindow
from app.widgets.q_central_widget import QCentralWidget

APP_START_TIME = time.perf_counter()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('PyQt6 calculator')
        self.setMinimumSize(300, 150)

        status = self.statusBar()
        elapsed = time.perf_counter() - APP_START_TIME
        status.showMessage(f'Program started in {elapsed:.3f} seconds', 3000)

        self.setCentralWidget(QCentralWidget(status=status))