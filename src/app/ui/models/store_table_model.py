from typing import Any, Generic, TypeVar

from PySide6.QtCore import QAbstractTableModel, QModelIndex, QPersistentModelIndex, Qt

T = TypeVar("T")


class EntityTableModel(QAbstractTableModel, Generic[T]):
    def __init__(self, columns: list[str], rows: list[T] | None = None) -> None:
        super().__init__()
        self.columns, self.rows = columns, rows or []

    def rowCount(self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self.rows)

    def columnCount(self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self.columns)

    def data(
        self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole
    ) -> Any:
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None
        return self.row_values(self.rows[index.row()])[index.column()]

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole
    ) -> Any:
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        return self.columns[section] if orientation == Qt.Orientation.Horizontal else section + 1

    def set_rows(self, rows: list[T]) -> None:
        self.beginResetModel()
        self.rows = rows
        self.endResetModel()

    def item_at(self, row: int) -> T | None:
        return self.rows[row] if 0 <= row < len(self.rows) else None

    def row_values(self, _item: T) -> list[str]:
        del _item
        raise NotImplementedError


class StoreTableModel(EntityTableModel[Any]):
    def __init__(self) -> None:
        super().__init__(
            [
                "Name",
                "City",
                "Street",
                "Building",
                "Phone",
                "Status",
                "Departments",
                "Created",
                "Updated",
            ]
        )

    def row_values(self, item: Any) -> list[str]:
        return [
            item.name,
            item.address.city,
            item.address.street,
            item.address.building,
            str(item.contact_phone),
            "Active" if item.is_active else "Inactive",
            str(item.departments_count),
            item.created_at.strftime("%Y-%m-%d %H:%M"),
            item.updated_at.strftime("%Y-%m-%d %H:%M"),
        ]
