from PySide6.QtWidgets import *
from PySide6.QtGui import *
from backend.path import NUMBER_OF_ROOM_PATH
from UI.dialogChangeNumberOfRoom import DiaLogChangeNumberOfRoom
from .path import PATH_TO_ROOM_DATA, DATA_DIR
from .room import Room
from pathlib import Path


class Shortcuts:
    def __init__(self, main_window: QWidget):
        self.room = Room()
        self.main_window = main_window

    def create_shortcuts(self):
        self.change_number_of_rooms_shortcut = QShortcut(QKeySequence('Ctrl+Shift+R'), self.main_window)
        self.change_number_of_rooms_shortcut.activated.connect(self.get_and_change_number_of_rooms)

    def get_and_change_number_of_rooms(self):
        with open(NUMBER_OF_ROOM_PATH, 'r', encoding='utf-8') as number_of_rooms_file:
            number_of_rooms_file.seek(0)

            current_number_of_room = number_of_rooms_file.readline()
            new_number_of_room, ok = DiaLogChangeNumberOfRoom.get_new_number_of_room_value(current_number_of_room)
            if not ok:
                return
            
            self.change_number_of_room(new_number_of_room)

    def change_number_of_room(self, new_number_of_room):
        self.new_number_of_room = new_number_of_room
        with open(NUMBER_OF_ROOM_PATH, 'w', encoding='utf-8') as number_of_rooms_file:
            number_of_rooms_file.write(str(new_number_of_room))
            self.remove_extra_room()

        a = self.room.get_number_of_rooms()
        self.room.check_number_of_rooms_data_file()
        del a

    def remove_extra_room(self):
        new_room_list = self.get_new_room_list()
        old_room_list = self.get_old_room_list()
        extra_room_list = set(old_room_list) - set(new_room_list)

        for room_path in extra_room_list:
            Path(room_path).unlink(missing_ok=True)

        self.move_to_lasted_room(extra_room_list)

    def get_new_room_list(self):
        room_list = []
        for i in range(self.new_number_of_room):
            room_list.append(Path(PATH_TO_ROOM_DATA).parent / f'room{i + 1}.csv')
        return room_list

    def get_old_room_list(self):
        old_room_list = [file for file in Path(PATH_TO_ROOM_DATA).parent.glob('*.csv')]
        return old_room_list
    
    def move_to_lasted_room(self, extra_room_list: list):
        current_room = self.room.get_opening_room()
        if Path(PATH_TO_ROOM_DATA).parent / f'room{current_room}.csv' in extra_room_list:
            with open(Path(DATA_DIR) / 'opening_room.txt', 'w+', encoding='utf-8') as opening_room_file:
                opening_room_file.seek(0)
                opening_room_file.write(str(self.new_number_of_room))
