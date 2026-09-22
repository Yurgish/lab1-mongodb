from collections.abc import Mapping
from typing import Any

from pymongo.collection import Collection

from app.common.errors import EntityNotFoundError
from app.common.mappers import map_document
from app.modules.store.schemas import DepartmentModel


class DepartmentRepository:
    def __init__(self, collection: Collection) -> None:
        self._collection = collection

    def create(self, store_id: str, document: Mapping[str, Any]) -> DepartmentModel:
        department = dict(document)
        result = self._collection.update_one(
            {"_id": store_id}, {"$push": {"departments": department}}
        )
        if result.matched_count == 0:
            raise EntityNotFoundError(f"Store '{store_id}' not found.")
        return map_document(department, DepartmentModel)

    def get_by_id(self, store_id: str, department_id: str) -> DepartmentModel | None:
        document = self._collection.find_one(
            {"_id": store_id, "departments.id": department_id},
            {"departments": {"$elemMatch": {"id": department_id}}},
        )
        if document is None or not document.get("departments"):
            return None
        return map_document(document["departments"][0], DepartmentModel)

    def get_all(self, store_id: str) -> list[DepartmentModel]:
        documents = self._collection.aggregate(
            [
                {"$match": {"_id": store_id}},
                {"$unwind": "$departments"},
                {"$sort": {"departments.name": 1}},
                {"$replaceRoot": {"newRoot": "$departments"}},
            ]
        )
        return [map_document(document, DepartmentModel) for document in documents]

    def update(
        self, store_id: str, department_id: str, updates: Mapping[str, Any]
    ) -> DepartmentModel | None:
        self._collection.update_one(
            {"_id": store_id, "departments.id": department_id},
            {"$set": {f"departments.$.{key}": value for key, value in updates.items()}},
        )
        return self.get_by_id(store_id, department_id)

    def delete(self, store_id: str, department_id: str) -> bool:
        result = self._collection.update_one(
            {"_id": store_id}, {"$pull": {"departments": {"id": department_id}}}
        )
        return result.modified_count > 0
