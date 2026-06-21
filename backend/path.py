from pathlib import Path

BASE_DIR = Path.cwd()

DATA_DIR = BASE_DIR / 'data'

NUMBER_OF_ROOM_PATH = DATA_DIR / 'number_of_rooms.txt'

PRICE_DATA_PATH = DATA_DIR / 'price.csv'

PATH_TO_ROOM_DATA = DATA_DIR / 'rooms' / '*.csv'

PATH_TO_ICON = DATA_DIR / 'icon'
