from PySide6.QtWidgets import *
from PySide6.QtCore import *


class DiaLogChangeNumberOfRoom(QDialog):
    def __init__(self, current_number_of_room: int):
        super().__init__()
        self.setWindowTitle('Cập nhật số lượng phòng')
        self.resize(200, 100)
        self.current_number_of_room = current_number_of_room

        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowCloseButtonHint)

        self.dialog_main_layout = QVBoxLayout()
        self.dialog_input_layout = QHBoxLayout()

        self.dialog_input_layout.setContentsMargins(8, 8, 8, 8)
        self.dialog_main_layout.setContentsMargins(8, 8, 8, 8)

        self.new_number_of_room_input_label = QLabel('Nhập số lượng phòng mới: ')

        self.new_number_of_room_input = QSpinBox(self)
        self.new_number_of_room_input.setMinimum(1)
        self.new_number_of_room_input.setValue(int(self.current_number_of_room))

        self.dialog_input_layout.addWidget(self.new_number_of_room_input_label)
        self.dialog_input_layout.addWidget(self.new_number_of_room_input)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.dialog_main_layout.addLayout(self.dialog_input_layout)
        self.dialog_main_layout.addWidget(self.button_box)
        self.setLayout(self.dialog_main_layout)

    @staticmethod
    def get_new_number_of_room_value(current_number_of_room):
        dialog = DiaLogChangeNumberOfRoom(current_number_of_room)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            return dialog.new_number_of_room_input.value(), True
        return current_number_of_room, False
