from PySide6.QtWidgets import *
from PySide6.QtGui import *
import datetime as dt
import win32gui
from backend.path import PATH_TO_ICON
from backend.search import Search
from backend.signal import SearchSignal, ReloadTable

now = dt.datetime.now()


class SearchBar(QWidget):
    def __init__(self, search_signal: SearchSignal, reload_table_signal: ReloadTable):
        super().__init__()
        self.searchbar_layout = QHBoxLayout()
        self.searcher = Search()

        self.search_signal = search_signal
        self.reload_table_signal = reload_table_signal
        self.fluent_font = QFont('Segoe Fluent Icon')

        self.month_search_box_label = QLabel('Tháng\t')

        self.month_search_box = QSpinBox(minimum=0, maximum=12)
        self.month_search_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.month_search_box.setValue(now.month)

        self.year_search_box_label = QLabel('Năm\t')

        self.year_search_box = QDoubleSpinBox()
        self.year_search_box.setDecimals(0)
        self.year_search_box.setMaximum(float('inf'))
        self.year_search_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.year_search_box.setValue(now.year)

        self.search_button = QPushButton('\uE721')
        self.search_button.setFont(self.fluent_font)
        self.search_button.setToolTip('Tìm')
        self.search_button.clicked.connect(self.search)

        self.show_all_btn = QPushButton('\uE8c4')
        self.show_all_btn.setFont(self.fluent_font)
        self.show_all_btn.setToolTip('Hiển thị tất cả dữ liệu của phòng này')
        self.show_all_btn.clicked.connect(lambda: self.reload_table_signal.reload_table_sigal.emit())

        self.add_new_month_button = QPushButton('\uE948')
        self.add_new_month_button.setToolTip('Tháng kế')
        self.add_new_month_button.clicked.connect(lambda: self.searcher.add_new_month(self.reload_table_signal))

        self.export_excel_button = QPushButton('\uEde1')
        self.export_excel_button.setToolTip('Xuất Excel')
        self.export_excel_button.clicked.connect(self.searcher.export_excel)

        self.searchbar_layout.addWidget(self.month_search_box_label)
        self.searchbar_layout.addWidget(self.month_search_box)
        self.searchbar_layout.addWidget(self.year_search_box_label)
        self.searchbar_layout.addWidget(self.year_search_box)
        self.searchbar_layout.addWidget(self.search_button)
        self.searchbar_layout.addWidget(self.show_all_btn)
        self.searchbar_layout.addStretch()
        self.searchbar_layout.addWidget(self.add_new_month_button)
        self.searchbar_layout.addWidget(self.export_excel_button)
        self.searchbar_layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(8, 0, 8, 0)
        self.setLayout(self.searchbar_layout)

    def search(self):
        year = int(self.year_search_box.value())
        month = int(self.month_search_box.value())
        searched_value = self.searcher.search(year, month)

        self.search_signal.searched_value.emit(searched_value)
