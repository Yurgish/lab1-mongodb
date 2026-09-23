from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel


class EmptyState(QLabel):
    def __init__(self, message: str = "No records found.", parent=None) -> None:
        super().__init__(message, parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
