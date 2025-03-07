# -*- coding: utf-8 -*-
import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox)
from PyQt5.QtCore import Qt, QSize

class DeviceInfoDialog(QWidget):
    def __init__(self, devices_id, device_model_name, devices_serial_number, num_devices):
        super().__init__()
        self.setWindowTitle("Информация об устройствах")
        self.setFixedSize(QSize(400, 300))

        self.devices_id = devices_id
        self.device_model_name = device_model_name
        self.devices_serial_number = devices_serial_number
        self.num_devices = num_devices

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Labels for Device Information
        id_label = QLabel(f"ID устройства: {self.devices_id}")
        model_label = QLabel(f"Модель устройства: {self.device_model_name}")
        serial_label = QLabel(f"Серийный номер: {self.devices_serial_number}")
        num_devices_label = QLabel(f"Количество доступных устройств: {self.num_devices}")

        # Input field for device number
        self.input_label = QLabel("Введите ID устройства, для подключения:")
        self.input_label.setStyleSheet("font-weight: bold;")
        self.input_field = QLineEdit()

        # Button to confirm the device number
        self.connect_button = QPushButton("Подключиться")
        self.connect_button.clicked.connect(self.on_connect)

        # Message label to show the input is invalid
        self.message_label = QLabel("")
        self.message_label.setStyleSheet("color: red;")  # Set text color to red

        # Layout
        layout.addWidget(id_label)
        layout.addWidget(model_label)
        layout.addWidget(serial_label)
        layout.addWidget(num_devices_label)
        layout.addWidget(self.input_label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.connect_button)
        layout.addWidget(self.message_label)
        self.setLayout(layout)

    def on_connect(self):
        try:
            nConnectionNum = int(self.input_field.text())
            if nConnectionNum >= self.num_devices:
                self.message_label.setText(f"Введенное значение больше, чем количество доступных устройств.")
            else:
                # Emit a signal or call a function with nConnectionNum
                # For now, just print
                self.accept_and_return_value(nConnectionNum)
        except ValueError:
            self.message_label.setText("Пожалуйста, введите целое число.")

    def accept_and_return_value(self, value):
      self.result = value
      self.close()
      QApplication.instance().quit() # Важно: останавливаем цикл событий

def show_device_info_dialog(devices_id, device_model_name, devices_serial_number, num_devices):
    """
    Показывает диалоговое окно с информацией об устройстве и возвращает введенный номер устройства.
    """
    app = QApplication.instance() # Проверяем существует ли QApplication
    if app is None:
        app = QApplication(sys.argv)

    dialog = DeviceInfoDialog(devices_id, device_model_name, devices_serial_number, num_devices)
    dialog.show()
    app.exec_() # Запускаем цикл обработки событий.

    return dialog.result if hasattr(dialog, 'result') else None # возвращает результат ввода
    # sys.exit(app.exec_())


if __name__ == '__main__':
    # Пример использования (замените фиктивными данными)
    devices_id = 0
    device_model_name = "MV-DP2060-01H"
    devices_serial_number = "00DA2925019"
    num_devices = 1

    device_number = show_device_info_dialog(devices_id, device_model_name, devices_serial_number, num_devices)

    if device_number is not None:
        print(f"Выбранный номер устройства: {device_number}")
    else:
        print("Ввод отменен или произошла ошибка.")