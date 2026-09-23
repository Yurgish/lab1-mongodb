import uuid
from datetime import datetime, timezone

from app.common.errors import EntityNotFoundError, OperationError
from app.common.query import QueryOptions
from app.modules.seller.repositories import SellerRepository
from app.modules.store.repositories import DepartmentRepository, StoreRepository
from app.modules.store.schemas import DepartmentCreate, DepartmentModel, DepartmentUpdate


class DepartmentService:
    def __init__(
        self,
        department_repository: DepartmentRepository,
        store_repository: StoreRepository,
        seller_repository: SellerRepository,
    ) -> None:
        self._department_repository = department_repository
        self._store_repository = store_repository
        self._seller_repository = seller_repository

    def create(self, store_id: str, data: DepartmentCreate) -> DepartmentModel:
        self._require_store(store_id)
        now = datetime.now(timezone.utc)
        department = self._department_repository.create(
            store_id,
            {
                "id": str(uuid.uuid4()),
                **data.model_dump(mode="python"),
                "created_at": now,
                "updated_at": now,
            },
        )
        self._store_repository.change_departments_count(store_id, 1)
        return department

    def get_by_id(self, store_id: str, department_id: str) -> DepartmentModel:
        self._require_store(store_id)
        department = self._department_repository.get_by_id(store_id, department_id)
        if department is None:
            raise EntityNotFoundError(f"Department '{department_id}' not found.")
        department.sellers_count = self._seller_repository.count_by_department(
            store_id, department_id
        )
        return department

    def get_all(self, store_id: str, options: QueryOptions | None = None) -> list[DepartmentModel]:
        self._require_store(store_id)
        departments = self._department_repository.get_all(store_id, options)
        for department in departments:
            department.sellers_count = self._seller_repository.count_by_department(
                store_id, department.id
            )
        if options is not None and options.sort_by == "sellers":
            departments.sort(key=lambda department: department.sellers_count)
            if options.descending:
                departments.reverse()
        return departments

    def update(self, store_id: str, department_id: str, data: DepartmentUpdate) -> DepartmentModel:
        self.get_by_id(store_id, department_id)
        updates = data.model_dump(exclude_unset=True, mode="python")
        if not updates:
            return self.get_by_id(store_id, department_id)
        updates["updated_at"] = datetime.now(timezone.utc)
        updated = self._department_repository.update(store_id, department_id, updates)
        if updated is None:
            raise OperationError(f"Department '{department_id}' disappeared while updating.")
        return updated

    def delete(self, store_id: str, department_id: str) -> None:
        self.get_by_id(store_id, department_id)
        self._seller_repository.delete_by_department_id(store_id, department_id)
        if not self._department_repository.delete(store_id, department_id):
            raise OperationError(f"Department '{department_id}' could not be deleted.")
        self._store_repository.change_departments_count(store_id, -1)

    def _require_store(self, store_id: str) -> None:
        if self._store_repository.get_by_id(store_id) is None:
            raise EntityNotFoundError(f"Store '{store_id}' not found.")
