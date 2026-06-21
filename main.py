from PySide6.QtWidgets import *
from PySide6.QtCore import *
from UI.mainWindow import MainWindow
from backend.shortcuts import Shortcuts
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    shortcut = Shortcuts(window)

    shortcut.create_shortcuts()
    window.show()
    window.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
    sys.exit(app.exec())
