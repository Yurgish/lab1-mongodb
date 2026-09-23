from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QMainWindow

from app.ui.application_view import ApplicationView


class AppWindow(QMainWindow):
    """Application shell containing the single management view."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Store management")
        self.setMinimumSize(1280, 850)
        self.setCentralWidget(ApplicationView(self))

    def closeEvent(self, event: QCloseEvent) -> None:
        central_widget = self.centralWidget()
        if isinstance(central_widget, ApplicationView):
            central_widget.close_database()
        event.accept()
