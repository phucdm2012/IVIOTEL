from PySide6.QtWidgets import *
from .room import RoomPage


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.main_window_layout = QVBoxLayout()

        self.createAndAddRoomPageToLayout()
        self.setLayout(self.main_window_layout)
        self.customUI()

    def createAndAddRoomPageToLayout(self):
        self.room_page = RoomPage()
        self.main_window_layout.addWidget(self.room_page)

    def customUI(self):
        self.main_window_layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
