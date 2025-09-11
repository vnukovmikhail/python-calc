from PyQt6.QtWidgets import QTabWidget, QLabel, QStatusBar
from app.widgets.q_calc_widget import QCalculatorWidget
from app.widgets.q_translator_widget import QTranslatorWidget

class QCentralWidget(QTabWidget):
    def __init__(self, status: QStatusBar):
        super().__init__()

        self.addTab(QCalculatorWidget(status=status), 'Calculator')
        self.addTab(QTranslatorWidget(status=status), 'Translator')