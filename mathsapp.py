import random
import typing

import numpy
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from constants import Operation, operations_map
from styles import main_style


class MathScratchPadApp(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.operation: Operation = operations_map[numpy.add.__name__]
        self.num_problems: int = 10
        self.digits: int = 2
        self.current_problem_count: int = 0
        self.total_correct: int = 0
        self.current_answer: typing.Optional[int] = None
        self.user_answer: typing.Optional[int] = None
        self.initUI()

    def initUI(self) -> None:
        self.setWindowTitle("SUPER FUN MATH EXPLOSION!")
        self.setGeometry(100, 100, 600, 400)

        self.scratch_pad = QTextEdit()
        self.scratch_pad.setPlaceholderText("Scratch pad...")
        self.scratch_pad.setMinimumHeight(150)

        self.problem_label = QLabel("Math Problem")
        self.answer_input = QLineEdit()
        self.answer_input.returnPressed.connect(self.check_answer)
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.check_answer)

        self.num_problems_spinbox = QComboBox()
        self.num_problems_spinbox.addItems([str(num) for num in list(range(1, 26))])
        self.num_problems_spinbox.setCurrentText("10")
        self.num_problems_spinbox.currentTextChanged.connect(self.update_num_problems)

        self.digits_spinbox = QComboBox()
        self.digits_spinbox.addItems([str(num) for num in list(range(1, 11))])
        self.digits_spinbox.setCurrentText("2")
        self.digits_spinbox.currentTextChanged.connect(self.update_digits)

        self.operation_combobox = QComboBox()
        self.operation_combobox.addItems(list(operations_map.keys()))
        self.operation_combobox.currentTextChanged.connect(self.update_operation)

        settings_layout = QHBoxLayout()

        total_layout = QLabel("Total")
        total_layout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        settings_layout.addWidget(total_layout)
        settings_layout.addWidget(self.num_problems_spinbox)

        digits_layout = QLabel("Digits")
        digits_layout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        settings_layout.addWidget(digits_layout)
        settings_layout.addWidget(self.digits_spinbox)

        operation_layout = QLabel("Operation")
        operation_layout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        settings_layout.addWidget(operation_layout)
        settings_layout.addWidget(self.operation_combobox)

        answer_layout = QHBoxLayout()
        answer_layout.addWidget(self.problem_label)
        answer_layout.addWidget(self.answer_input)
        answer_layout.addWidget(self.submit_button)

        layout = QVBoxLayout()
        layout.addLayout(settings_layout)
        layout.addWidget(self.scratch_pad)
        layout.addLayout(answer_layout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setStyleSheet(main_style)

        self.current_answer = None
        self.user_answer = None
        self.update_math_problem()

    def update_math_problem(self) -> None:
        lower_bound = 10 ** (self.digits - 1)
        upper_bound = lower_bound * 10 - 1

        if self.operation.fn.__name__ == numpy.divide.__name__:
            min_num = random.randint(lower_bound, upper_bound)
            max_num = min_num * random.randint(2, 9)
            problem_format = f"\n\n{len(str(min_num)) * ' '}{(len(str(max_num)) + 1) * '_'}\n{min_num}|{max_num}"
        else:
            num1 = random.randint(lower_bound, upper_bound)
            num2 = random.randint(lower_bound, upper_bound)
            max_num = max(num1, num2)
            min_num = min(num1, num2)
            problem_format = (
                f"\n  {max_num}\n{self.operation.symbol} {min_num}\n--------\n  "
            )

        self.current_answer = self.operation.fn(max_num, min_num)

        problem_text = f"{max_num} {self.operation.symbol} {min_num} = "

        self.problem_label.setText(problem_text)
        self.scratch_pad.clear()
        self.scratch_pad.append(
            f"Total Correct: {self.total_correct} of {self.num_problems}\n{problem_format}"
        )

    def check_answer(self) -> None:
        try:
            self.user_answer = int(self.answer_input.text())
            if self.user_answer == self.current_answer:
                self.total_correct += 1
                self.update_math_problem()
            else:
                self.scratch_pad.append(
                    f"{self.problem_label.text().replace('=', '!=')}{self.user_answer}"
                )
            if self.num_problems == self.total_correct:
                self.scratch_pad.clear()
                self.scratch_pad.append("All problems completed!")
                self.submit_button.setEnabled(False)
                return
        except ValueError:
            self.scratch_pad.append("Please enter a valid integer.")
        self.answer_input.clear()
        self.answer_input.setFocus()

    def reset(self) -> None:
        self.total_correct = 0
        self.update_math_problem()

    def update_num_problems(self, value: str) -> None:
        self.num_problems = int(value)
        self.reset()

    def update_digits(self, value: str) -> None:
        self.digits = int(value)
        self.reset()

    def update_operation(self, text: str) -> None:
        self.operation = operations_map[text]
        self.reset()
