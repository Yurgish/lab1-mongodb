from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget


class TableActions(QWidget):
    add_clicked = Signal()
    edit_clicked = Signal()
    delete_clicked = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        for text, tip, signal in (
            ("Add", "Create", self.add_clicked),
            ("Edit", "Edit selected", self.edit_clicked),
            ("Delete", "Delete selected", self.delete_clicked),
        ):
            button = QPushButton(text, self)
            button.setToolTip(tip)
            button.setAccessibleName(tip)
            button.clicked.connect(signal)
            layout.addWidget(button)
