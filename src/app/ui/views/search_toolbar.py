from PySide6.QtCore import QTimer, Signal
from PySide6.QtWidgets import QLineEdit, QToolBar


class SearchToolbar(QToolBar):
    search_changed = Signal(str)

    def __init__(self, placeholder: str, parent=None) -> None:
        super().__init__(parent)
        self.search = QLineEdit(self)
        self.search.setPlaceholderText(placeholder)
        self.search.setClearButtonEnabled(True)
        self._debounce = QTimer(self)
        self._debounce.setSingleShot(True)
        self._debounce.setInterval(250)
        self.search.textChanged.connect(self._schedule_search)
        self._debounce.timeout.connect(self._emit_search)
        self.addWidget(self.search)

    def _schedule_search(self) -> None:
        self._debounce.start()

    def _emit_search(self) -> None:
        self.search_changed.emit(self.text())

    def text(self) -> str:
        return self.search.text().strip()
