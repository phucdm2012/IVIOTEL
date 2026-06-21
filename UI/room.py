from PySide6.QtWidgets import *
from PySide6.QtGui import *
from .table import DataTable
from .search import SearchBar
from .title import TitleWidget
from backend.room import Room
from backend.signal import SearchSignal, ReloadTable


class RoomPage(QWidget):
    def __init__(self):
        super().__init__()
        self.room_page_main_layout = QVBoxLayout()
        self.room_page_data_table_layout = QHBoxLayout()

        self.room = Room()
        self.room_name = self.room.get_opening_room()

        self.search_signal = SearchSignal()
        self.reload_table_signal = ReloadTable()

        self.create_room_name_label()
        self.room_page_data_table_layout.addWidget(self.number_of_room_label)

        self.room_page_main_layout.addLayout(self.room_page_data_table_layout)

        self.searchBar = SearchBar(self.search_signal, self.reload_table_signal)
        self.room_page_main_layout.addWidget(self.searchBar)

        self.data_table = DataTable(self.search_signal, self.reload_table_signal)
        self.room_page_main_layout.addWidget(self.data_table)

        self.setLayout(self.room_page_main_layout)

        self.customPage()
        self.customContent()

    def create_room_name_label(self):
        self.number_of_room_label = TitleWidget(self.reload_table_signal)

    def customPage(self):
        self.room_page_main_layout.setContentsMargins(0, 0, 0, 0)

    def customContent(self):
        self.room_page_data_table_layout.setContentsMargins(0, 0, 0, 0)
