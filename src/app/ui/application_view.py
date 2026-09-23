from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class ApplicationView(QWidget):
    """Single application view containing all store management functionality."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Store management"))
