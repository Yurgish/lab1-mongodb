from collections.abc import Mapping

from app.common.decorators import handle_errors
from app.common.errors import AppError
from app.modules.store.schemas import DepartmentCreate, DepartmentUpdate
from app.modules.store.services import DepartmentService


class DepartmentController:
    def __init__(self, view, service: DepartmentService) -> None:
        self._view = view
        self._service = service

    def _handle_error(self, error: AppError) -> None:
        self._view.show_error(error.title, str(error))

    @handle_errors
    def load(self, store_id: str) -> None:
        self._view.show_departments(self._service.get_all(store_id))

    @handle_errors
    def create(self, store_id: str, form_data: Mapping[str, object]) -> None:
        data = DepartmentCreate.model_validate(dict(form_data))
        self._service.create(store_id, data)
        self._view.show_success("Department created.")
        self.load(store_id)

    @handle_errors
    def update(self, store_id: str, department_id: str, form_data: Mapping[str, object]) -> None:
        data = DepartmentUpdate.model_validate(dict(form_data))
        self._service.update(store_id, department_id, data)
        self._view.show_success("Department updated.")
        self.load(store_id)

    @handle_errors
    def delete(self, store_id: str, department_id: str) -> None:
        self._service.delete(store_id, department_id)
        self._view.show_success("Department deleted.")
        self.load(store_id)
