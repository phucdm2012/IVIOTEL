from PySide6.QtWidgets import *
from PySide6.QtCore import *
from backend.room import Room
from backend.caculator import Caculator
from backend.path import PATH_TO_ROOM_DATA
from backend.table import RemovedBoardPlaceholder
from backend.signal import SearchSignal, ReloadTable
import numpy as np
import pandas as pd
import datetime as dt
from pathlib import Path

now = dt.datetime.now()


class DataTable(QWidget):
    def __init__(self, search_signal: SearchSignal, reload_table_signal: ReloadTable):
        super().__init__()
        self.room = Room()
        self.room_name = self.room.get_opening_room()
        self.room_data = pd.DataFrame(self.room.get_room_data(str(self.room_name)))
        self.room_data = self.room_data.fillna('')
        self.room.check_number_of_rooms_data_file()

        self.locked_columns = [0, 1, 4, 5]

        self.search_signal = search_signal
        self.reload_table_signal = reload_table_signal

        self.data_table_layout = QVBoxLayout()

        self.create_room_data_table()
        self.custom_data_table()
        self.data_table_layout.addWidget(self.room_data_table)

        self.search_signal.searched_value.connect(self.reload_table_with_search_value)
        self.reload_table_signal.reload_table_sigal.connect(self.reload_table_data)

        self.setLayout(self.data_table_layout)

    def create_room_data_table(self):
        self.room_data = pd.DataFrame(self.room.get_room_data(str(self.room_name)))
        self.room_data.columns = self.room_data.columns.astype(str).str.strip()

        if 'Unnamed: 0' in self.room_data.columns:
            self.room_data = self.room_data.drop('Unnamed: 0', axis=1)

        self.room_data_table = QTableWidget()
        self.room_data_table.setItemDelegate(RemovedBoardPlaceholder(self))
        self.room_data_table.itemChanged.connect(self.caculate_bill)
        room_data = self.room_data.fillna('')
        
        num_rows = len(room_data)
        num_cols = len(room_data.columns) if len(room_data) > 0 else 0
        
        self.room_data_table.setRowCount(num_rows)
        self.room_data_table.setColumnCount(num_cols)
        self.room_data_table.setHorizontalHeaderLabels(room_data.columns.tolist())

        self.set_data_to_board(num_rows, num_cols)

    def custom_data_table(self):
        self.room_data_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.room_data_table.verticalHeader().setVisible(False)
        self.data_table_layout.setContentsMargins(2, 2, 2, 2)

    def caculate_bill(self, item: QTableWidgetItem):
        row = item.row()
        column = item.column()
        column_name = self.room_data_table.horizontalHeaderItem(column).text()

        if column_name not in ['Số điện mới', 'Số điện cũ']:
            return

        try:
            current_value = float(item.text())
        except ValueError:
            return

        self.room_data.at[row, column_name] = current_value
        other_value = self.get_other_value_in_board(row, column_name)

        if other_value == '' or pd.isna(other_value):
            return

        try:
            other_value = float(other_value)
        except ValueError:
            return

        self.caculator = Caculator()
        if column_name == 'Số điện mới':
            bill = self.caculator.caculateElectricityBill(current_value, other_value)
        else:
            bill = self.caculator.caculateElectricityBill(other_value, current_value)

        usage = self.caculator.caculateElectrictyUsage()
        self.update_bill_table(bill, usage, row)

    def get_other_value_in_board(self, row: int, column_name: str):
        if column_name == 'Số điện mới':
            return self.room_data.at[row, 'Số điện cũ']
        return self.room_data.at[row, 'Số điện mới']
        
    def update_bill_table(self, bill: float, usage: float, row: int):
        self.room_data.at[row, 'Tổng điện tiêu thụ'] = usage
        self.room_data.at[row, 'Thành tiền'] = bill

        self.room_data_table.blockSignals(True)
        self.room_data_table.setItem(row, 4, QTableWidgetItem(f'{usage:,.0f}'))
        self.room_data_table.setItem(row, 5, QTableWidgetItem(f'{bill:,.0f}'))
        self.room_data_table.blockSignals(False)

        file_path = Path(PATH_TO_ROOM_DATA).parent / f'room{self.room_name}.csv'
        self.room_data.to_csv(file_path, index=False)

    def reload_table_with_search_value(self, searched_data: pd.DataFrame):
        self.room_data = searched_data.fillna('')

        num_rows = len(self.room_data)
        num_cols = len(self.room_data.columns)

        self.room_data_table.setRowCount(num_rows)
        self.room_data_table.setColumnCount(num_cols)
        self.room_data_table.setHorizontalHeaderLabels(self.room_data.columns.to_list())

        self.set_data_to_board(num_rows, num_cols)

    def reload_table_data(self):
        """Reload bảng từ dữ liệu mới khi tạo tháng mới"""

        self.room_name = self.room.get_opening_room()
        self.room_data = pd.DataFrame(self.room.get_room_data(str(self.room_name)))
        self.room_data = self.room_data.fillna('')
        
        if 'Unnamed: 0' in self.room_data.columns:
            self.room_data = self.room_data.drop('Unnamed: 0', axis=1)
        
        num_rows = len(self.room_data)
        num_cols = len(self.room_data.columns)
        
        self.room_data_table.setRowCount(num_rows)
        self.room_data_table.setColumnCount(num_cols)
        self.room_data_table.setHorizontalHeaderLabels(self.room_data.columns.tolist())
        
        self.set_data_to_board(num_rows, num_cols)

    def set_data_to_board(self, num_rows: int, num_cols: int):
        if num_rows is None or num_cols is None:
            pass

        self.room_data_table.blockSignals(True)
        for row in range(num_rows):
            for column in range(num_cols):
                value = self.room_data.iloc[row, column]

                if column not in [0, 1]:
                    try:
                        item_value = f'{float(value):,.0f}'
                    except (ValueError, TypeError):
                        item_value = str(value)
                else:
                    item_value = str(value)
                item = QTableWidgetItem(item_value)

                if column in self.locked_columns:
                    flags = item.flags()
                    item.setFlags(flags & ~Qt.ItemFlag.ItemIsEditable)

                self.room_data_table.setItem(row, column, item)
        self.room_data_table.blockSignals(False)
