from PySide6.QtWidgets import *


class RemovedBoardPlaceholder(QStyledItemDelegate):
    def create_editor(parent, option, index):
        editor = super().__init__(parent, option, index)

        if isinstance(editor, QLineEdit):
            editor.setPlaceholderText('')
        return editor
