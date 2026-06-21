from backend.path import NUMBER_OF_ROOM_PATH, PATH_TO_ROOM_DATA, DATA_DIR
from pathlib import Path
import pandas as pd
import os
import glob
import datetime as dt

now = dt.datetime.now()
ROOM_DATA_HEADER = f'Tháng,Năm,Số điện mới,Số điện cũ,Tổng điện tiêu thụ,Thành tiền\n{str(now.month)},{str(now.year)},,,,'


class Room:
    def __init__(self):
        self.default_number_of_rooms = 10

    def get_number_of_rooms(self):
        """Lấy số lượng phòng đang có: get_number_of_rooms()"""
        try:
            with open(NUMBER_OF_ROOM_PATH, 'a+', encoding="utf-8") as number_of_rooms_file:
                number_of_rooms_file.seek(0)
                content = number_of_rooms_file.read().strip()
                if not content:
                    number_of_rooms_file.write('10')
                    self.number_of_rooms = self.default_number_of_rooms
                else:
                    try:
                        self.number_of_rooms = int(content)
                        if self.number_of_rooms <= 0:
                            self.number_of_rooms = self.default_number_of_rooms
                    except Exception:
                        self.number_of_rooms = self.default_number_of_rooms
        except Exception as e:
            print(f"[NumberOfRooms] {e}")
            self.number_of_rooms = self.default_number_of_rooms

    def get_room_data(self, room: str) -> pd.DataFrame:
        """Lấy data phòng:
        room = Room()
        room_name = 1
        room.get_room_data(str(room_name))
        """
        if not hasattr(self, 'number_of_rooms'):
            try:
                self.get_number_of_rooms()
            except Exception:
                pass
            if not hasattr(self, 'number_of_rooms'):
                self.number_of_rooms = self.default_number_of_rooms

        self.__make_rooms_dir()
        files_path = glob.glob(str(PATH_TO_ROOM_DATA))

        if not files_path:
            for i in range(self.number_of_rooms):
                self.__create_room_data_file(i + 1)
            files_path = glob.glob(str(PATH_TO_ROOM_DATA))

        try:
            file_path = self.rooms_dir / f'room{room}.csv'
            return pd.DataFrame(pd.read_csv(file_path)).fillna('')
        except Exception:
            return pd.DataFrame().fillna('')

    def check_number_of_rooms_data_file(self):
        """Kiểm tra có thiếu file data hay không, nếu có thì tạo"""
        self.__make_rooms_dir()

        for number_of_room in range(1, self.number_of_rooms + 1):
            file_path = self.rooms_dir / f'room{number_of_room}.csv'

            if not file_path.exists():
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(ROOM_DATA_HEADER)

    def get_opening_room(self):
        file_opening_room_dir = self.__get_file_opening_room_dir()
        try:
            with open(file_opening_room_dir, mode='a+',encoding='utf-8') as opening_room_file:
                opening_room_file.seek(0)
                content = opening_room_file.read().strip()
                if not content:
                    opening_room_file.write('1')
                    return 1
                return int(content)
        except FileNotFoundError:
            with open(file_opening_room_dir, 'w', encoding='utf-8') as file:
                file.write('1')
            return 1
        except Exception as e:
            print(f'[Room] {e}')
            return 1

    def __create_room_data_file(self, room_name):
        """Tạo file data phòng"""
        self.__make_rooms_dir()
        file_path = self.rooms_dir / f'room{room_name}.csv'

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(ROOM_DATA_HEADER)

    def __make_rooms_dir(self):
        """Lấy địa chỉ đến thư mục data phòng"""
        self.rooms_dir = Path(PATH_TO_ROOM_DATA).parent
        self.rooms_dir.mkdir(parents=True, exist_ok=True)

    def __get_file_opening_room_dir(self):
        """Lấy địa chỉ đến file opening_room.txt"""
        return Path(DATA_DIR) / 'opening_room.txt'
