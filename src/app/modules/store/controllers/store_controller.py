from collections.abc import Mapping

from app.common.decorators import handle_errors
from app.common.errors import AppError
from app.common.query import QueryOptions
from app.modules.store.schemas import StoreCreate, StoreUpdate
from app.modules.store.services import StoreService


class StoreController:
    def __init__(self, view, service: StoreService) -> None:
        self._view = view
        self._service = service

    def _handle_error(self, error: AppError) -> None:
        self._view.show_error(error.title, str(error))

    @handle_errors
    def load(self, options: QueryOptions | None = None) -> None:
        self._view.show_stores(self._service.get_all(options))

    @handle_errors
    def create(self, form_data: Mapping[str, object]) -> None:
        data = StoreCreate.model_validate(dict(form_data))
        self._service.create(data)
        self._view.show_success("Store created.")
        self.load()

    @handle_errors
    def update(self, store_id: str, form_data: Mapping[str, object]) -> None:
        data = StoreUpdate.model_validate(dict(form_data))
        self._service.update(store_id, data)
        self._view.show_success("Store updated.")
        self.load()

    @handle_errors
    def delete(self, store_id: str) -> None:
        self._service.delete(store_id)
        self._view.show_success("Store deleted.")
        self.load()
