from PySide6.QtCore import *
import pandas as pd


class SearchSignal(QObject):
    searched_value = Signal(pd.DataFrame)

class ReloadTable(QObject):
    reload_table_sigal = Signal()
