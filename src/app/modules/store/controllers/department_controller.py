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
from app.modules.store.schemas import DepartmentCreate, DepartmentUpdate
from app.modules.store.services import DepartmentService


class DepartmentController:
    def __init__(
        self, service: DepartmentService, on_event: ControllerEventHandler | None = None
    ) -> None:
        self._service = service
        self._on_event = on_event or discard_event

    def _handle_error(self, error: AppError) -> None:
        self._on_event(Failed(error.title, str(error)))

    @handle_errors
    def load(self, store_id: str, options: QueryOptions | None = None) -> None:
        self._on_event(Loaded("departments", self._service.get_all(store_id, options)))

    @handle_errors
    def create(self, store_id: str, form_data: Mapping[str, object]) -> None:
        data = DepartmentCreate.model_validate(dict(form_data))
        self._service.create(store_id, data)
        self._on_event(Succeeded("Department created."))
        self.load(store_id)

    @handle_errors
    def update(self, store_id: str, department_id: str, form_data: Mapping[str, object]) -> None:
        data = DepartmentUpdate.model_validate(dict(form_data))
        self._service.update(store_id, department_id, data)
        self._on_event(Succeeded("Department updated."))
        self.load(store_id)

    @handle_errors
    def delete(self, store_id: str, department_id: str) -> None:
        self._service.delete(store_id, department_id)
        self._on_event(Succeeded("Department deleted."))
        self.load(store_id)
