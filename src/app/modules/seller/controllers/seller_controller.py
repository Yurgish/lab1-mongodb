from collections.abc import Mapping

from app.common.decorators import handle_errors
from app.common.errors import AppError
from app.common.query import QueryOptions
from app.modules.seller.schemas import SellerCreate, SellerUpdate
from app.modules.seller.services import SellerService


class SellerController:
    def __init__(self, view, service: SellerService) -> None:
        self._view = view
        self._service = service

    def _handle_error(self, error: AppError) -> None:
        self._view.show_error(error.title, str(error))

    @handle_errors
    def load(
        self,
        store_id: str | None = None,
        department_id: str | None = None,
        options: QueryOptions | None = None,
    ) -> None:
        if store_id is not None and department_id is not None:
            sellers = self._service.get_by_department(store_id, department_id, options)
        else:
            sellers = self._service.get_all(options)
        self._view.show_sellers(sellers)

    @handle_errors
    def create(self, form_data: Mapping[str, object]) -> None:
        data = SellerCreate.model_validate(dict(form_data))
        self._service.create(data)
        self._view.show_success("Seller created.")
        self.load()

    @handle_errors
    def update(self, seller_id: str, form_data: Mapping[str, object]) -> None:
        data = SellerUpdate.model_validate(dict(form_data))
        self._service.update(seller_id, data)
        self._view.show_success("Seller updated.")
        self.load()

    @handle_errors
    def delete(self, seller_id: str) -> None:
        self._service.delete(seller_id)
        self._view.show_success("Seller deleted.")
        self.load()
