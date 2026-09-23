from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QAbstractItemView, QGroupBox, QHBoxLayout, QTableView, QVBoxLayout

from ..models import DepartmentTableModel
from .proportional_header import ProportionalHeader
from .search_toolbar import SearchToolbar
from .table_actions import TableActions


class DepartmentsPanel(QGroupBox):
    selected = Signal(object)
    sort_changed = Signal(str, bool)

    def __init__(self, parent=None) -> None:
        super().__init__("Departments", parent)
        self.search: SearchToolbar
        self.table_actions: TableActions
        self.table: QTableView
        self.search, self.table_actions, self.table = (
            SearchToolbar("Search departments...", self),
            TableActions(self),
            QTableView(self),
        )
        self.model = DepartmentTableModel()
        self.table.setModel(self.model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        header = ProportionalHeader(self.table)
        self.table.setHorizontalHeader(header)
        header.setStretchLastSection(False)
        header.setSectionsClickable(True)
        header.setSortIndicatorShown(True)
        header.sectionClicked.connect(self._sort_clicked)
        self._sort_section = -1
        self._descending = False
        self.table.clicked.connect(
            lambda index: self.selected.emit(self.model.item_at(index.row()))
        )
        layout = QVBoxLayout(self)
        controls = QHBoxLayout()
        controls.addWidget(self.search, 1)
        controls.addWidget(self.table_actions)
        layout.addLayout(controls)
        layout.addWidget(self.table)

    def _sort_clicked(self, section: int) -> None:
        fields = ("name", "floor", "sellers", "description", "created_at", "updated_at")
        header = self.table.horizontalHeader()
        if self._sort_section == section:
            self._descending = not self._descending
        else:
            self._sort_section = section
            self._descending = False
        descending = self._descending
        order = Qt.SortOrder.DescendingOrder if descending else Qt.SortOrder.AscendingOrder
        header.setSortIndicator(section, order)
        self.sort_changed.emit(fields[section], descending)
