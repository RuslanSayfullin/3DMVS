# -- coding: utf-8 --
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QSize

class MainWindow(QWidget):
    def __init__(self, text="Внимание!"):  # Добавляем параметр text
        super().__init__()
        self.setWindowTitle("Внимание!")
        self.setFixedSize(QSize(500, 200))  # Устанавливаем фиксированный размер окна

        self.label = QLabel(text)  # Используем переданный текст
        self.label.setAlignment(Qt.AlignCenter)

        self.button = QPushButton("OK")
        self.button.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)
        # Устанавливаем флаг, чтобы окно было поверх всех
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)


def show_window(text="Внимание!"):
    """Функция для показа окна с заданным текстом."""
    app = QApplication.instance()  # Проверяем, существует ли уже экземпляр QApplication
    if app is None:
        app = QApplication(sys.argv)  # Создаем, если нет
    window = MainWindow(text)
    window.show()
    app.exec_()  # Важно:  Запускаем цикл событий QApplication только один раз в главном скрипте


if __name__ == '__main__':
    # Пример использования, когда запускаем этот файл напрямую
    show_window("Hello from main!")