from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from backend.room import Room
from backend.signal import ReloadTable
from backend.title import TitleLogic


class ClickableLabel(QLabel):
    clicked = Signal()

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()


class TitleWidget(QStackedWidget):
    def __init__(self, reload_table_signal: ReloadTable):
        super().__init__()
        self.custom_title_widget()
        self.room = Room()
        self.opening_room = self.room.get_opening_room()
        self.title_widget_0 = QWidget()
        self.title_widget_1 = QWidget()

        self.title_layout_0 = QHBoxLayout()
        self.title_layout_1 = QHBoxLayout()

        self.title_widget_0.setLayout(self.title_layout_0)
        self.title_widget_1.setLayout(self.title_layout_1)
        self.title_logic = TitleLogic(table_reload_signal=reload_table_signal)

        self.create_title_label()
        self.create_title_input()

        self.custom_room_name_label()

        self.timer = QTimer(self)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.change_title_label_to_current_room)
        self.timer.start()

        self.addWidget(self.title_widget_0)
        self.addWidget(self.title_widget_1)
        self.setCurrentIndex(0)

        self.title_input.editingFinished.connect(self.input_complete)
        self.title_label.mouseDoubleClickEvent = self.change_to_input
        self.title_label.clicked.connect(lambda: self.change_to_input(None))

    def create_title_label(self):
        self.title_label = ClickableLabel(f"Phòng {self.opening_room}")

        self.title_label.setCursor(Qt.CursorShape.PointingHandCursor)
        self.title_layout_0.addWidget(self.title_label)

    def create_title_input(self):
        self.title_input_label = QLabel('Phòng')
        self.title_input = QSpinBox(self)

        self.title_input.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding)

        min_val = 1
        max_val = max(1, int(self.title_logic.get_number_of_rooms()))

        self.title_input.setMinimum(min_val)
        self.title_input.setMaximum(max_val)

        cur_val = int(self.opening_room) if int(self.opening_room) >= min_val else min_val
        self.title_input.setValue(cur_val)

        self.title_layout_1.addWidget(self.title_input_label)
        self.title_layout_1.addWidget(self.title_input)
        self.title_layout_1.addStretch()

    def change_to_input(self, event=None):
        if event is None or event.button == Qt.MouseButton.LeftButton:
            self.setCurrentIndex(1)
            max_val = max(1, int(self.title_logic.get_number_of_rooms()))
            self.title_input.setMaximum(max_val)
            self.title_input.setFocus()

    def input_complete(self):
        val = self.title_input.value()
        self.title_logic.go_to_new_room(val)
        self.setCurrentIndex(0)

    def change_title_label_to_current_room(self):
        opening_room = self.room.get_opening_room()
        if opening_room != self.opening_room:
            self.opening_room = opening_room
            self.title_label.setText(f'Phòng {self.opening_room}')

    def custom_room_name_label(self):
        self.title_label_font = QFont("Arial", 18, QFont.Weight.Bold)
        self.title_label.setFont(self.title_label_font)
        self.title_input_label.setFont(self.title_label_font)

        self.title_label.setContentsMargins(8, 8, 8, 0)
        self.title_input_label.setContentsMargins(8, 8, 8, 0)

    def custom_title_widget(self):
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
