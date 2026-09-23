from typing import Any

from .store_table_model import EntityTableModel


class DepartmentTableModel(EntityTableModel[Any]):
    def __init__(self) -> None:
        super().__init__(["Name", "Floor", "Sellers", "Description", "Created", "Updated"])

    def row_values(self, item: Any) -> list[str]:
        return [
            item.name,
            str(item.floor),
            str(item.sellers_count),
            item.description,
            item.created_at.strftime("%Y-%m-%d %H:%M"),
            item.updated_at.strftime("%Y-%m-%d %H:%M"),
        ]
