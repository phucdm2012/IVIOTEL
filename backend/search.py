from PySide6.QtWidgets import *
from .path import PATH_TO_ROOM_DATA, DATA_DIR
from .room import Room
from backend.signal import ReloadTable
from pathlib import Path
import pandas as pd
import datetime as dt

now = dt.datetime.now()


class Search:
    def __init__(self):
        self.room = Room()
        self.current_room = self.room.get_opening_room()
        self.room_data = self.room.get_room_data(room=str(self.current_room))

    def search(self, search_year, search_month):
        try:
            year_value = int(search_year)
            month_value = int(search_month)
        except (ValueError, TypeError):
            return pd.DataFrame()

        year_filtered_data = self.room_data[self.room_data['Năm'] == year_value]
        month_filtered_data = year_filtered_data[year_filtered_data['Tháng'] == month_value]

        if month_value != 0:
            return month_filtered_data
        return year_filtered_data
    
    def add_new_month(self, reload_table_signal: ReloadTable):
        self.room_data.sort_values(by='Năm')
        self.room_data.sort_values(by='Tháng')

        path_to_data = Path(PATH_TO_ROOM_DATA).parent / f'room{self.current_room}.csv'

        self.years = [str(now.year), str(now.year - 1), str(now.year - 2)]
        self.months = list(map(str, range(1, 13)))

        new_year, year_ok = QInputDialog.getItem(None, "Chọn năm", "Chọn năm để tạo tháng mới", self.years, editable=False)
        if not year_ok:
            return

        new_month, month_ok = QInputDialog.getItem(None, "Chọn tháng", "Chọn tháng để thạo tháng mới", self.months, editable=False)
        if not month_ok:
            return
        
        self.new_year = int(new_year)
        self.new_month = int(new_month)

        year_filter = self.room_data[self.room_data['Năm'] == self.new_year]

        if not year_filter.empty and (year_filter['Tháng'] == self.new_month).any():
            QMessageBox.warning(None, 'Lỗi', f'Tháng {self.new_month}/{self.new_year} đã tồn tại.')
            return

        new_month_dict = {'Tháng':self.new_month,'Năm':self.new_year}
        new_month_row = pd.DataFrame([new_month_dict])
                
        self.room_data = pd.concat([self.room_data, new_month_row], ignore_index=True)

        self.room_data.sort_values(by=['Năm', 'Tháng'], inplace=True, ignore_index=True)
        self.room_data.to_csv(path_to_data, index=False)
        reload_table_signal.reload_table_sigal.emit()

    def export_excel(self):
        room_data = self.room_data.fillna(0)

        file_filter = 'Excel file (*.xlsx)'

        file_path, select_filter = QFileDialog.getSaveFileName(None, "Xuất Excel", "", file_filter)

        if file_path:
            room_data.to_csv(file_path, index=False)
