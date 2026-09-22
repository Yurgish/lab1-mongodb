import uuid
from datetime import datetime, timezone

from app.common.errors import EntityNotFoundError, OperationError
from app.modules.seller.repositories import SellerRepository
from app.modules.seller.schemas import SellerCreate, SellerModel, SellerUpdate
from app.modules.store.repositories import StoreRepository


class SellerService:
    def __init__(
        self, seller_repository: SellerRepository, store_repository: StoreRepository
    ) -> None:
        self._seller_repository = seller_repository
        self._store_repository = store_repository

    def create(self, data: SellerCreate) -> SellerModel:
        self._validate_department(data.store_id, data.department_id)
        now = datetime.now(timezone.utc)
        document = {
            "_id": str(uuid.uuid4()),
            **data.model_dump(mode="python"),
            "created_at": now,
            "updated_at": now,
        }
        return self._seller_repository.create(document)

    def get_by_id(self, seller_id: str) -> SellerModel:
        seller = self._seller_repository.get_by_id(seller_id)
        if seller is None:
            raise EntityNotFoundError(f"Seller '{seller_id}' not found.")
        return seller

    def get_all(self) -> list[SellerModel]:
        return self._seller_repository.get_all()

    def update(self, seller_id: str, data: SellerUpdate) -> SellerModel:
        seller = self.get_by_id(seller_id)
        updates = data.model_dump(exclude_unset=True, mode="python")
        store_id = updates.get("store_id", seller.store_id)
        department_id = updates.get("department_id", seller.department_id)
        self._validate_department(store_id, department_id)
        if not updates:
            return seller
        updates["updated_at"] = datetime.now(timezone.utc)
        updated = self._seller_repository.update(seller_id, updates)
        if updated is None:
            raise OperationError(f"Seller '{seller_id}' disappeared while updating.")
        return updated

    def delete(self, seller_id: str) -> None:
        self.get_by_id(seller_id)
        if not self._seller_repository.delete(seller_id):
            raise OperationError(f"Seller '{seller_id}' could not be deleted.")

    def _validate_department(self, store_id: str, department_id: str) -> None:
        store = self._store_repository.get_by_id(store_id)
        if store is None:
            raise EntityNotFoundError(f"Store '{store_id}' not found.")
        if not any(department.id == department_id for department in store.departments):
            raise EntityNotFoundError(f"Department '{department_id}' not found.")
