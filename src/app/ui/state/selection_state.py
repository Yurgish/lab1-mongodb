from dataclasses import dataclass


@dataclass
class SelectionState:
    store_id: str | None = None
    department_id: str | None = None
    seller_scope: str = "store"

    def select_store(self, store_id: str | None) -> None:
        self.store_id, self.department_id, self.seller_scope = store_id, None, "store"

    def select_department(self, department_id: str | None) -> None:
        self.department_id, self.seller_scope = department_id, "department"

    def show_all_sellers(self) -> None:
        self.department_id, self.seller_scope = None, "store"
