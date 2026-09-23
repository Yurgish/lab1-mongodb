from PySide6.QtWidgets import QMainWindow

from app.ui.application_view import ApplicationView


class AppWindow(QMainWindow):
    """Application shell containing the application's single view."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Store management")
        self.setMinimumSize(1200, 800)
        self.setCentralWidget(ApplicationView(self))
