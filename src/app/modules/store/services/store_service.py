import uuid
from datetime import datetime, timezone

from app.common.errors import EntityNotFoundError, OperationError
from app.common.query import QueryOptions
from app.modules.seller.repositories import SellerRepository
from app.modules.store.repositories import StoreRepository
from app.modules.store.schemas import StoreCreate, StoreModel, StoreUpdate


class StoreService:
    def __init__(
        self, store_repository: StoreRepository, seller_repository: SellerRepository
    ) -> None:
        self._store_repository = store_repository
        self._seller_repository = seller_repository

    def create(self, data: StoreCreate) -> StoreModel:
        now = datetime.now(timezone.utc)
        document = {
            "_id": str(uuid.uuid4()),
            **data.model_dump(mode="python"),
            "departments": [],
            "departments_count": 0,
            "created_at": now,
            "updated_at": now,
        }
        return self._store_repository.create(document)

    def get_by_id(self, store_id: str) -> StoreModel:
        store = self._store_repository.get_by_id(store_id)
        if store is None:
            raise EntityNotFoundError(f"Store '{store_id}' not found.")
        return store

    def get_all(self, options: QueryOptions | None = None) -> list[StoreModel]:
        return self._store_repository.get_all(options)

    def update(self, store_id: str, data: StoreUpdate) -> StoreModel:
        self.get_by_id(store_id)
        updates = data.model_dump(exclude_unset=True, mode="python")
        if not updates:
            return self.get_by_id(store_id)
        updates["updated_at"] = datetime.now(timezone.utc)
        updated = self._store_repository.update(store_id, updates)
        if updated is None:
            raise OperationError(f"Store '{store_id}' disappeared while updating.")
        return updated

    def delete(self, store_id: str) -> None:
        self.get_by_id(store_id)
        self._seller_repository.delete_by_store_id(store_id)
        if not self._store_repository.delete(store_id):
            raise OperationError(f"Store '{store_id}' could not be deleted.")
