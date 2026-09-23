from app.common.query import QueryOptions
from app.modules.controller_events import Loaded


class DepartmentPresenter:
    def __init__(self, controller, model, notify) -> None:
        self.controller, self.model, self.notify = controller, model, notify

    def handle(self, event) -> None:
        if isinstance(event, Loaded) and event.resource == "departments":
            self.model.set_rows(list(event.items))

    def load(
        self,
        store_id: str | None,
        search: str = "",
        sort_by: str = "name",
        descending: bool = False,
    ) -> None:
        if store_id:
            self.controller.load(store_id, QueryOptions(sort_by, descending, search or None))
        else:
            self.model.set_rows([])

    def create(self, store_id, values) -> None:
        self.controller.create(store_id, values)

    def update(self, store_id, item_id, values) -> None:
        self.controller.update(store_id, item_id, values)

    def delete(self, store_id, item_id) -> None:
        self.controller.delete(store_id, item_id)
