import sys
import time
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QSize

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hello World Example")
        self.setFixedSize(QSize(500, 200))  # Устанавливаем фиксированный размер окна

        self.label = QLabel("Hello, World!")
        self.label.setAlignment(Qt.AlignCenter)

        self.button = QPushButton("OK")
        self.button.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()