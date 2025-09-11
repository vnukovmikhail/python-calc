from PyQt6.QtWidgets import QWidget, QStatusBar, QGridLayout, QComboBox, QPushButton, QLabel, QLineEdit, QVBoxLayout

class QTranslatorWidget(QWidget):
    def __init__(self, status: QStatusBar):
        super().__init__()
        self.status = status

        vbox = QVBoxLayout(self)

        grid = QGridLayout()
        self.input_edit = QLineEdit()
        self.input_edit.setPlaceholderText('Enter number...')
        grid.addWidget(QLabel('Number:'), 0, 0)
        grid.addWidget(self.input_edit,   0, 1, 1, 3)
        self.from_base = QComboBox()
        self.to_base = QComboBox()
        for b in [2, 8, 10, 16]:
            self.from_base.addItem(str(b))
            self.to_base.addItem(str(b))
        grid.addWidget(QLabel('From system:'), 1, 0)
        grid.addWidget(self.from_base,         1, 1)
        grid.addWidget(QLabel('To system:'),   1, 2)
        grid.addWidget(self.to_base,           1, 3)
        button = QPushButton('Convert!')
        button.clicked.connect(self.convert)
        grid.addWidget(button, 2, 0, 1, 4)
        self.result_label = QLabel('Result: ')
        grid.addWidget(self.result_label, 3, 0, 1, 4)

        vbox.addLayout(grid)
        vbox.addStretch()

    def convert(self):
        num_str = self.input_edit.text().strip()
        try:
            base_from = int(self.from_base.currentText())
            base_to = int(self.to_base.currentText())

            num = int(num_str, base_from)

            match base_to:
                case 2: 
                    result = bin(num)[2:]
                case 8:
                    result = oct(num)[2:]
                case 10:
                    result = str(num)
                case 16:
                    result = hex(num)[2:].upper()
                case _:
                    result = 'Error::'

            self.result_label.setText(f'Result: {result}')
        except Exception:
            self.result_label.setText('Error: Invalid number')