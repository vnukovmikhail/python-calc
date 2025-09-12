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

        print(math.sin(math.radians(30)))

        rows = [
            ['rad', 'deg', 'sin', 'cos', 'tan'],
            ['log', 'log10', 'log2', '(', ')'],
            ['^', 'C', 'CE', '%', '÷'],
            ['√', '7', '8', '9', '×'],
            ['x!', '4', '5', '6', '−'],
            ['¹/x', '1', '2', '3', '+'],
            ['π', 'ℯ', '0', '.', '='],
        ]

        grid = QGridLayout(self)
        grid.addWidget(self.display, 0, 0, 1, 5)

        rows_m = ['MC', 'MR', 'MS', 'M+', 'M-']
        for c, label in enumerate(rows_m):
            btn = QPushButton(label)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            # btn.setDisabled(True)
            btn.clicked.connect(lambda _, t=label: self.on_memory(t))
            grid.addWidget(btn, 1, c)

        for i, row in enumerate(rows, start=2):
            for j, char in enumerate(row):
                btn = QPushButton(char)
                btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

                btn.clicked.connect(lambda _, ch=char:self.on_button(ch))

                grid.addWidget(btn, i, j)

    def on_memory(self, key: str):
        print('memory')
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

    def prepare_expr(self, expr: str) -> str:
        expr = expr.replace('×', '*').replace('÷', '/').replace('−', '-')
        expr = expr.replace('^', '**')
        expr = expr.replace('π', 'math.pi').replace('ℯ', 'math.e')
        expr = expr.replace('sqrt(', 'math.sqrt(')
        expr = expr.replace('rad(', 'math.degrees(').replace('deg(', 'math.radians(')
        
        return expr
    
    def safe_env(self):
        return {
            'math': math,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'log': math.log,
            'log10': math.log10,
            'log2': math.log2,
        } 
    
    def add_dot(self, ch: str):
        expr = self.prepare_expr(self.expr)
        last_number = expr.split('+')[-1].split('-')[-1].split('*')[-1].split('/')[-1]
        if '.' in last_number:
            return  

        self.expr += ch
        self.display.setText(self.expr)
    
    def calculate(self):
        try:
            expr = self.prepare_expr(self.expr)
            result = eval(expr, {'__builtins__': None}, self.safe_env())
            result = str(round(result, 10))
            self.display.setText(result)
            self.expr = result
        except Exception as e:
            self.display.setText(f'Err: {e.args[0]}')
            self.expr = ""
            
    def on_button(self, label: str):
        match label:
            case 'CE':
                self.expr = self.expr[:-1]
                self.display.setText(self.expr)
            case 'C':
                self.expr = ''
                self.display.setText('')
            case '√':
                self.expr += 'sqrt('
                self.display.setText(self.expr)
            case 'rad' | 'deg' | 'sin' | 'cos' | 'tan' | 'log' | 'log10' | 'log2':
                self.expr += f'{label}('
                self.display.setText(self.expr)
            case '%':
                self.calculate()
                self.expr = str(float(self.expr) / 100)
                self.display.setText(self.expr)
            case 'x!':
                self.calculate()
                try:
                    self.expr = str(math.factorial(int(self.expr)))
                    self.display.setText(self.expr)
                except Exception as e:
                    self.expr = ''
                    self.display.setText(f'Err: {e.args[0]}')
            case '¹/x':
                self.calculate()
                try:
                    self.expr = str(1 / float(self.expr))
                    self.display.setText(self.expr)
                except Exception as e:
                    self.expr = ''
                    self.display.setText(f'Err: {e.args[0]}')
            case '=':
                self.calculate()
            case '.':
                self.add_dot(label)
            case _:
                self.expr += label
                self.display.setText(self.expr)
    