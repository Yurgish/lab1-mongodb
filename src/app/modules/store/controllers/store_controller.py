from collections.abc import Mapping

from app.common.decorators import handle_errors
from app.common.errors import AppError
from app.common.query import QueryOptions
from app.modules.controller_events import (
    ControllerEventHandler,
    Failed,
    Loaded,
    Succeeded,
    discard_event,
)
from app.modules.store.schemas import StoreCreate, StoreUpdate
from app.modules.store.services import StoreService


class StoreController:
    def __init__(
        self, service: StoreService, on_event: ControllerEventHandler | None = None
    ) -> None:
        self._service = service
        self._on_event = on_event or discard_event

    def _handle_error(self, error: AppError) -> None:
        self._on_event(Failed(error.title, str(error)))

    @handle_errors
    def load(self, options: QueryOptions | None = None) -> None:
        self._on_event(Loaded("stores", self._service.get_all(options)))

    @handle_errors
    def create(self, form_data: Mapping[str, object]) -> None:
        data = StoreCreate.model_validate(dict(form_data))
        self._service.create(data)
        self._on_event(Succeeded("Store created."))
        self.load()

    @handle_errors
    def update(self, store_id: str, form_data: Mapping[str, object]) -> None:
        data = StoreUpdate.model_validate(dict(form_data))
        self._service.update(store_id, data)
        self._on_event(Succeeded("Store updated."))
        self.load()

    @handle_errors
    def delete(self, store_id: str) -> None:
        self._service.delete(store_id)
        self._on_event(Succeeded("Store deleted."))
        self.load()
