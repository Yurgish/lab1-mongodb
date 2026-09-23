from typing import Any

from .store_table_model import EntityTableModel


class SellerTableModel(EntityTableModel[Any]):
    def __init__(self) -> None:
        super().__init__(
            [
                "First name",
                "Last name",
                "Age",
                "Phone",
                "Email",
                "Position",
                "Salary",
                "Store",
                "Department",
                "Created",
                "Updated",
            ]
        )

    def row_values(self, item: Any) -> list[str]:
        return [
            item.first_name,
            item.last_name,
            str(item.age),
            str(item.phone),
            str(item.email),
            item.position,
            f"{item.salary:.2f}",
            item.store_id,
            item.department_id,
            item.created_at.strftime("%Y-%m-%d %H:%M"),
            item.updated_at.strftime("%Y-%m-%d %H:%M"),
        ]
