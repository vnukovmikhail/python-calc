import math, random
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QSizePolicy, QLineEdit, QStatusBar
from PyQt6.QtGui import QFont

class QCalculatorWidget(QWidget):
    def __init__(self, status: QStatusBar):
        super().__init__()
        self.status = status
        self.memory = 0.0
        self.expr = ''

        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setFixedHeight(50)
        self.display.setFont(QFont('monospace', 16))
        self.display.setTextMargins(5, 5, 5, 5)

        rows = [
            ["(", ")", "%", "CE", "C"],
            ["7", "8", "9", "÷", "^"],
            ["4", "5", "6", "×", "√"],
            ["1", "2", "3", "−", "π"],
            ["0", ".", "=", "+", ""],
            ["sin", "cos", "tan", "exp", "ln"],
            ["log", "abs", "rand", "", ""],
        ]

        grid = QGridLayout(self)
        grid.addWidget(self.display, 0, 0, 1, 5)

        mem_buttons = ["MC", "MR", "MS", "M+", "M-"]
        for c, label in enumerate(mem_buttons):
            btn = QPushButton(label)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            btn.clicked.connect(lambda _, t=label: self.on_memory(t))
            grid.addWidget(btn, 1, c)

        for i, row in enumerate(rows, start=2):
            for j, char in enumerate(row):
                btn = QPushButton(char)
                btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

                btn.clicked.connect(lambda _, ch=char:self.on_button(ch))

                grid.addWidget(btn, i, j)

    def on_memory(self, key: str):
        try:
            current = float(self.display.text()) if self.display.text() else 0.0
        except Exception:
            current = 0.0

        match key:
            case "MC":
                self.memory = 0.0
            case "MR":
                self.expr = str(self.memory)
                self.display.setText(self.expr)
            case "MS":
                self.memory = current
            case "M+":
                self.memory += current
            case "M-":
                self.memory -= current

        self.status.showMessage(f'Memory was updated! Current value: {self.memory}', 5000)

    def on_button(self, label: str):
        match label:
            case 'C':
                self.expr = self.expr[:-1]
                self.display.setText(self.expr)
            case 'CE':
                self.expr = ""
                self.display.setText("")
            case '√':
                self.expr += 'sqrt('
                self.display.setText(self.expr)
            case 'sin' | 'cos' | 'tan' | 'ln' | 'log' | 'abs':
                self.expr += f'{label}('
                self.display.setText(self.expr)
            case '=':
                try:
                    expr = self.prepare_expr(self.expr)
                    result = eval(expr, {"__builtins__": None}, self.safe_env())
                    self.display.setText(str(result))
                    self.expr = str(result)
                except Exception as e:
                    self.display.setText(f'Error: {e}')
                    self.expr = ""
            case _:
                self.expr += label
                self.display.setText(self.expr)

    def prepare_expr(self, expr: str) -> str:
        expr = expr.replace("×", "*").replace("÷", "/").replace("−", "-")
        expr = expr.replace("^", "**")
        expr = expr.replace("π", "math.pi")
        expr = expr.replace("sqrt(", "math.sqrt(")
        return expr

    def safe_env(self):
        return {
            'math': math,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'exp': math.exp,
            'ln': math.log,
            'log': math.log10,
            'sqrt': math.sqrt,
            'abs': abs,
            'rand': random.random,
        }