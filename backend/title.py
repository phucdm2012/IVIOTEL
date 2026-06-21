from pathlib import Path
from backend.path import DATA_DIR
from backend.signal import ReloadTable
import time


class TitleLogic:
    def __init__(self, table_reload_signal: ReloadTable):
        self.opening_room_data_path = Path(DATA_DIR) / 'opening_room.txt'
        self.number_of_rooms_data_path = Path(DATA_DIR) / 'number_of_rooms.txt'
        self.reload_table_signal = table_reload_signal

    def go_to_new_room(self, new_room: int):
        with open(self.opening_room_data_path, 'w+', encoding='utf-8') as opening_room_file:
            opening_room_file.seek(0)
            opening_room_file.write(str(new_room))
        self.reload_table_signal.reload_table_sigal.emit()

    def get_number_of_rooms(self):
        with open(self.number_of_rooms_data_path, 'r', encoding='utf-8') as number_of_rooms_file:
            return int(number_of_rooms_file.read())
