from collections.abc import Mapping
from typing import Any

from pymongo.collection import Collection

from app.common.mappers import map_document
from app.common.query import QueryOptions, get_sort_spec, text_search
from app.modules.store.schemas import StoreModel

STORE_SORT_FIELDS = {
    "name": "name",
    "created_at": "created_at",
    "updated_at": "updated_at",
    "is_active": "is_active",
}


class StoreRepository:
    def __init__(self, collection: Collection) -> None:
        self._collection = collection

    def create(self, document: Mapping[str, Any]) -> StoreModel:
        self._collection.insert_one(dict(document))
        created = self.get_by_id(str(document["_id"]))
        if created is None:
            raise RuntimeError("Store was inserted but could not be read back.")
        return created

    def get_by_id(self, store_id: str) -> StoreModel | None:
        document = self._collection.find_one({"_id": store_id})
        return None if document is None else map_document(document, StoreModel)

    def get_all(self, options: QueryOptions | None = None) -> list[StoreModel]:
        options = options or QueryOptions(sort_by="name")
        documents = self._collection.find(text_search(options.search, ("name",))).sort(
            get_sort_spec(options, STORE_SORT_FIELDS)
        )
        return [map_document(document, StoreModel) for document in documents]

    def update(self, store_id: str, updates: Mapping[str, Any]) -> StoreModel | None:
        self._collection.update_one({"_id": store_id}, {"$set": dict(updates)})
        return self.get_by_id(store_id)

    def delete(self, store_id: str) -> bool:
        result = self._collection.delete_one({"_id": store_id})
        return result.deleted_count > 0

    def change_departments_count(self, store_id: str, amount: int) -> None:
        self._collection.update_one({"_id": store_id}, {"$inc": {"departments_count": amount}})
