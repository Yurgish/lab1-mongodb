from PySide6.QtCore import Qt
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import QHeaderView


class ProportionalHeader(QHeaderView):
    """Fills the table without forcing every column to have the same width."""

    def __init__(self, parent=None) -> None:
        super().__init__(Qt.Orientation.Horizontal, parent)
        self._resizing = False
        self.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self._resize_proportionally()

    def _resize_proportionally(self) -> None:
        if self._resizing or self.count() == 0:
            return
        self._resizing = True
        try:
            minimum = 72
            preferred = [max(minimum, self.sectionSizeHint(index)) for index in range(self.count())]
            available = max(0, self.viewport().width())
            total_preferred = sum(preferred)
            if available <= 0:
                return
            if total_preferred < available:
                extra = available - total_preferred
                total_weight = sum(preferred)
                widths = [base + (extra * base // total_weight) for base in preferred]
                widths[-1] += available - sum(widths)
            else:
                scale = available / total_preferred
                widths = [max(minimum, int(base * scale)) for base in preferred]
                widths[-1] += available - sum(widths)
            for index, width in enumerate(widths):
                self.resizeSection(index, width)
        finally:
            self._resizing = False
