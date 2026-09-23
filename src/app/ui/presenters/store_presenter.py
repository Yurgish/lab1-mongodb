from app.common.query import QueryOptions
from app.modules.controller_events import Loaded


class StorePresenter:
    def __init__(self, controller, model, notify) -> None:
        self.controller, self.model, self.notify = controller, model, notify

    def handle(self, event) -> None:
        if isinstance(event, Loaded) and event.resource == "stores":
            self.model.set_rows(list(event.items))

    def load(self, search: str = "", sort_by: str = "name", descending: bool = False) -> None:
        self.controller.load(QueryOptions(sort_by, descending, search or None))

    def create(self, values) -> None:
        self.controller.create(values)

    def update(self, item_id: str, values) -> None:
        self.controller.update(item_id, values)

    def delete(self, item_id: str) -> None:
        self.controller.delete(item_id)
