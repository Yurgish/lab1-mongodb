from app.common.query import QueryOptions
from app.modules.controller_events import Loaded


class SellerPresenter:
    def __init__(self, controller, model, notify) -> None:
        self.controller, self.model, self.notify = controller, model, notify

    def handle(self, event) -> None:
        if isinstance(event, Loaded) and event.resource == "sellers":
            self.model.set_rows(list(event.items))

    def load(
        self,
        store_id=None,
        department_id=None,
        search="",
        sort_by: str = "last_name",
        descending: bool = False,
    ) -> None:
        self.controller.load(
            store_id, department_id, QueryOptions(sort_by, descending, search or None)
        )

    def create(self, values) -> None:
        self.controller.create(values)

    def update(self, item_id, values) -> None:
        self.controller.update(item_id, values)

    def delete(self, item_id) -> None:
        self.controller.delete(item_id)
