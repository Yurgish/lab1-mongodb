from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QAbstractItemView,
    QGroupBox,
    QHBoxLayout,
    QPushButton,
    QTableView,
    QVBoxLayout,
)

from ..models import SellerTableModel
from .proportional_header import ProportionalHeader
from .search_toolbar import SearchToolbar
from .table_actions import TableActions


class SellersPanel(QGroupBox):
    selected = Signal(object)
    sort_changed = Signal(str, bool)

    def __init__(self, parent=None) -> None:
        super().__init__("Sellers", parent)
        self.search: SearchToolbar
        self.table_actions: TableActions
        self.table: QTableView
        self.search, self.table_actions, self.table = (
            SearchToolbar("Search sellers...", self),
            TableActions(self),
            QTableView(self),
        )
        self.all_store_sellers = QPushButton("All store sellers", self)
        self.model = SellerTableModel()
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
        controls.addWidget(self.all_store_sellers)
        controls.addWidget(self.table_actions)
        layout.addLayout(controls)
        layout.addWidget(self.table)

    def _sort_clicked(self, section: int) -> None:
        fields = (
            "first_name",
            "last_name",
            "age",
            "phone",
            "email",
            "position",
            "salary",
            "store_id",
            "department_id",
            "created_at",
            "updated_at",
        )
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
